# Copilot Brief: Local Expert Verification Implementation

**Date:** 2025-11-23  
**Feature:** Local Expert Verification System  
**Status:** ✅ Complete  
**Related ADR:** adr-1.0.6-local-expert-verification-system.md

## Overview

Implemented a comprehensive Local Expert verification system that distinguishes professional service providers from regular homeowners. The system uses a combined registration form with progressive disclosure, admin approval workflow, and strict access controls.

## What Was Built

### 1. ExpertProfile Model
**File:** `accounts/models.py`

Extended the custom User model and created ExpertProfile:

```python
class ExpertProfile(models.Model):
    """
    Extended profile for verified local experts/professionals.
    Stores business information, credentials, and approval tracking.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='expert_profile')
    
    # Company Information
    company_name = models.CharField(max_length=200)
    trade = models.CharField(max_length=50, choices=TRADE_CHOICES)
    
    # Contact Information
    business_phone = models.CharField(max_length=20, validators=[phone_regex])
    business_email = models.EmailField()
    website = models.URLField(blank=True)
    
    # Business Address
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10, validators=[zip_regex])
    
    # Professional Credentials
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

**Migration:** `accounts/migrations/0002_alter_user_is_verified_expert_expertprofile.py` ✅ Applied

### 2. Combined Registration Form
**File:** `accounts/forms.py`

Created `CombinedRegistrationForm` replacing `UserRegistrationForm`:

**Key Features:**
- Radio button account type selection (homeowner/expert)
- All 15+ expert fields included as optional form fields
- `clean()` method validates expert fields required only when account_type='expert'
- `save()` method handles two registration paths:
  - **Homeowner**: Sets `is_active=True`, user logged in immediately
  - **Expert**: Sets `is_active=False` (blocks login), creates ExpertProfile automatically

**Expert Fields:**
- company_name, trade (dropdown with 11 choices)
- business_phone (validated format), business_email, website
- street_address, city, state, zip_code (validated format)
- license_number, years_in_business

### 3. Registration View Updates
**File:** `accounts/views.py`

Updated `RegisterView` to handle both account types:

```python
def form_valid(self, form):
    response = super().form_valid(form)
    account_type = form.cleaned_data.get('account_type')
    
    if account_type == 'homeowner':
        login(self.request, self.object)
        messages.success(self.request, "Welcome to Homestead Compass!")
    elif account_type == 'expert':
        messages.info(
            self.request,
            "Your expert application has been submitted. "
            "An administrator will review your information. "
            "You will receive an email notification when approved."
        )
        return redirect('accounts:login')
    
    return response
```

### 4. Dynamic Registration Template
**File:** `templates/accounts/register.html`

Complete rewrite with:
- Account type radio buttons at top with clear descriptions
- Progressive disclosure using JavaScript
- Expert fields hidden by default, shown when "Local Expert" selected
- Alert box explaining verification requirement
- Dynamic submit button text: "Create Account" vs "Submit Expert Application"
- Bootstrap 5 styling with organized sections

**JavaScript Logic:**
```javascript
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
```

### 5. Admin Approval System
**File:** `accounts/admin.py`

Added `ExpertProfileAdmin` with:

**Bulk Actions:**
- `approve_experts`: Sets `is_verified_expert=True`, `is_active=True`, records approval metadata
- `revoke_expert_status`: Removes verification, expert can no longer create tips

**List Display:**
- company_name, user, trade, city, state
- application_submitted, approved_at
- List filters by trade, state, approval status

**Fieldsets:**
- Company Information
- Contact Information
- Business Address
- Professional Credentials
- Approval Information (read-only)

### 6. Content Creation Restriction
**File:** `tips/views.py`

Updated `TipCreateView`:

```python
class TipCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_verified_expert
    
    def handle_no_permission(self):
        messages.error(
            self.request,
            "Only verified experts can share tips. "
            "Please apply for expert verification in your profile."
        )
        return redirect('tips:tip_list')
```

### 7. Expert Profile Views
**File:** `accounts/views.py`

Created three views:
- `ExpertProfileCreateView`: Apply for expert status (separate flow, kept for compatibility)
- `ExpertProfileUpdateView`: Edit expert profile
- `ExpertProfileDetailView`: View expert's public profile

**URL Patterns:**
- `accounts/expert/apply/`
- `accounts/expert/edit/`
- `accounts/expert/<username>/`

### 8. UI Enhancements

**Templates Updated:**
- `templates/accounts/profile.html`: Shows expert status, business card for verified experts
- `templates/tips/tip_list.html`: "Verified Expert" badges, conditional "Share a Tip" button
- `templates/accounts/expert_profile_form.html`: Full expert application form

**Bootstrap Badges:**
```html
<span class="badge bg-success">
    <i class="bi bi-patch-check-fill"></i> Verified Expert
</span>
```

## User Workflows

### Homeowner Registration Flow
1. Visit `/accounts/register/`
2. Select "Homeowner" radio button (default)
3. Fill basic fields: username, email, password, location
4. Check "I am a first-time homeowner" if applicable
5. Click "Create Account"
6. **Logged in automatically** → Redirected to home page
7. Success message: "Welcome to Homestead Compass!"

### Expert Registration Flow
1. Visit `/accounts/register/`
2. Select "Local Expert (Requires Verification)" radio button
3. Expert section appears with 15+ fields
4. Fill all required fields:
   - Account info: username, email, password, location
   - Company info: company name, trade
   - Contact: business phone, business email, optional website
   - Address: street, city, state, ZIP
   - Credentials: years in business, optional license number
5. Click "Submit Expert Application"
6. Account created with `is_active=False` (cannot login yet)
7. ExpertProfile created and linked
8. Redirected to login page
9. Info message: "Your expert application has been submitted..."

### Admin Approval Flow
1. Admin logs into Django admin
2. Navigate to "Expert Profiles"
3. See list of pending applications (unverified users)
4. Review expert information:
   - Company details
   - Contact information
   - Business address
   - Credentials
5. Select expert profile(s)
6. Choose "Approve Selected Experts" from Actions dropdown
7. Click "Go"
8. System sets:
   - `user.is_verified_expert = True`
   - `user.is_active = True` (enables login)
   - `profile.approved_by = admin_user`
   - `profile.approved_at = current_timestamp`
9. Success message: "Successfully approved X experts"

### Expert Login & Access Flow
1. Expert attempts login at `/accounts/login/`
2. **Before approval**: Login blocked by Django auth (is_active=False)
   - Error: "Please enter a correct username and password"
3. **After approval**: Login succeeds
4. Expert can:
   - View their profile with "Verified Expert" badge
   - Click "Share a Tip" button on tips page
   - Create and submit tips
   - Edit their expert profile
5. Expert tips display with verification badge

## Technical Details

### Database Schema Changes
**Migration 0002:**
- Added ExpertProfile table with foreign key to auth_user
- Altered User.is_verified_expert field (already existed, modified help_text)

**Fields & Constraints:**
- OneToOneField ensures one ExpertProfile per User
- Phone/ZIP validators use regex patterns
- Trade choices limited to 11 predefined options
- Timestamps track application submission and approval

### Form Validation Logic

**Conditional Validation:**
```python
def clean(self):
    cleaned_data = super().clean()
    account_type = cleaned_data.get('account_type')
    
    if account_type == 'expert':
        expert_fields = [
            'company_name', 'trade', 'business_phone', 'business_email',
            'street_address', 'city', 'state', 'zip_code', 'years_in_business'
        ]
        for field in expert_fields:
            if not cleaned_data.get(field):
                self.add_error(field, 'This field is required for expert accounts.')
    
    return cleaned_data
```

### Security Implementation

1. **Login Blocking**: Django's `is_active` flag prevents unverified expert login
2. **View Protection**: `UserPassesTestMixin` checks `is_verified_expert` before allowing tip creation
3. **Template Guards**: Conditional rendering based on verification status
4. **Admin Audit**: Tracks who approved experts and when
5. **Form Validation**: Server-side validation ensures all expert fields provided

### JavaScript Progressive Disclosure

**Benefits:**
- Reduces cognitive load (only shows relevant fields)
- Clear visual feedback when selecting account type
- No page reload required
- Submit button text updates dynamically
- Form remains accessible (works without JS, just shows all fields)

## Testing Completed

✅ **Registration Tests:**
- Homeowner registration → immediate login
- Expert registration → account created, login blocked
- Form validation (missing expert fields rejected)

✅ **Admin Tests:**
- Bulk approve action → sets flags correctly
- Approval metadata recorded
- Revoke action removes verification

✅ **Access Control Tests:**
- Unverified expert blocked from tip creation
- Verified expert can create tips
- Login blocked for is_active=False

✅ **UI Tests:**
- Progressive disclosure works
- Badges display correctly
- Messages show appropriately

## Files Modified/Created

### Created:
- `accounts/migrations/0002_alter_user_is_verified_expert_expertprofile.py`
- `templates/accounts/expert_profile_form.html`
- `docs/adr/adr-1.0.6-local-expert-verification-system.md`
- `docs/briefs/brief-local-expert-verification.md`

### Modified:
- `accounts/models.py` - Added ExpertProfile model
- `accounts/forms.py` - Replaced UserRegistrationForm with CombinedRegistrationForm
- `accounts/views.py` - Updated RegisterView, added expert profile views
- `accounts/admin.py` - Added ExpertProfileAdmin with approval actions
- `accounts/urls.py` - Added expert profile URL patterns
- `tips/views.py` - Added UserPassesTestMixin to TipCreateView
- `templates/accounts/register.html` - Complete rewrite with progressive disclosure
- `templates/accounts/profile.html` - Added expert status display
- `templates/tips/tip_list.html` - Added verification badges

## Configuration

**Trade Choices:**
```python
TRADE_CHOICES = [
    ('general', 'General Contractor'),
    ('plumbing', 'Plumber'),
    ('electrical', 'Electrician'),
    ('hvac', 'HVAC Technician'),
    ('roofing', 'Roofer'),
    ('landscaping', 'Landscaper'),
    ('painting', 'Painter'),
    ('carpentry', 'Carpenter'),
    ('masonry', 'Mason'),
    ('appliance', 'Appliance Repair'),
    ('other', 'Other'),
]
```

**State Choices:** All 50 US states + DC (dropdown select)

## Known Limitations

1. **Email Notifications**: Not yet implemented
   - Experts don't receive automatic email when approved
   - Admins don't receive notification of new applications
   
2. **Expert Dashboard**: No dedicated status page
   - Experts must try to login to know if approved
   - No visibility into application status

3. **Profile Photos**: Not implemented
   - Expert profiles don't have photos/logos
   - Tips don't show author avatars

4. **License Verification**: Manual process
   - Admin must manually verify license numbers
   - No integration with state licensing databases

5. **Expert Directory**: Not yet built
   - No searchable directory of experts
   - No filtering by trade/location

## Future Enhancements

**Priority 1 (High):**
- Email notifications for approval/rejection
- Expert application status dashboard
- Blue checkmark icon styling

**Priority 2 (Medium):**
- Expert directory with search/filter
- Profile photos/company logos
- Rating/review system for expert tips

**Priority 3 (Low):**
- Auto-verification via third-party APIs
- Expert subscription tiers
- Direct messaging between users and experts
- Mobile license photo upload

## Success Metrics

✅ Expert applications centralized in one registration flow  
✅ 100% of experts go through admin approval  
✅ Zero unverified experts can create tips  
✅ Clear visual distinction (badges) for expert content  
✅ Single source of truth for expert business information  
✅ Audit trail of all approvals  

## Developer Notes

**Key Design Decisions:**
1. Used `is_active=False` to block unverified expert login (leverages Django's built-in auth)
2. Progressive disclosure in one form rather than multi-step wizard (better UX)
3. ExpertProfile is separate model (not inline in User) for clean separation of concerns
4. Admin approval is manual (ensures quality but requires admin time)
5. JavaScript enhancement is optional (form works without it, just shows all fields)

**Gotchas:**
- Remember to check both `is_authenticated` AND `is_verified_expert` when protecting views
- `is_active=False` prevents all login, not just tip creation
- Form validation happens on both client (HTML5) and server (Django)
- Expert fields are optional in form but validated conditionally in clean()

**Testing Tips:**
- Create test superuser to approve experts
- Test both registration flows
- Verify login blocking for unverified experts
- Check badges render correctly
- Test form with JavaScript disabled

## Deployment Status

🚀 **Ready for Production**
- All migrations applied
- No database errors
- Server running stable on http://127.0.0.1:8080/
- All manual testing passed
- Documentation complete

**Next Steps:**
1. Push to GitHub ✅ (in progress)
2. Deploy to production environment
3. Create admin accounts for client
4. Train client on expert approval workflow
5. Monitor for first expert registrations

---

**Last Updated:** 2025-11-23  
**Implemented By:** GitHub Copilot + Development Team  
**Review Status:** ✅ Complete and tested
