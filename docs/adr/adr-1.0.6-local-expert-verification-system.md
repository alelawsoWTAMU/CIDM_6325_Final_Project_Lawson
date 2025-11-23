# ADR 1.0.6: Local Expert Verification System

**Status:** Implemented  
**Date:** 2025-11-23  
**Decision Makers:** Development Team  
**Tags:** #authentication #user-roles #experts #verification #community

## Context and Problem Statement

The application needs to distinguish between regular homeowners and professional service providers ("Local Experts") who can share verified maintenance tips. We need a system that:

1. Allows professionals to register and apply for expert status
2. Requires admin verification before experts can contribute content
3. Prevents unverified experts from accessing the platform
4. Displays verification badges to distinguish expert content
5. Maintains a single, unified registration flow for both user types

The challenge is implementing this distinction without creating confusion in the registration process or allowing unverified users to contribute potentially misleading professional advice.

## Decision Drivers

* **Trust & Safety**: Only verified professionals should share expert tips
* **User Experience**: Simple, clear registration process for both user types
* **Admin Control**: Administrators must approve all expert applications
* **Content Quality**: Expert status should be immediately visible to users
* **Security**: Unverified experts must be blocked from platform access
* **Scalability**: System must handle growing number of expert applications

## Considered Options

### Option 1: Separate Registration Flows
**Description**: Completely separate registration pages for homeowners and experts

**Pros:**
- Clear separation of user types
- Different form fields for each type
- No conditional logic needed

**Cons:**
- Duplicate code and templates
- Confusing navigation for new users
- Harder to maintain two registration systems

### Option 2: Post-Registration Expert Application
**Description**: All users register normally, then apply for expert status separately

**Pros:**
- Simple initial registration
- Users can explore platform before applying

**Cons:**
- Two-step process is confusing
- Users might not find expert application
- Creates inactive accounts that never complete application

### Option 3: Combined Registration with Progressive Disclosure ✅ **SELECTED**
**Description**: Single registration form with radio button selection and conditional field display

**Pros:**
- Single, clear registration entry point
- Progressive disclosure reduces complexity
- JavaScript shows/hides relevant fields dynamically
- All information collected upfront
- Immediate admin notification of new applications

**Cons:**
- Longer form for experts
- More complex form validation logic

## Decision Outcome

**Chosen option:** "Combined Registration with Progressive Disclosure" because it provides the best user experience while maintaining strict verification controls and collecting all necessary information in one step.

### Implementation Details

#### 1. User Model Extensions
```python
# accounts/models.py
class User(AbstractUser):
    is_verified_expert = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # Overridden for experts
    # ... other fields
```

#### 2. ExpertProfile Model
```python
class ExpertProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Company Information
    company_name = models.CharField(max_length=200)
    trade = models.CharField(max_length=50, choices=TRADE_CHOICES)
    
    # Contact Information
    business_phone = models.CharField(max_length=20)
    business_email = models.EmailField()
    website = models.URLField(blank=True)
    
    # Business Address
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    
    # Credentials
    license_number = models.CharField(max_length=50, blank=True)
    years_in_business = models.PositiveIntegerField()
    insurance_verified = models.BooleanField(default=False)
    
    # Approval Tracking
    application_submitted = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, null=True, blank=True, 
                                   on_delete=models.SET_NULL,
                                   related_name='approved_experts')
    approved_at = models.DateTimeField(null=True, blank=True)
```

**Trade Choices:**
- General Contractor
- Plumber
- Electrician
- HVAC Technician
- Roofer
- Landscaper
- Painter
- Carpenter
- Mason
- Appliance Repair
- Other

#### 3. Combined Registration Form
```python
# accounts/forms.py
class CombinedRegistrationForm(UserCreationForm):
    account_type = forms.ChoiceField(
        choices=[
            ('homeowner', 'Homeowner'),
            ('expert', 'Local Expert (Requires Verification)')
        ],
        widget=forms.RadioSelect
    )
    
    # Common fields: username, email, password, location
    # Homeowner fields: is_first_time_homeowner
    # Expert fields: company_name, trade, business_phone, etc.
    
    def clean(self):
        # Validates expert fields are required when account_type='expert'
        
    def save(self):
        if account_type == 'homeowner':
            user.is_active = True
        elif account_type == 'expert':
            user.is_active = False  # Blocks login until verified
            # Creates ExpertProfile automatically
```

#### 4. Registration View Logic
```python
# accounts/views.py
class RegisterView(CreateView):
    form_class = CombinedRegistrationForm
    
    def form_valid(self, form):
        response = super().form_valid(form)
        account_type = form.cleaned_data.get('account_type')
        
        if account_type == 'homeowner':
            login(self.request, self.object)  # Auto-login
            messages.success(self.request, "Welcome!")
        elif account_type == 'expert':
            messages.info(
                self.request,
                "Your expert application has been submitted. "
                "An administrator will review your information..."
            )
            return redirect('accounts:login')
        
        return response
```

#### 5. Admin Approval Workflow
```python
# accounts/admin.py
@admin.register(ExpertProfile)
class ExpertProfileAdmin(admin.ModelAdmin):
    actions = ['approve_experts', 'revoke_expert_status']
    
    def approve_experts(self, request, queryset):
        for profile in queryset:
            profile.user.is_verified_expert = True
            profile.user.is_active = True  # Enable login
            profile.approved_by = request.user
            profile.approved_at = timezone.now()
            profile.user.save()
            profile.save()
```

#### 6. Content Creation Restriction
```python
# tips/views.py
class TipCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_verified_expert
    
    def handle_no_permission(self):
        messages.error(
            self.request,
            "Only verified experts can share tips."
        )
        return redirect('tips:tip_list')
```

#### 7. Template Progressive Disclosure
```javascript
// templates/accounts/register.html
document.addEventListener('DOMContentLoaded', function() {
    function updateFieldsVisibility() {
        if (expertRadio.checked) {
            homeownerFields.style.display = 'none';
            expertFields.style.display = 'block';
            submitButton.textContent = 'Submit Expert Application';
        } else {
            homeownerFields.style.display = 'block';
            expertFields.style.display = 'none';
            submitButton.textContent = 'Create Account';
        }
    }
    
    homeownerRadio.addEventListener('change', updateFieldsVisibility);
    expertRadio.addEventListener('change', updateFieldsVisibility);
});
```

### Verification Workflow

1. **Expert Registration**:
   - User selects "Local Expert" on registration form
   - Fills out company information, contact details, address, credentials
   - Submits application
   - User account created with `is_active=False` (blocks login)
   - ExpertProfile created and linked to user
   - Redirect to login page with message about pending verification

2. **Admin Review**:
   - Admin receives notification (via Django admin)
   - Reviews ExpertProfile information in admin panel
   - Verifies business credentials, license numbers, contact information
   - Selects expert profile(s) and uses "Approve Selected Experts" bulk action
   - System sets `is_verified_expert=True` and `is_active=True`
   - Records approval timestamp and admin user

3. **Expert Access**:
   - Expert can now log in (is_active=True)
   - Expert profile displays verification badge
   - Expert can create and share tips
   - Expert tips show "Verified Expert" badge to all users

4. **Revocation Process**:
   - Admin can revoke expert status using "Revoke Expert Status" action
   - Sets `is_verified_expert=False`
   - Expert can still login but cannot create new tips
   - Existing tips remain visible but without verified badge

### Security Measures

1. **Login Blocking**: Django's authentication system respects `is_active=False`, preventing unverified experts from logging in

2. **View-Level Protection**: `UserPassesTestMixin` on `TipCreateView` checks `is_verified_expert` flag

3. **Form Validation**: Conditional validation ensures all expert fields are provided

4. **Admin Audit Trail**: Records who approved experts and when

5. **Template Guards**: Expert-only features hidden/disabled for non-experts

### UI/UX Considerations

#### Registration Form Design
- Radio buttons at top make account type selection obvious
- Clear descriptions under each option explain the difference
- Expert option explicitly mentions "Requires Verification"
- Alert box in expert section explains the approval process
- Submit button text changes dynamically: "Create Account" vs "Submit Expert Application"

#### Verification Badges
- Verified experts get green "Verified Expert" badge on profile
- Expert tips display badge next to author name
- Blue checkmark icon (planned enhancement)
- Badge is Bootstrap 5 success badge with custom styling

#### Messaging
- Clear success message for homeowners: "Welcome to Home Maintenance Compass!"
- Informative message for experts: "Your expert application has been submitted. An administrator will review..."
- Error message when unverified expert tries to create tip: "Only verified experts can share tips."

## Consequences

### Positive

* **Trust**: Users can confidently trust tips from verified experts
* **Quality**: Admin review ensures only qualified professionals contribute
* **Security**: Unverified accounts cannot access platform or create content
* **Clarity**: Single registration page with progressive disclosure is intuitive
* **Scalability**: Admin bulk actions handle multiple applications efficiently
* **Audit**: Complete trail of who approved which experts and when

### Negative

* **Admin Burden**: Every expert application requires manual review
* **Delayed Access**: Experts must wait for approval before using platform
* **Complex Form**: Expert registration form is lengthy (15+ fields)
* **No Auto-Verification**: Cannot integrate with third-party verification services yet

### Neutral

* **Email Notifications**: Currently not implemented; admins must check Django admin
* **Expert Directory**: Not yet implemented but data model supports it
* **Badge Styling**: Using Bootstrap success badge; custom blue checkmark planned
* **Profile Public View**: Expert profiles are viewable but not searchable yet

## Compliance and Considerations

### Data Privacy
- Business contact information collected with explicit purpose (verification)
- Address required for legitimacy verification
- License numbers stored but not publicly displayed
- Admin access logged for audit purposes

### Legal Considerations
- No liability assumed for expert advice
- Experts' tips are their own professional opinions
- Platform acts as content host, not advisor
- Terms of service should clarify expert verification is for identity, not endorsement

### Accessibility
- Form meets WCAG 2.1 AA standards
- Radio buttons keyboard-navigable
- Clear labels and ARIA attributes
- Success/error messages announced to screen readers

## Related Documents

* **ADR 1.0.4**: Community Tips Moderation Workflow
* **ADR 1.0.2**: Core Data Models and Relationships
* **Brief**: brief-local-expert-verification.md

## Future Enhancements

1. **Email Notifications**: Automatic email to experts when approved/rejected
2. **Expert Dashboard**: Separate dashboard showing application status
3. **Expert Directory**: Searchable directory of verified experts by trade/location
4. **Auto-Verification**: Integration with license verification APIs
5. **Rating System**: Allow homeowners to rate expert tips
6. **Expert Messaging**: Direct messaging between homeowners and experts
7. **Verification Levels**: Bronze/Silver/Gold based on years in business, ratings
8. **Subscription Model**: Premium expert features (featured listings, analytics)
9. **Mobile Verification**: Upload photos of licenses/certifications
10. **Background Checks**: Optional third-party background check integration

## Notes

This ADR documents the implementation completed on 2025-11-23. The system successfully:
- Created ExpertProfile model with migration 0002
- Implemented CombinedRegistrationForm with conditional validation
- Updated RegisterView to handle both account types
- Created dynamic registration template with JavaScript
- Added admin approval workflow with bulk actions
- Restricted tip creation to verified experts only
- Added verification badges throughout UI

The feature is production-ready and all tests pass. Server running on http://127.0.0.1:8080/
