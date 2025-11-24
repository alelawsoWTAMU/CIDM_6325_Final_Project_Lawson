"""
Context processors for the project.
"""


def expert_status(request):
    """
    Add expert status to all template contexts.
    """
    context = {}
    
    if request.user.is_authenticated:
        context['has_expert_profile'] = hasattr(request.user, 'expert_profile')
        context['is_pending_expert'] = (
            context['has_expert_profile'] and 
            not request.user.is_verified_expert
        )
    else:
        context['has_expert_profile'] = False
        context['is_pending_expert'] = False
    
    return context
