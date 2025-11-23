# BRIEF: Build Home Information Database

## Goal

- Implement comprehensive home information database with appliances and service providers addressing PRD §4 F-005 and FR-F-005-1 through FR-F-005-3.

## Scope (single PR)

- **Files to touch**:
  - `homes/models.py`: Home, Appliance, ServiceProvider models with full field definitions
  - `homes/views.py`: CBVs for CRUD operations (ListView, DetailView, CreateView, UpdateView, DeleteView)
  - `homes/forms.py`: HomeForm, ApplianceForm, ServiceProviderForm with validation
  - `homes/admin.py`: Custom admin with ApplianceInline and ServiceProviderInline
  - `templates/homes/`: All home-related templates (list, detail, form, delete confirm)
  - `homes/urls.py`: RESTful URL patterns with namespacing

- **Non-goals**: 
  - Photo uploads for homes or appliances (deferred to v1.2)
  - Appliance maintenance reminders (deferred to v1.1)
  - Service provider ratings or reviews (deferred to v1.2)
  - Integration with real estate APIs (deferred to v2.0)

## Standards

- **Commits**: Conventional style (feat/fix/docs/refactor/chore)
  - Example: `feat(homes): add Home model with construction types and climate zones`
  - Example: `feat(homes): implement CRUD views for home management`
  - Example: `feat(homes): add inline editing for appliances and service providers`
- **No secrets**: All configuration via `settings.py` or environment variables
- **Django tests**: Use unittest/Django TestCase (no pytest)
  - Test Home CRUD operations with authentication
  - Test user can only access/edit their own homes
  - Test appliance and service provider relationships
  - Test inline creation in admin interface

## Acceptance

- **User flow for creating a home**:
  1. Authenticated user navigates to "My Homes"
  2. User clicks "Add a New Home" button
  3. User fills form: name, address, year built, construction type, climate zone, square footage, features (checkboxes for basement, attic, garage, HVAC, etc.)
  4. User submits form
  5. System creates Home linked to current user as owner
  6. User redirects to home detail page

- **User flow for adding appliance**:
  1. User views home detail page
  2. User scrolls to "Appliances" section
  3. User clicks "Add Appliance" button
  4. User fills form: appliance type, manufacturer, model, year installed, warranty expiration
  5. User submits form
  6. System creates Appliance linked to home
  7. User redirects back to home detail page with appliance now visible

- **User flow for adding service provider**:
  1. User views home detail page
  2. User scrolls to "Service Providers" section
  3. User clicks "Add Service Provider" button
  4. User fills form: name, company, specialty (HVAC, plumbing, etc.), contact info
  5. User submits form
  6. System creates ServiceProvider linked to home
  7. User redirects back to home detail page with provider now visible

- **Include migration?**: Yes
  - Migration for Home model with all fields and feature flags
  - Migration for Appliance model with ForeignKey to Home
  - Migration for ServiceProvider model with ForeignKey to Home

- **Update docs & PR checklist**:
  - Update README.md with home database feature description
  - Add to PROJECT_SUMMARY.md completion checklist
  - Document construction type and climate zone choices

## Prompts for Copilot

- "Generate Django models for home information database. Include Home model with owner (FK to User), construction type choices (wood frame, brick, concrete, manufactured), climate zone choices (Northeast, Southeast, Midwest, Southwest, Northwest, Alaska, Hawaii, Tropical), and boolean feature flags (has_basement, has_attic, has_garage, has_hvac, has_fireplace, has_pool, has_well, has_septic). Include Appliance model with FK to Home and ServiceProvider model with FK to Home."

- "Generate Django CBVs for Home CRUD operations using LoginRequiredMixin and UserPassesTestMixin to ensure users can only access/edit their own homes. Include success_url redirects and proper context data."

- "Create Django admin customization for Home model with inline editing for Appliances and ServiceProviders. Include fieldsets to organize the many Home fields logically (Basic Info, Location, Construction Details, Features)."

- "Explain the relationship structure: How are homes linked to users? How are appliances and service providers linked to homes? Why use ForeignKey instead of ManyToMany?"

- "Refactor home age calculation into a property method on Home model that returns the number of years since year_built. Show diff-ready patch."

---

**Related ADR**: None (functionality driven directly by PRD)  
**PRD Reference**: §4 F-005; §5 FR-F-005-1 through FR-F-005-3
