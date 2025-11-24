# BRIEF: Implement Expert Blog Posts Feature

**Goal**: Implement comprehensive blog CMS for verified experts to publish longer-form educational content

**Scope (Single Feature)**:
- Create BlogPost and BlogComment models with rich text support
- Implement 9 views for CRUD operations and engagement
- Add django-ckeditor for WYSIWYG editing
- Create approval workflow (draft → pending → approved/rejected)
- Build frontend templates with featured posts carousel
- Add upvoting, commenting, and view tracking

**Standards**:
- Commits: Conventional style (feat/fix/docs)
- Django CBVs: LoginRequiredMixin, UserPassesTestMixin for permissions
- Bootstrap 5 for styling consistency
- No secrets; CKEditor config in settings.py

**Files to Touch**:
- `tips/models.py` - Add BlogPost, BlogComment models
- `tips/views.py` - Add 9 blog-related CBVs
- `tips/forms.py` - Add BlogPostForm, BlogCommentForm
- `tips/urls.py` - Add 9 blog URL patterns
- `tips/admin.py` - Add BlogPostAdmin with bulk actions
- `templates/tips/blog_*.html` - Create 5 blog templates
- `templates/base.html` - Add "Expert Blog" navigation link
- `home_maintenance_compass/settings.py` - Add ckeditor to INSTALLED_APPS, configure CKEDITOR_CONFIGS
- `requirements.txt` - Add django-ckeditor, Pillow

**Non-Goals**:
- Email notifications (future enhancement)
- Social media sharing buttons
- RSS feed generation
- Advanced analytics dashboard

**Acceptance Criteria**:

1. **Model Implementation**:
   - [x] BlogPost model with RichTextField content
   - [x] Status choices: draft, pending, approved, rejected
   - [x] Featured_image ImageField with Pillow support
   - [x] ManyToMany upvotes relationship
   - [x] Tags as comma-separated CharField
   - [x] BlogComment model with ForeignKey to BlogPost

2. **Rich Text Editor**:
   - [x] django-ckeditor 6.7.3 installed
   - [x] CKEditor toolbar configured in settings.py
   - [x] WYSIWYG editor appears in blog form
   - [x] Bold, italic, lists, links, blockquote support

3. **Views & URLs**:
   - [x] BlogListView with featured posts section
   - [x] BlogDetailView with view count increment
   - [x] BlogCreateView (expert-only with UserPassesTestMixin)
   - [x] BlogUpdateView (author-only)
   - [x] BlogDeleteView with confirmation
   - [x] BlogMyPostsView showing expert's posts by status
   - [x] BlogUpvoteView toggle functionality
   - [x] BlogCommentCreateView and BlogCommentDeleteView

4. **Templates**:
   - [x] blog_list.html with featured carousel and filters
   - [x] blog_detail.html with article content and comments
   - [x] blog_form.html with CKEditor integration
   - [x] blog_confirm_delete.html
   - [x] Navigation link in base.html

5. **Approval Workflow**:
   - [x] Draft status for work-in-progress
   - [x] Pending status triggers admin review
   - [x] Admin bulk actions: approve, reject, feature
   - [x] Moderation notes field for feedback
   - [x] Only approved posts visible to public

6. **Engagement Features**:
   - [x] Upvote toggle (login required)
   - [x] get_upvote_count() method (not @property to avoid conflicts)
   - [x] Comment system with author attribution
   - [x] View count tracking
   - [x] Reading time calculation (word_count / 200)

7. **Filtering & Search**:
   - [x] Filter by category
   - [x] Search by title/content
   - [x] Sort by: popular, recent, most-viewed
   - [x] Pagination (paginate_by=10)

8. **Admin Interface**:
   - [x] BlogPostAdmin with list_display showing status, featured, upvotes, views
   - [x] list_filter: status, category, is_featured, author
   - [x] search_fields: title, content, excerpt, author__username
   - [x] Bulk actions for moderation
   - [x] Readonly fields: timestamps, get_upvote_count, view_count

**Migrations**:
- [x] Create migration 0004 for BlogPost and BlogComment
- [x] Run makemigrations && migrate successfully
- [x] Verify tables created with proper indexes

**Documentation**:
- [x] Update TODO.md marking Expert Blog Posts COMPLETE
- [x] Create ADR-1.0.7-expert-blog-posts-cms.md
- [x] Update AI_USAGE_DISCLOSURE.md with blog implementation details
- [x] Update README.md with blog feature description

**Prompts for Copilot**:

1. **Initial Setup**:
   - "Install django-ckeditor and Pillow, add to settings.INSTALLED_APPS"
   - "Generate BlogPost model with RichTextField, featured_image, status workflow"
   - "Configure CKEDITOR_CONFIGS with custom toolbar"

2. **Views Implementation**:
   - "Create BlogListView with featured posts carousel and filtering"
   - "Generate BlogCreateView with UserPassesTestMixin for experts only"
   - "Implement BlogUpvoteView toggle with redirect to detail page"
   - "Build BlogMyPostsView showing expert's posts grouped by status"

3. **Templates**:
   - "Create blog_list.html with Bootstrap 5 carousel for featured posts"
   - "Generate blog_detail.html with CKEditor content rendering and comment form"
   - "Build blog_form.html with CKEditor widget integration"

4. **Bug Fixes**:
   - "Fix TemplateSyntaxError: Cannot parse 'blog_post.tags.split:',''"
   - "Change @property upvote_count to method get_upvote_count() to avoid annotation conflict"
   - "Fix Featured Articles text color - change to white for readability"

5. **Testing**:
   - "Create 4 sample blog posts with 2 featured (HVAC guide, Safety devices)"
   - "Test expert-only creation restriction"
   - "Verify approval workflow from draft to approved"
   - "Test upvote toggle and comment creation"

**Commit Messages**:
```
feat(tips): add BlogPost and BlogComment models with rich text support
feat(tips): implement 9 blog views with approval workflow
feat(tips): create blog templates with featured posts carousel
feat(tips): add CKEditor integration for WYSIWYG editing
feat(tips): implement blog upvoting and commenting system
fix(tips): change upvote_count to method to avoid annotation conflict
fix(tips): add get_tags_list() method for proper tag parsing
fix(tips): improve Featured Articles header text contrast
docs: add ADR-1.0.7 for Expert Blog Posts CMS decision
docs: update TODO.md marking Expert Blog Posts complete
```

**Testing Checklist**:
- [x] Expert user can create blog post
- [x] Non-expert redirected from create page
- [x] Draft posts not visible to public
- [x] Pending posts visible to admins
- [x] Approved posts display in list
- [x] Featured posts appear in carousel
- [x] Upvote toggle works correctly
- [x] Comments can be added and deleted
- [x] View count increments
- [x] Reading time calculates accurately
- [x] Tags render as badges
- [x] Search finds posts by keywords
- [x] Category filter works
- [x] Sort by popular/recent/views works
- [x] Edit/delete restricted to author
- [x] Admin bulk actions function
- [x] Featured image uploads successfully

**Success Metrics**:
- All 14 acceptance criteria items completed ✅
- 4 sample blog posts created successfully
- Zero template syntax errors in production
- All engagement features (upvote, comment, view tracking) operational
- Expert users can publish long-form content independently
- Admin approval workflow prevents low-quality content
