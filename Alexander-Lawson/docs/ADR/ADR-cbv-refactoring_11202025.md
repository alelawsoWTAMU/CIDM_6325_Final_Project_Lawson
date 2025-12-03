# ADR-004: Class-Based View (CBV) Refactoring for CRUD Operations

Date: 2025-11-20
Status: Accepted

## Context

- PRD link: Module 4 Requirements - CBV Implementation and Architectural Analysis
- Problem/forces:
  - Module 3 implementation used mix of patterns (some views as FBVs, some as CBVs)
  - Code duplication across create/update/delete operations (form handling, permission checks)
  - Difficulty onboarding new developers due to inconsistent view patterns
  - Maintenance burden when adding new features (had to update multiple similar functions)

The project needed to standardize on a single architectural pattern for CRUD operations while maintaining all existing functionality (authentication, HTMX search, comments, form validation, accessibility).

## Options

### View Architecture Pattern
- **A) Pure CBVs**: All views as class-based (ListView, DetailView, CreateView, UpdateView, DeleteView)
- **B) Pure FBVs**: All views as functions with decorators
- **C) Hybrid approach**: CBVs for standard CRUD, FBVs for custom logic

### Permission Strategy
- **A) Decorator-based**: @login_required, @permission_required on FBVs
- **B) Mixin-based**: LoginRequiredMixin, UserPassesTestMixin on CBVs
- **C) Manual checks**: if request.user.is_authenticated in view body

### Form Handling
- **A) CBV form_valid/form_invalid**: Override methods in CreateView/UpdateView
- **B) FBV manual processing**: if request.method == 'POST' with form.is_valid()
- **C) Service layer**: Extract form processing to separate service classes

## Decision

We chose:
- **View Architecture**: Hybrid approach (Option C)
  - CBVs for Post CRUD operations (PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView)
  - FBV for search_posts (custom logic with Q objects and HTMX partial rendering)
- **Permission Strategy**: Mixin-based (Option B)
  - LoginRequiredMixin for authentication
  - UserPassesTestMixin with test_func() for authorization
- **Form Handling**: CBV form_valid/form_invalid (Option A)
  - Leverage Django's generic view form processing
  - Override form_valid() to set author automatically

### Implementation Details

#### 1. ListView Pattern
```python
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
```
- No permissions required (public view)
- Automatically queries `Post.objects.all()`
- Passes `posts` variable to template

#### 2. CreateView Pattern
```python
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:index')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```
- LoginRequiredMixin redirects unauthenticated users to login
- form_valid() automatically called when form validates
- Sets author before saving (no manual form.save(commit=False))

#### 3. UpdateView Pattern
```python
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser
    
    def get_success_url(self):
        return reverse_lazy('blog:detail', kwargs={'pk': self.object.pk})
```
- UserPassesTestMixin calls test_func() before allowing access
- Returns 403 if test_func() returns False
- Superuser bypass for moderation

#### 4. DeleteView Pattern
```python
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:index')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser
```
- Same permission logic as UpdateView
- Displays confirmation page before deletion
- Automatically handles POST to delete object

#### 5. Hybrid FBV for Custom Logic
```python
def search_posts(request):
    query = request.GET.get('search', '')
    posts = Post.objects.all()
    
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )
    
    return render(request, 'blog/partials/post_list_content.html', {'posts': posts})
```
- FBV chosen due to custom Q object filtering
- HTMX partial template rendering (not full page)
- Simple enough that CBV overhead not justified

## Consequences

### Positive
- **Reduced Code Duplication**: Generic CBVs eliminate repetitive GET/POST handling
- **Declarative Permissions**: Mixin composition clearly shows security requirements
- **Easier Testing**: Each view is a class with predictable methods to test
- **Better Onboarding**: Django developers recognize standard CBV patterns
- **Maintainability**: Single location to update form handling behavior
- **Type Safety**: Class attributes (model, form_class) provide better IDE support

### Negative/Risks
- **Learning Curve**: Team must understand MRO (Method Resolution Order) for mixin composition
- **Debugging Complexity**: Call stack deeper than FBVs (Django internals invoked)
- **Less Explicit**: Magic methods (get_context_data, form_valid) not obvious to beginners
- **Over-Engineering Risk**: Simple views may not need full CBV machinery
- **Harder to Customize**: Overriding specific behavior requires understanding parent class methods

### Technical Debt
- Some FBV patterns remain (search_posts) - team must know both approaches
- No service layer yet - business logic still in views (acceptable for current complexity)
- test_func() logic duplicated between UpdateView and DeleteView
  - *Future*: Extract to reusable IsAuthorOrSuperuserMixin
- No caching strategy for frequently accessed posts
- Comment CRUD operations not yet implemented (future need)

## Validation

### Success Metrics
- ✅ All CRUD operations migrated to CBVs (5 views converted)
- ✅ No feature regression (authentication, HTMX, validation all working)
- ✅ Permission tests pass for author-only restrictions
- ✅ Lines of code in views.py reduced by ~35%
- ✅ `python manage.py check` passes with 0 issues

### Testing Strategy
```python
# Unit test for permission enforcement
class PostUpdateViewTests(TestCase):
    def test_non_author_cannot_edit(self):
        user1 = User.objects.create_user('user1', password='pass')
        user2 = User.objects.create_user('user2', password='pass')
        post = Post.objects.create(author=user1, title='Test', content='Content')
        
        self.client.login(username='user2', password='pass')
        response = self.client.get(reverse('blog:edit', args=[post.pk]))
        
        self.assertEqual(response.status_code, 403)
```

### Rollback Strategy
If CBVs cause issues:
1. Revert views.py to Module 3 FBV implementation
2. Keep migrations (no database changes)
3. Templates remain unchanged (work with both FBVs and CBVs)

### Monitoring
- Django admin logs capture authentication failures
- Template errors logged to console during development
- UserPassesTestMixin failures return 403 (easily searchable in logs)

## Comparison: Before vs After

### Before (Module 3 - FBV Pattern)
```python
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:index')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author and not request.user.is_superuser:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})
```
**Lines**: ~40 for create + update
**Issues**: Duplicated form handling, repetitive permission checks, manual GET/POST branching

### After (Module 4 - CBV Pattern)
```python
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:index')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_superuser
    
    def get_success_url(self):
        return reverse_lazy('blog:detail', kwargs={'pk': self.object.pk})
```
**Lines**: ~25 for create + update (37% reduction)
**Benefits**: Declarative permissions, no manual GET/POST, Django handles form rendering

## Decision Matrix

| Criterion | FBV Approach | CBV Approach | Winner |
|-----------|-------------|--------------|---------|
| Code Reusability | Low (copy-paste) | High (inheritance) | CBV |
| Readability | High (explicit) | Medium (implicit) | FBV |
| Onboarding Speed | Fast (simple logic) | Slow (MRO knowledge) | FBV |
| Maintainability | Low (DRY violations) | High (single pattern) | CBV |
| Testing Ease | Medium (decorators) | High (class methods) | CBV |
| Customization | Easy (add code) | Hard (understand parent) | FBV |
| Django Idiomatic | Acceptable | Recommended | CBV |
| Performance | Slightly faster | Negligible difference | Tie |

**Overall**: CBV wins for standard CRUD operations; FBV preferred for unique logic

## References
- Django CBV Documentation: <https://docs.djangoproject.com/en/5.2/topics/class-based-views/>
- Classy Class-Based Views: <https://ccbv.co.uk/>
- Two Scoops of Django (Best Practices Guide)
- Related ADRs: ADR-001 (Basic Blog), ADR-003 (Auth + HTMX)
- PRD: Module 4 CBV Implementation Requirements
