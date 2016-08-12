from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from apps.accounts.models import BaseUser


class UserTypeMiddleware(object):
    
    def process_request(self, request):
        try:
            request.user = BaseUser.objects.get_subclass(pk=request.user.pk)
        except BaseUser.DoesNotExist:
            path = request.get_full_path()
            login_url = reverse('accounts:login')
            if (not request.path == login_url and
                '/login' not in path and
                '/admin' not in path and
                '/rest' not in path):
                return redirect('%s?next=%s' % (login_url, request.path))

