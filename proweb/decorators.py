from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def group_required(*group_names):
    def in_group(user):
        if user.groups.filter(name__in=group_names).exists():
            return True
        else:
            raise PermissionDenied
    return user_passes_test(in_group)