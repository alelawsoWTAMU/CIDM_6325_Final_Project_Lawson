# BRIEF: Build Community Tips Module with Moderation

## Goal

- Implement community-driven localized tips module with content moderation addressing PRD §4 F-003, F-004 and FR-F-003-1 through FR-F-004-4.

## Scope (single PR)

- **Files to touch**:
  - `tips/models.py`: LocalTip, TipComment, TipReport models with status workflow
  - `tips/views.py`: CRUD views for tips, upvote view, comment submission, report submission
  - `tips/forms.py`: LocalTipForm with auto-slugification, TipCommentForm, TipReportForm
  - `tips/admin.py`: Custom admin with bulk approve/reject/flag actions
  - `templates/tips/`: All tip-related templates with disclaimer
  - `tips/urls.py`: URL patterns for tip browsing, submission, upvoting, commenting, reporting

- **Non-goals**: 
  - Email notifications for tip approval/rejection (deferred to v1.1)
  - Reputation system or user badges (deferred to v1.2)
  - Image uploads for tips (deferred to v1.2)
  - Advanced search with full-text indexing (deferred to v1.1)

## Standards

- **Commits**: Conventional style (feat/fix/docs/refactor/chore)
  - Example: `feat(tips): add LocalTip model with moderation workflow`
  - Example: `feat(tips): implement upvote functionality with duplicate prevention`
  - Example: `feat(tips): add admin bulk actions for content moderation`
- **No secrets**: All configuration via `settings.py` or environment variables
- **Django tests**: Use unittest/Django TestCase (no pytest)
  - Test tip submission creates pending status
  - Test upvote functionality prevents duplicates
  - Test bulk moderation actions in admin
  - Test report submission workflow
  - Test visibility of approved vs pending tips

## Acceptance

- **User flow for tip submission**:
  1. Authenticated user navigates to "Community Tips"
  2. User clicks "Share a Tip" button
  3. User fills form: title, content (Markdown supported), category, location (city/region)
  4. User submits form
  5. System creates LocalTip with status="pending"
  6. User sees success message: "Your tip has been submitted and is awaiting moderation"

- **User flow for upvoting**:
  1. User browses approved tips
  2. User clicks upvote icon on tip
  3. System adds user to tip.upvoted_by ManyToMany field
  4. System increments upvote count display
  5. Subsequent clicks toggle upvote (remove from ManyToMany)

- **Admin flow for moderation**:
  1. Moderator logs into admin interface
  2. Moderator navigates to "Local tips"
  3. Moderator filters by status="pending"
  4. Moderator selects multiple tips via checkboxes
  5. Moderator selects bulk action: "Approve selected tips"
  6. System updates status="approved" for all selected tips
  7. Tips become visible to public users

- **Include migration?**: Yes
  - Migration for LocalTip, TipComment, TipReport models
  - Migration for upvoted_by ManyToMany relationship

- **Update docs & PR checklist**:
  - Update README.md with community tips feature description
  - Add to PROJECT_SUMMARY.md completion checklist
  - Document moderation workflow in admin documentation
  - Include disclaimer language in legal documentation

## Prompts for Copilot

- "Generate Django models for a community tips system with moderation workflow. Include LocalTip model with status choices (pending/approved/rejected/flagged), ManyToMany upvotes, view count tracking, TipComment model for threaded comments, and TipReport model for user-submitted reports."

- "Generate Django admin customization for LocalTip model with bulk actions to approve, reject, and flag multiple tips simultaneously. Include list_filter for status, list_display for key fields, and search_fields for title and content."

- "Create Django view for upvoting tips that prevents duplicate votes from same user. Use ManyToMany relationship to track which users have upvoted. Return JSON response for AJAX requests with updated upvote count."

- "Explain the moderation workflow: How does content flow from pending to approved? What safety checks prevent bad advice from reaching users? How does the disclaimer protect against liability?"

- "Refactor tip upvoting logic into a reusable method on LocalTip model that handles duplicate prevention and count updates. Show diff-ready patch."

---

**Related ADR**: None (functionality driven directly by PRD)  
**PRD Reference**: §4 F-003, F-004; §5 FR-F-003-1 through FR-F-004-4
