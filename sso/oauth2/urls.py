from django.urls import include, path

from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from allauth.utils import import_attribute

from sso.oauth2.provider import SsoOAuth2Provider


def customized_urlpatterns(provider):
    login_view = import_attribute(
        provider.get_package() + '.views.oauth2_login')
    callback_view = import_attribute(
        provider.get_package() + '.views.oauth2_callback')

    urlpatterns = [
        path('login/<str:client_identifier>/', login_view, name=provider.id + "_login"),
        path('login/callback/<str:client_identifier>/', callback_view, name=provider.id + "_callback"),
    ]

    return [path(provider.get_slug() + '/', include(urlpatterns))]


urlpatterns = customized_urlpatterns(SsoOAuth2Provider)
