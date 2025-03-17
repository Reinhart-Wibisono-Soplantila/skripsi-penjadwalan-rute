from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied

class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is admin."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)