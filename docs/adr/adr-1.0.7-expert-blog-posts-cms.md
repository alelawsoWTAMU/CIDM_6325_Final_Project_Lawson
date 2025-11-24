# ADR-1.0.7: Expert Blog Posts CMS

**Status**: ✅ Accepted and Implemented  
**Date**: 2025-11-23  
**Decision makers**: Alexander J Lawson  
**Technical Story**: Implementation of comprehensive blog system for verified experts

---

## Context and Problem Statement

While the Community Tips feature allows quick advice sharing, verified experts need a platform for longer-form, in-depth educational content. A dedicated blog system with rich text editing, approval workflows, and engagement features would:

1. Position verified experts as thought leaders
2. Provide detailed, comprehensive guides beyond short tips
3. Allow formatting flexibility (headers, lists, images, code)
4. Implement moderation to ensure quality content
5. Drive user engagement through featured posts and upvoting

**Problem**: How should we implement a blog CMS that balances expert autonomy with quality control while maximizing user engagement?

---

## Decision Drivers

- **Content Quality**: Need approval workflow to maintain high standards
- **Expert Empowerment**: Verified experts should have rich editing capabilities
- **User Engagement**: Upvoting, comments, and featured posts drive community
- **SEO Optimization**: Meta descriptions and tags improve discoverability
- **Scalability**: Must handle growing library of articles efficiently
- **Separation of Concerns**: Blog posts are distinct from quick community tips

---

## Considered Options

### Option 1: Extend Existing LocalTip Model
**Pros**: Reuse existing moderation infrastructure  
**Cons**: Tips and blogs serve different purposes; would create messy model with optional fields

### Option 2: Separate BlogPost Model with Full CMS Features ✅ SELECTED
**Pros**: Clean separation, rich text support, dedicated workflow, better UX  
**Cons**: More code to maintain, additional database tables

### Option 3: Third-Party CMS Integration (Wagtail, django-blog-zinnia)
**Pros**: Battle-tested features, extensive plugins  
**Cons**: Learning curve, potential over-engineering, harder to customize

---

## Decision Outcome

**Chosen option: "Option 2 - Separate BlogPost Model with Full CMS Features"**

We implemented a complete blog CMS with the following architecture:

### Data Models

**BlogPost Model** (`tips/models.py`)
```python
class BlogPost(models.Model):
    # Core content
    author = ForeignKey(User)
    title = CharField(max_length=200, unique=True)
    slug = SlugField(max_length=220, unique=True)
    excerpt = TextField(max_length=500)
    content = RichTextField()  # django-ckeditor
    featured_image = ImageField(upload_to='blog_images/', blank=True)
    
    # SEO & Organization
    category = CharField(choices=CATEGORY_CHOICES)
    meta_description = CharField(max_length=160)
    tags = CharField(max_length=200)  # Comma-separated
    
    # Publishing & Moderation
    status = CharField(choices=[draft, pending, approved, rejected])
    is_featured = BooleanField()
    moderation_notes = TextField()
    
    # Engagement
    upvotes = ManyToManyField(User, related_name='blog_upvotes')
    view_count = PositiveIntegerField(default=0)
    
    # Timestamps
    created_at, updated_at, published_at
```

**BlogComment Model** (`tips/models.py`)
```python
class BlogComment(models.Model):
    blog_post = ForeignKey(BlogPost)
    author = ForeignKey(User)
    content = TextField()
    created_at = DateTimeField()
```

### Views Architecture

Implemented 9 class-based views:

1. **BlogListView** - Homepage with featured posts carousel, filtering (category, search, sort)
2. **BlogDetailView** - Full article with engagement (upvotes, comments, view tracking)
3. **BlogCreateView** - Expert-only creation with CKEditor integration
4. **BlogUpdateView** - Edit own posts with version tracking
5. **BlogDeleteView** - Deletion with confirmation
6. **BlogMyPostsView** - Expert dashboard showing all their posts by status
7. **BlogUpvoteView** - Toggle upvote with redirect
8. **BlogCommentCreateView** - Add comments to posts
9. **BlogCommentDeleteView** - Delete own comments

### Rich Text Integration

**Package**: `django-ckeditor 6.7.3` with `Pillow 12.0.0`

**Configuration** (`settings.py`):
```python
INSTALLED_APPS = [
    'ckeditor',
    # ... other apps
]

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['NumberedList', 'BulletedList', 'Blockquote'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ],
        'height': 400,
        'width': '100%',
    }
}
```

### Approval Workflow

**Status Progression**:
```
draft → pending → approved/rejected
          ↓
      (admin review)
```

- **Draft**: Expert working copy, not visible to public
- **Pending**: Submitted for review, visible to admins
- **Approved**: Published and visible to all users
- **Rejected**: Declined with moderation notes

**Admin Features** (`tips/admin.py`):
- Bulk actions: Approve posts, Reject posts, Feature posts
- Filters: Status, category, featured, author
- Search: Title, content, excerpt, author username
- Readonly: Created/updated timestamps, upvote count, view count

### URL Structure

```
/tips/blog/                               # List all approved posts
/tips/blog/<slug:slug>/                   # Article detail
/tips/blog/create/                        # Create new post (experts only)
/tips/blog/<slug:slug>/edit/              # Edit post (author only)
/tips/blog/<slug:slug>/delete/            # Delete post (author only)
/tips/blog/my-posts/                      # Expert dashboard
/tips/blog/<slug:slug>/upvote/            # Toggle upvote
/tips/blog/<slug:slug>/comment/           # Add comment
/tips/blog/comment/<int:pk>/delete/       # Delete comment
```

### Template Structure

**blog_list.html**:
- Featured Articles carousel (2-article rotation)
- Filter sidebar: Category, Search, Sort (popular/recent/most-viewed)
- Paginated article cards with excerpt, author badge, reading time, views
- Responsive Bootstrap 5 grid layout

**blog_detail.html**:
- Article header with category badge, author info, publication date
- Featured image display
- Rich text content rendering
- Tags display using `get_tags_list()` method
- Upvote button with count
- Comments section with inline form
- Related posts (future enhancement placeholder)

**blog_form.html**:
- CKEditor WYSIWYG integration
- Image upload for featured_image
- Category selection dropdown
- Excerpt textarea (500 char max)
- Meta description for SEO
- Tags input (comma-separated)
- Status selection (draft/pending for non-admins)

### Engagement Features

**Upvoting System**:
- ManyToManyField stores user-post relationships
- `get_upvote_count()` method (not @property to avoid annotation conflicts)
- Toggle functionality: upvote again to remove
- Shows "(X)" count next to upvote button
- Login required to upvote

**Comment System**:
- Simple TextField comments
- Author attribution with expert badges
- Delete own comments
- Login required to comment

**View Tracking**:
- `view_count` increments on each BlogDetailView GET request
- Displayed in article cards and detail pages

**Reading Time Calculation**:
```python
@property
def reading_time(self):
    word_count = len(self.content.split())
    return max(1, round(word_count / 200))  # 200 words/min
```

### Security & Permissions

**Expert-Only Creation**:
```python
class BlogCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_verified_expert
```

**Author-Only Editing**:
```python
class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.get_object().author == self.request.user
```

**Public Read Access**:
- List and detail views require no authentication
- Only approved posts visible to non-authors

---

## Consequences

### Positive

✅ **Expert Empowerment**: Verified experts can create rich, formatted content  
✅ **Quality Control**: Approval workflow ensures high standards  
✅ **User Engagement**: Upvoting and comments drive community interaction  
✅ **SEO Benefits**: Meta descriptions and tags improve search visibility  
✅ **Clean Separation**: Blogs don't clutter the quick-tips feed  
✅ **Scalability**: Efficient queries with select_related/prefetch_related  
✅ **Featured Content**: Carousel highlights best articles  
✅ **Analytics**: View counts and upvotes show engagement  

### Negative

⚠️ **Maintenance Overhead**: Separate system from LocalTip requires parallel updates  
⚠️ **Moderation Burden**: Admin must review all pending posts  
⚠️ **Storage Requirements**: Featured images increase media storage needs  
⚠️ **Complexity**: Additional URL patterns, views, forms, templates to maintain  

### Neutral

ℹ️ **Learning Curve**: Experts must learn CKEditor for rich text formatting  
ℹ️ **Two-Step Publishing**: Draft → Pending → Approved adds friction  
ℹ️ **Image Dependency**: Pillow library required for ImageField support  

---

## Implementation Notes

### Database Migrations

**Migration 0004** (`tips/migrations/0004_blogpost_blogcomment.py`):
- Created BlogPost table with all fields
- Created BlogComment table with foreign keys
- Added indexes on published_at, status, category
- Set up ManyToMany through table for upvotes

### Bug Fixes During Implementation

**Issue 1: Property Conflict**
- **Problem**: `@property upvote_count` conflicted with `.annotate(upvote_count=Count('upvotes'))`
- **Solution**: Changed to method `get_upvote_count()`, updated all references

**Issue 2: Template Syntax Error**
- **Problem**: `{% for tag in blog_post.tags.split:',' %}` - invalid Django syntax
- **Solution**: Added `get_tags_list()` method to model returning `[tag.strip() for tag in self.tags.split(',')]`

**Issue 3: Featured Articles Readability**
- **Problem**: Dark text on gold background (`--compass-gold`) had poor contrast
- **Solution**: Changed card-header and h4 to `color: white !important;`

### Sample Data Created

Created 4 blog posts with 2 featured:
1. **Complete Guide to HVAC Maintenance** (HVAC1234, featured)
2. **10 Home Safety Devices Every Homestead Should Have** (SafetyInspector, featured)
3. **Home Electrical Safety Tips** (ElectricianExpert)
4. (Additional post in production)

---

## Validation and Testing

### Manual Testing Performed

✅ Expert user can create blog post with rich text formatting  
✅ Non-expert users cannot access create page (redirected)  
✅ Draft posts not visible to public  
✅ Pending posts visible to admins for review  
✅ Approved posts display in blog list  
✅ Featured posts appear in carousel  
✅ Upvote toggle works correctly  
✅ Comments display and can be added  
✅ View count increments on page view  
✅ Reading time calculates correctly  
✅ Tags render as badges  
✅ Search and filter work properly  
✅ Pagination works on blog list  
✅ Edit/delete restricted to post author  
✅ Featured image uploads successfully  

### Admin Testing

✅ Bulk approve/reject/feature actions work  
✅ Moderation notes save correctly  
✅ Filter by status/category/featured works  
✅ Search finds posts by title/content  
✅ Readonly fields prevent accidental edits  

---

## References

- **PRD**: [home_maintenance_compass_prd_v1.0.2.md](../prd/home_maintenance_compass_prd_v1.0.2.md) - Expert Blog Posts requirement
- **TODO**: [TODO.md](../../TODO.md) - Expert Blog Posts checklist (marked COMPLETE)
- **Package**: [django-ckeditor documentation](https://github.com/django-ckeditor/django-ckeditor)
- **Related ADR**: [adr-1.0.6-local-expert-verification-system.md](./adr-1.0.6-local-expert-verification-system.md) - Expert verification prerequisite

---

## Future Enhancements

- **Rich Media**: YouTube video embeds, image galleries
- **Categories Management**: Dynamic category creation in admin
- **Tag Cloud**: Popular tags visualization
- **Related Posts Algorithm**: Show similar articles based on tags/category
- **Draft Auto-Save**: Prevent content loss during editing
- **Version History**: Track edits over time
- **Email Notifications**: Notify admins of pending posts, authors of approval/rejection
- **Social Sharing**: Share buttons for Facebook, Twitter, LinkedIn
- **Reading Progress Bar**: Visual indicator of scroll position
- **Bookmarking**: Save articles for later reading
- **Author Profiles**: Dedicated page showing all posts by expert
- **RSS Feed**: Subscribe to new blog posts
