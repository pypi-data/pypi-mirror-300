from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import View
from rest_framework.reverse import reverse


class AppView(View):
    """Etherflow's Python DCIM Populator main/home view"""
    template_name = 'py_populate_dcim/appview.html'

    def get(self, request):
        if not request.user.is_authenticated:
            print(request.resolver_match.view_name)
            after_login = reverse("plugins:py_populate_dcim:home")
            login_url = reverse(settings.LOGIN_URL)
            return redirect(f"{login_url}?next={after_login}")

        return render(request, self.template_name, {
            'appview_field': 'testasdf'
        })
