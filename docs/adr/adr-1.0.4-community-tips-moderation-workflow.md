# ADR-1.0.4 Community Tips Moderation Workflow

Date: 2025-11-23  
Status: Accepted  
Version: 1.0  
Authors: Alexander J Lawson  
Reviewers: GitHub Copilot (Claude Sonnet 4.5)  
Supersedes or amends: —

---

## Links and traceability

PRD link: docs/prd/home_maintenance_compass_prd_v1.0.1.md#4-scope-items-and-checklist-seeds (F-003, F-004) · docs/prd/home_maintenance_compass_prd_v1.0.1.md#5-functional-requirements-bound-to-scope (FR-F-004-1, FR-F-004-2, FR-F-004-3, FR-F-004-4)  
Scope IDs from PRD: F-003 (Localized Community Tips Module), F-004 (Content Moderation System)  
Functional requirements: FR-F-004-1 (pending status), FR-F-004-2 (bulk actions), FR-F-004-3 (user reporting), FR-F-004-4 (disclaimer)  
Related issues or PRs: Tips app moderation implementation

---

## Intent and scope

Define the content moderation workflow for user-submitted community tips to ensure quality advice and mitigate legal liability from crowd-sourced content.

**In scope**: Moderation status workflow, admin bulk actions, user reporting mechanism, disclaimer requirements  
**Out of scope**: Automated content filtering (ML-based spam detection deferred to v2.0), reputation systems (deferred to v1.2), tip rewards/gamification (deferred to v2.0)

---

## Problem and forces

### Problem Statement
Per PRD §5 Edge Case B: "John Doe II is an inexperienced new homeowner who attempts to use the app to solve his leaky faucet problem. Using the Localized Tips Module, he sees a DIY suggestion with a lot of upvotes, which makes him feel secure in trying it for himself. During the repair, something breaks (a burst pipe perhaps) which leads to substantial and expensive water damage."

This scenario illustrates the critical risk: **crowd-sourced home maintenance advice can cause property damage or personal injury if incorrect**. The application must balance community knowledge sharing with quality control and legal liability protection.

### Forces
- **Liability Risk**: Incorrect DIY advice could cause property damage, injury, or financial loss
- **Content Quality**: Bad advice undermines user trust and app credibility
- **Community Engagement**: Overly restrictive moderation discourages participation
- **Moderator Workload**: Manual review of every tip doesn't scale
- **Legal Protection**: Need "bulletproof" disclaimer per PRD §9 (Risks & Assumptions)
- **User Safety**: First-time homeowners may lack judgment to identify bad advice

### Constraints
- Must comply with user-generated content laws and liability standards
- Moderators are not guaranteed to be licensed professionals
- Cannot completely prevent bad advice from being submitted
- Must maintain fast submission-to-approval turnaround (target: <24 hours) to keep community engaged
- Must use Django admin interface per project standards (no custom moderation UI for MVP)

---

## Options considered

### Option A: No Moderation (Immediate Publication)
**Approach**: All submitted tips immediately visible to all users

**Pros**:
- Zero moderator workload
- Instant community gratification
- Maximum engagement and participation

**Cons**:
- Significant legal liability exposure
- No quality control (spam, dangerous advice, misinformation)
- Fails PRD FR-F-004-1 requirement
- Unacceptable risk per PRD §9 (Edge Case B)

**PRD Alignment**: Explicitly rejected in PRD §9 (Risks: Legal liability)

**Verdict**: Rejected - unacceptable legal and safety risk

---

### Option B: Post-Publication Moderation (Publish Then Review)
**Approach**: Tips publish immediately but moderators review and can unpublish

**Pros**:
- Faster community engagement (no submission delay)
- Moderators can focus on reported content
- Reduces moderator workload (only review flagged tips)

**Cons**:
- Bad advice reaches users before removal
- Liability window exists between publication and moderation
- Reactive rather than proactive quality control
- Users may act on advice before it's removed

**PRD Alignment**: Partially meets requirements but fails FR-F-004-1 (pending status before visibility)

**Verdict**: Rejected - insufficient liability protection

---

### Option C: Pre-Publication Moderation (Approve Before Publish)
**Approach**: All tips enter "pending" status and require moderator approval before public visibility

```python
class LocalTip(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('flagged', 'Flagged for Review'),
    ]
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
```

**Workflow**:
1. User submits tip → status='pending'
2. Tip NOT visible in public tip list (filtered by status='approved')
3. Moderator reviews pending tips in admin
4. Moderator approves/rejects/flags tip
5. If approved → status='approved' → tip becomes visible

**Pros**:
- Proactive quality control (bad advice never reaches users)
- Meets FR-F-004-1 (pending status requirement)
- Clear liability protection (no advice published without review)
- Aligns with PRD risk mitigation strategy
- Standard moderation pattern (used by forums, comment systems)

**Cons**:
- Delay between submission and publication (user must wait for approval)
- Requires moderator capacity (all tips must be reviewed)
- Risk of bottleneck if moderator team is small

**PRD Alignment**: Directly implements FR-F-004-1, supports PRD §9 liability mitigation

**Verdict**: Selected - best balance of quality control and liability protection

---

### Option D: Hybrid Moderation (Trusted Users Skip Review)
**Approach**: Pre-publication moderation for new users; auto-approve for verified experts

**Pros**:
- Reduces moderator workload (verified experts skip review)
- Rewards community contributors
- Faster publication for quality contributors

**Cons**:
- Complexity in determining "trusted user" status
- Even experts can make mistakes
- Creates two-tier system (potential resentment)
- Still carries liability risk for auto-approved content

**PRD Alignment**: Aligns with expert_verified field from custom User model, but increases complexity

**Verdict**: Deferred to v1.2 - adds complexity beyond MVP requirements

---

## Decision

**We choose Option C: Pre-Publication Moderation with Bulk Actions**

### Decision Drivers (Ranked)
1. **Legal Liability Protection**: No bad advice reaches users without moderator review
2. **PRD Compliance**: Directly implements FR-F-004-1 (pending status), FR-F-004-2 (bulk actions)
3. **User Safety**: Proactive quality control protects first-time homeowners from dangerous advice
4. **Standard Pattern**: Well-understood moderation workflow used by established platforms
5. **Admin Integration**: Leverages Django admin bulk actions (no custom UI needed)

### Rationale
Pre-publication moderation provides the strongest liability protection while meeting all PRD requirements. The moderator workload concern is mitigated by bulk actions (approve 10+ tips simultaneously) and can be further addressed in v1.2 with automated spam filtering.

---

## Consequences

### Positive

**Liability Protection**:
- No user-generated advice reaches public without human review
- Moderators can reject dangerous or incorrect advice before publication
- Creates audit trail (who approved what, when)

**Quality Assurance**:
- Moderators can enforce quality standards (clear writing, specific details, safety notes)
- Can reject spam, low-effort, or duplicate tips
- Can request revisions before approval (via rejection with feedback)

**Admin Bulk Actions**:
```python
# tips/admin.py
@admin.register(LocalTip)
class LocalTipAdmin(admin.ModelAdmin):
    actions = ['approve_tips', 'reject_tips', 'flag_tips']
    list_filter = ('status', 'category', 'created_at')
    
    def approve_tips(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} tips have been approved.')
    
    def reject_tips(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} tips have been rejected.')
    
    def flag_tips(self, request, queryset):
        updated = queryset.update(status='flagged')
        self.message_user(request, f'{updated} tips have been flagged for review.')
```

**User Reporting**:
```python
# Users can report approved tips for re-review
class TipReport(models.Model):
    tip = models.ForeignKey(LocalTip, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

**Disclaimer Integration**:
All tip display templates include prominent disclaimer per FR-F-004-4:
```html
<!-- templates/tips/tip_detail.html -->
<div class="alert alert-warning">
    <strong>⚠️ Safety Notice:</strong> Tips are user-generated content. 
    Always consult a licensed professional before performing home repairs 
    or maintenance tasks. Use this information at your own risk.
</div>
```

### Negative and Risks

**Submission Delay**:
- Users must wait for moderator approval before tip becomes visible
- Risk of user frustration if approval takes >24 hours
- **Mitigation**: Set moderator SLA (review within 24 hours), provide user feedback ("Your tip is pending review"), display estimated review time

**Moderator Bottleneck**:
- Small moderator team could create approval backlog
- **Mitigation**: 
  - Implement bulk actions (approve 10+ tips at once)
  - Add multiple moderators to team
  - v1.2: Add automated spam filtering to reduce workload
  - v2.0: Implement trusted user program (verified experts skip review)

**Moderator Error**:
- Moderators might approve incorrect advice or reject good advice
- **Mitigation**:
  - Provide moderator training and guidelines
  - Document moderation criteria
  - Implement flagging system (users can report approved tips)
  - Multiple moderators can review flagged tips

**Liability Still Exists**:
- Even with moderation, incorrect advice might slip through
- Moderators are not guaranteed to be licensed professionals
- **Mitigation**:
  - Prominent disclaimer on all tip pages per FR-F-004-4
  - Terms of service with liability waiver
  - Professional liability insurance (business decision)
  - Document that moderators use "reasonable care" standard

---

## Implementation notes

### Status Workflow State Machine
```
                    ┌─────────┐
                    │ Pending │ (initial state)
                    └────┬────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
     ┌─────────┐   ┌─────────┐   ┌─────────┐
     │Approved │   │Rejected │   │ Flagged │
     └────┬────┘   └─────────┘   └────┬────┘
          │                            │
          │         ┌─────────┐        │
          └────────►│ Flagged │◄───────┘
                    └────┬────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
     ┌─────────┐   ┌─────────┐   ┌─────────┐
     │Approved │   │Rejected │   │ Pending │
     └─────────┘   └─────────┘   └─────────┘
```

### Model Implementation
```python
# tips/models.py
from django.db import models
from django.conf import settings

class LocalTip(models.Model):
    """Community-submitted home maintenance tip with moderation."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('flagged', 'Flagged for Review'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    content = models.TextField()
    category = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submitted_tips'
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Moderation status - pending tips are not visible to public"
    )
    
    upvoted_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='upvoted_tips',
        blank=True
    )
    
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def increment_views(self):
        """Increment view count (call in DetailView)."""
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['category', 'status']),
        ]

class TipReport(models.Model):
    """User-submitted report for problematic tips."""
    
    REASON_CHOICES = [
        ('incorrect', 'Incorrect or Dangerous Advice'),
        ('spam', 'Spam or Advertisement'),
        ('offensive', 'Offensive Content'),
        ('duplicate', 'Duplicate Tip'),
        ('other', 'Other (explain in details)'),
    ]
    
    tip = models.ForeignKey(
        LocalTip,
        on_delete=models.CASCADE,
        related_name='reports'
    )
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = [['tip', 'reported_by']]  # One report per user per tip
```

### View Filtering
```python
# tips/views.py
class TipListView(ListView):
    """Display approved tips only."""
    model = LocalTip
    template_name = 'tips/tip_list.html'
    context_object_name = 'tips'
    paginate_by = 20
    
    def get_queryset(self):
        # Only show approved tips to public
        return LocalTip.objects.filter(status='approved').order_by('-created_at')
```

### Admin Configuration
```python
# tips/admin.py
from django.contrib import admin
from .models import LocalTip, TipReport

@admin.register(LocalTip)
class LocalTipAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'category', 'location', 
                    'upvote_count', 'view_count', 'created_at')
    list_filter = ('status', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'author__username', 'location')
    readonly_fields = ('created_at', 'updated_at', 'view_count', 'slug')
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'category')
        }),
        ('Metadata', {
            'fields': ('author', 'location', 'status')
        }),
        ('Engagement', {
            'fields': ('view_count', 'upvoted_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_tips', 'reject_tips', 'flag_tips']
    
    def approve_tips(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f'{updated} tips have been approved.')
    approve_tips.short_description = "Approve selected tips"
    
    def reject_tips(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} tips have been rejected.')
    reject_tips.short_description = "Reject selected tips"
    
    def flag_tips(self, request, queryset):
        updated = queryset.update(status='flagged')
        self.message_user(request, f'{updated} tips have been flagged for review.')
    flag_tips.short_description = "Flag selected tips for review"
    
    def upvote_count(self, obj):
        return obj.upvoted_by.count()
    upvote_count.short_description = 'Upvotes'

@admin.register(TipReport)
class TipReportAdmin(admin.ModelAdmin):
    list_display = ('tip', 'reported_by', 'reason', 'created_at')
    list_filter = ('reason', 'created_at')
    search_fields = ('tip__title', 'reported_by__username', 'details')
    readonly_fields = ('created_at',)
```

### Disclaimer Template
```html
<!-- templates/tips/disclaimer.html -->
<div class="alert alert-warning border-warning" role="alert">
    <h5 class="alert-heading">
        <i class="bi bi-exclamation-triangle-fill"></i> 
        Important Safety Notice
    </h5>
    <p class="mb-0">
        <strong>Tips are user-generated content.</strong> While we moderate 
        submissions for quality, we cannot guarantee the accuracy or safety of 
        all advice. <strong>Always consult a licensed professional</strong> 
        before performing home repairs or maintenance tasks. Use this 
        information at your own risk.
    </p>
</div>

<!-- Include in all tip templates -->
{% include 'tips/disclaimer.html' %}
```

---

## Future enhancements

### v1.2: Automated Spam Filtering
Pre-filter obvious spam before moderator review:
```python
# Simple keyword-based spam detection
spam_keywords = ['buy now', 'click here', 'guaranteed results']
if any(keyword in tip.content.lower() for keyword in spam_keywords):
    tip.status = 'flagged'  # Auto-flag for moderator review
```

### v1.2: Trusted User Program
Verified experts skip moderation queue:
```python
def save(self, *args, **kwargs):
    if self.author.expert_verified:
        self.status = 'approved'  # Auto-approve verified experts
    super().save(*args, **kwargs)
```

### v2.0: Machine Learning Content Quality
Train ML model on approved/rejected tips to predict quality:
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Train on historical moderation decisions
# Flag low-quality tips for moderator attention
```

---

## Related decisions

- ADR-1.0.0: Application Architecture (defines tips app boundary)
- ADR-1.0.1: Custom User Model (expert_verified field supports moderation)
- ADR-1.0.2: Core Data Models (LocalTip, TipReport relationships)

---

## References

- PRD Section 5: FR-F-004-1, FR-F-004-2, FR-F-004-3, FR-F-004-4
- PRD Section 9: Risks & Assumptions (Legal liability mitigation)
- PRD Section 5: Edge Case B (DIY advice causing damage)
- Django Admin Actions Documentation
- User-Generated Content Liability Law (Section 230, CDA)
- Content Moderation Best Practices

---

## Revision history

- 2025-11-23: v1.0 Initial version - accepted
