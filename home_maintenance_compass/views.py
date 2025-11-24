"""
Views for the main project pages.
"""

from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    Main homepage view that handles different user states.
    """
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Check if user has an expert profile but is not approved
        if self.request.user.is_authenticated:
            context['has_expert_profile'] = hasattr(self.request.user, 'expert_profile')
            context['is_pending_expert'] = (
                context['has_expert_profile'] and 
                not self.request.user.is_verified_expert
            )
        
        return context
