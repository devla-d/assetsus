from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings


def custom_processor(request):
    current_site = get_current_site(request)
    context = {}
    context["sitename"] = current_site.name
    context["domain"] = current_site.domain
    context["RECAPTCHA_PUBLIC_KEY"] = settings.RECAPTCHA_PRIVATE_KEY

    return context
