# Database Schema Documentation

## Entity Relationship Diagram

```
┌─────────────────────────┐
│        User             │
│    (Django Built-in)    │
├─────────────────────────┤
│ - id (PK)               │
│ - username              │
│ - email                 │
│ - password              │
│ - is_staff              │
│ - is_superuser          │
└─────────────────────────┘
         │ 1
         │
         │ *
┌─────────────────────────┐         ┌─────────────────────────┐
│         Post            │ 1     * │       Comment           │
├─────────────────────────┤◄────────┤─────────────────────────┤
│ - id (PK)               │         │ - id (PK)               │
│ - title                 │         │ - post_id (FK)          │
│ - content               │         │ - author_id (FK)        │
│ - author_id (FK)        │         │ - content               │
│ - date_created          │         │ - date_created          │
│ - date_updated          │         │ - date_updated          │
└─────────────────────────┘         └─────────────────────────┘
         │ *
         │
         │ 1
         │
    (User as author)
```

## Models Description

### Post Model
The Post model represents individual blog entries.

**Fields:**
- `id`: Auto-incrementing primary key
- `title`: CharField(max_length=200) - Post title
- `content`: TextField - Main post content
- `author`: ForeignKey(User) - Reference to post author
- `date_created`: DateTimeField - Publication timestamp (default: timezone.now)
- `date_updated`: DateTimeField - Last modification timestamp (auto_now=True)

**Relationships:**
- **Many-to-One** with User (author): Each post has one author, a user can have many posts
- **One-to-Many** with Comment: Each post can have many comments

**Business Logic:**
- Posts are ordered by `date_created` descending (newest first)
- Author field provides accountability and enables permission checking
- Timestamps enable content lifecycle tracking

### Comment Model
The Comment model represents user comments on blog posts.

**Fields:**
- `id`: Auto-incrementing primary key
- `post`: ForeignKey(Post, related_name='comments') - Reference to parent post
- `author`: ForeignKey(User) - Reference to comment author
- `content`: TextField - Comment text
- `date_created`: DateTimeField - Comment timestamp (auto_now_add=True)
- `date_updated`: DateTimeField - Last edit timestamp (auto_now=True)

**Relationships:**
- **Many-to-One** with Post: Each comment belongs to one post, a post can have many comments
- **Many-to-One** with User: Each comment has one author, a user can write many comments

**Business Logic:**
- Comments are ordered by `date_created` ascending (oldest first) for chronological discussion
- The `related_name='comments'` allows easy access via `post.comments.all()`
- CASCADE deletion ensures comments are removed when parent post is deleted

## Migration Notes

### Migration 0001_initial (Post Model)
Created the initial Post model with:
- All base fields (title, content, author, timestamps)
- ForeignKey relationship to Django's User model
- Meta ordering configuration

**Migration Command:**
```bash
python manage.py makemigrations myblog
python manage.py migrate myblog
```

### Migration 0002_comment (Comment Model)
Added Comment model with:
- Relationship to Post and User models
- Timestamp fields for tracking
- Cascade deletion behavior

**Migration Command:**
```bash
python manage.py makemigrations myblog
python manage.py migrate myblog
```

## Business & Analytics Use Cases

### Content Management
- **Post Tracking**: Monitor which authors create the most content
- **Update Frequency**: Analyze how often posts are revised via `date_updated`
- **Publication Timeline**: Track content creation patterns over time

### User Engagement
- **Comment Analytics**: Measure engagement by counting comments per post
- **Active Contributors**: Identify most active commenters
- **Discussion Patterns**: Analyze comment timestamps to understand peak engagement times

### Permissions & Workflow
- **Author Ownership**: Authors can edit/delete only their own posts
- **Moderation**: Superusers can manage all content
- **Guest Authors**: Support for "Guest" user enables anonymous-style contributions

### Data Integrity
- **Referential Integrity**: ForeignKey constraints ensure data consistency
- **Cascade Deletion**: Prevents orphaned comments when posts are deleted
- **Timestamp Tracking**: Automatic audit trail for all content changes

## Database Constraints

1. **Title Uniqueness** (Application Level): Form validation prevents duplicate titles
2. **Required Fields**: title, content, author, post (for comments)
3. **Max Lengths**: title limited to 200 characters
4. **Cascade Rules**: Deleting a post cascades to its comments; deleting a user cascades to their posts and comments

## Performance Considerations

- **Indexing**: Primary keys and foreign keys automatically indexed
- **Ordering**: Pre-sorted queries use database-level ordering
- **Related Queries**: Use `select_related('author')` for post queries to reduce N+1 queries
- **Prefetch**: Use `prefetch_related('comments')` when displaying posts with comment counts
