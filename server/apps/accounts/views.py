from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView, View

from .forms import LoginForm


class LoginFormView(FormView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def get_success_url(self):
        next_param = self.request.GET.get('next', None)
        if next_param:
            return next_param
        return reverse_lazy('accounts:dashboard')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            login(self.request, user)
            return super(LoginFormView, self).form_valid(form)
        form.errors['__all__'] = form.error_class(['Invalid login'])
        return render(self.request, 'accounts/login.html', {'form': form})


class LogoutView(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('accounts:login'))


class DashboardView(TemplateView):
    template_name = 'accounts/dashboard.html'
   
    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        from apps.budgets.models import Transaction
        from apps.budgets.models import Budget
        transactions = Transaction.objects.filter(
                            account__app_users=self.request.user)
        context['budgets'] = Budget.objects.filter(pk__in=transactions)
        return context
