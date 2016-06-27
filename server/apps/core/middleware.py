from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from apps.accounts.models import BaseUser


class UserTypeMiddleware(object):
    
    def process_request(self, request):
        try:
            request.user = BaseUser.objects.get_subclass(pk=request.user.pk)
        except BaseUser.DoesNotExist:
            path = request.get_full_path()
            if (not path == reverse('accounts:login') and
                '/admin' not in path):
                return redirect('accounts:login')

