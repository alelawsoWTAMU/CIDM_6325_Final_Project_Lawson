# ADR-1.0.1 Custom User Model Implementation

Date: 2025-11-23  
Status: Accepted  
Version: 1.0  
Authors: Alexander J Lawson  
Reviewers: GitHub Copilot (Claude Sonnet 4.5)  
Supersedes or amends: —

---

## Links and traceability

PRD link: docs/prd/home_maintenance_compass_prd_v1.0.1.md#5-functional-requirements-bound-to-scope (User authentication requirements)  
Scope IDs from PRD: F-003, F-004, F-005, F-006 (all require user authentication)  
Functional requirements: Implicit authentication requirement for all user-facing features  
Related issues or PRs: Initial accounts app implementation

---

## Intent and scope

Define the user authentication model to support homeowner-specific attributes and enable future extensibility without complex migrations.

**In scope**: Custom User model extending AbstractUser, homeowner-specific fields, expert verification workflow  
**Out of scope**: Social authentication (OAuth), multi-factor authentication (deferred to v1.2), profile photos (requires Pillow, deferred to v1.2)

---

## Problem and forces

### Problem Statement
The application targets first-time homeowners and local experts. Django's default User model (username, email, password, first_name, last_name) lacks fields for:
- Identifying first-time homeowner status (affects onboarding UX)
- Marking users as local experts (affects tip credibility)
- Verifying expert credentials (moderation requirement)
- Storing location for tip filtering
- Providing user bio for community trust-building

Django best practice mandates using a custom user model from project inception because migrating later is extremely difficult.

### Forces
- **Extensibility**: Need flexibility to add fields without painful migrations
- **Django Best Practice**: Official Django documentation strongly recommends custom user model even if not immediately needed
- **Homeowner Context**: First-time homeowner flag enables targeted tips and onboarding flows
- **Expert Verification**: Community tips quality depends on verified expert contributors
- **Privacy**: Location data should be optional and user-controlled
- **Academic Context**: Demonstrates understanding of Django authentication patterns per rubric

### Constraints
- Must use Django's built-in authentication system per course requirements
- Must be decided before first migration (cannot change easily after)
- Must maintain compatibility with Django admin, LoginRequiredMixin, authentication middleware
- Cannot add image uploads without Pillow package (not in requirements)

---

## Options considered

### Option A: Django Default User Model
**Approach**: Use `django.contrib.auth.models.User` without modification

**Pros**:
- Zero configuration required
- Familiar to all Django developers
- All Django packages assume this structure

**Cons**:
- Cannot add homeowner-specific fields directly to User model
- Requires OneToOne UserProfile model for extensions (anti-pattern when known from start)
- Changing to custom user later requires complex data migrations and risk
- Does not support future extensibility (v1.1, v2.0 features)
- Fails to demonstrate Django best practices for academic context

**PRD Alignment**: Insufficient for F-003 (community members have expertise levels), F-004 (expert verification needed)

**Verdict**: Rejected - fails extensibility and best practices requirements

---

### Option B: Custom User Model Extending AbstractUser
**Approach**: Create `accounts.User` extending `AbstractUser`, add homeowner-specific fields

```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_first_time_homeowner = models.BooleanField(default=False)
    is_expert = models.BooleanField(default=False)
    expert_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
```

Configure in settings:
```python
AUTH_USER_MODEL = 'accounts.User'
```

**Pros**:
- Maintains all default Django authentication functionality (username, email, password, staff, superuser)
- Adds homeowner-specific fields directly on User model (no joins needed)
- Django best practice per official documentation
- Enables future field additions without major migrations
- Supports expert verification workflow for tip moderation
- Demonstrates understanding of Django authentication for academic evaluation

**Cons**:
- Must be configured before first migration (irreversible after)
- All Django authentication references must use `settings.AUTH_USER_MODEL` or `get_user_model()`
- Requires updating admin interface to handle custom fields

**PRD Alignment**: Directly supports F-003 (expert contributors), F-004 (verification workflow), future v1.1/v2.0 features

**Verdict**: Selected - aligns with Django best practices and PRD requirements

---

### Option C: Custom User Model Extending AbstractBaseUser
**Approach**: Build completely custom user model from AbstractBaseUser (email-based login, custom fields)

**Pros**:
- Maximum flexibility
- Can use email instead of username for login
- Complete control over authentication fields

**Cons**:
- Must manually implement all authentication functionality (permissions, groups, admin)
- Significant development time for marginal benefit
- Increased complexity for academic project
- Overkill for requirements (username login is acceptable)

**PRD Alignment**: Over-engineered; no PRD requirement justifies this complexity

**Verdict**: Rejected - unnecessary complexity

---

## Decision

**We choose Option B: Custom User Model Extending AbstractUser**

### Decision Drivers (Ranked)
1. **Django Best Practice**: Official documentation strongly recommends custom user model from project start
2. **Extensibility**: Supports v1.1 and v2.0 feature additions without complex migrations
3. **PRD Requirements**: Directly supports expert verification (F-004) and homeowner targeting
4. **Academic Demonstration**: Shows understanding of Django authentication patterns per rubric
5. **Maintainability**: Simpler than OneToOne profile pattern; fewer queries for user attributes

### Rationale
Using AbstractUser provides all Django authentication features while enabling homeowner-specific extensions. The decision must be made before first migration per Django constraints, and the PRD clearly indicates need for user differentiation (first-time homeowners vs. experts).

---

## Consequences

### Positive

**Future-Proof Architecture**:
- Can add fields (e.g., `phone_number`, `preferred_notification_method`) in future versions without major migrations
- Supports v1.1 email notifications (add `email_verified` field)
- Supports v2.0 reputation system (add `reputation_score` field)

**Simplified Queries**:
```python
# No join needed - all user data in one table
user = User.objects.get(username='john')
if user.is_expert and user.expert_verified:
    # Show "Verified Expert" badge
```

**Expert Verification Workflow**:
```python
# Tips from verified experts get priority in sorting
verified_expert_tips = LocalTip.objects.filter(
    author__is_expert=True,
    author__expert_verified=True
)
```

**Homeowner Onboarding**:
```python
# Target first-time homeowner welcome flow
if request.user.is_first_time_homeowner:
    # Show beginner-friendly tips and tutorials
```

### Negative and Risks

**Pre-Migration Requirement**:
- Must be configured before `python manage.py migrate` runs for the first time
- Changing AUTH_USER_MODEL after migrations is extremely difficult (requires manual database surgery)
- **Mitigation**: Documented in README.md setup instructions; verified during initial implementation

**Reference Updates Required**:
- All ForeignKey references to User must use `settings.AUTH_USER_MODEL`
- All code retrieving User must use `get_user_model()`
- **Mitigation**: Consistent pattern enforced during development; documented in implementation notes

**Admin Customization Needed**:
- Must create custom UserAdmin to handle additional fields
- **Mitigation**: Implemented in `accounts/admin.py` with proper fieldsets

---

## Implementation notes

### Settings Configuration
```python
# home_maintenance_compass/settings.py
AUTH_USER_MODEL = 'accounts.User'
```

### Model Definition
```python
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model for Home Maintenance Compass.
    
    Extends Django's AbstractUser to add homeowner-specific fields:
    - bio: User biography for community credibility
    - location: Geographic location for tip filtering
    - is_first_time_homeowner: Flag for targeted onboarding
    - is_expert: User claims local expertise
    - expert_verified: Admin has verified expert credentials
    """
    bio = models.TextField(
        max_length=500, 
        blank=True,
        help_text="Tell the community about your home maintenance experience"
    )
    location = models.CharField(
        max_length=100, 
        blank=True,
        help_text="City or region (for localized tips)"
    )
    is_first_time_homeowner = models.BooleanField(
        default=False,
        help_text="Check if this is your first home"
    )
    is_expert = models.BooleanField(
        default=False,
        help_text="User claims to be a local home maintenance expert"
    )
    expert_verified = models.BooleanField(
        default=False,
        help_text="Admin has verified expert credentials"
    )
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
```

### Foreign Key References
```python
# homes/models.py
from django.conf import settings

class Home(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ✅ Correct
        on_delete=models.CASCADE,
        related_name='homes'
    )

# ❌ Incorrect - do not hardcode User model
# owner = models.ForeignKey('auth.User', ...)
```

### Getting User Model in Code
```python
# views.py or anywhere needing User model
from django.contrib.auth import get_user_model

User = get_user_model()

# Now use User as normal
new_user = User.objects.create_user(username='john', password='secure123')
```

### Admin Configuration
```python
# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model with homeowner fields."""
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Homeowner Information', {
            'fields': ('bio', 'location', 'is_first_time_homeowner')
        }),
        ('Expert Verification', {
            'fields': ('is_expert', 'expert_verified')
        }),
    )
    
    list_display = ['username', 'email', 'is_first_time_homeowner', 
                    'is_expert', 'expert_verified', 'is_staff']
    list_filter = BaseUserAdmin.list_filter + (
        'is_first_time_homeowner', 'is_expert', 'expert_verified'
    )
```

### Registration Form Example
```python
# accounts/forms.py
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'location', 'is_first_time_homeowner', 'bio']
    
    def clean_password2(self):
        # Verify passwords match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
```

---

## Related decisions

- ADR-1.0.0: Application Architecture (defines accounts app boundary)
- ADR-1.0.3: Authentication and Authorization Strategy (uses this User model)
- ADR-1.0.4: Community Tips Moderation (uses expert_verified field)

---

## References

- Django Documentation: Customizing authentication (https://docs.djangoproject.com/en/5.0/topics/auth/customizing/)
- Django Documentation: Substituting a custom User model (https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#substituting-a-custom-user-model)
- Two Scoops of Django: Chapter on Authentication
- Matt Layman, "Understand Django" - Authentication chapter
- PRD Section 5 (Functional Requirements) - User authentication implicit in all features

---

## Revision history

- 2025-11-23: v1.0 Initial version - accepted
