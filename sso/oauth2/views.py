import requests

from django.contrib.auth.models import User
from django.urls import reverse

from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
from allauth.utils import build_absolute_uri

from sso.oauth2.models import Client
from sso.oauth2.provider import SsoOAuth2Provider


class SsoOAuth2Adapter(OAuth2Adapter):
    provider_id = SsoOAuth2Provider.id

    def get_oauth2_client_identifier(self):
        oauth2_client_identifier = self.request.path.split('/')[-2]
        return oauth2_client_identifier

    def get_oauth2_client(self):
        client_identifier = self.get_oauth2_client_identifier()
        oauth2_client = Client.objects.get(identifier=client_identifier)
        return oauth2_client

    def get_provider(self):
        provider = super().get_provider()
        provider.client_id = ''
        provider.client_name = ''
        return provider

    def get_callback_url(self, request, app):
        client_identifier = self.get_oauth2_client_identifier()
        callback_url = reverse(self.provider_id + "_callback", kwargs={'client_identifier': client_identifier})
        protocol = self.redirect_uri_protocol
        return build_absolute_uri(request, callback_url, protocol)

    @property
    def authorize_url(self):
        oauth2_client = self.get_oauth2_client()
        return oauth2_client.authorize_url

    @property
    def access_token_url(self):
        oauth2_client = self.get_oauth2_client()
        return oauth2_client.access_token_url

    @property
    def profile_url(self):
        oauth2_client = self.get_oauth2_client()
        return oauth2_client.profile_url

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(
            self.profile_url,
            headers={'Authorization': 'Bearer %s' % token.token})
        resp.raise_for_status()
        extra_data = resp.json()
        oauth2_client = self.get_oauth2_client()
        extra_data.update({
            'sso_client_identifier': oauth2_client.identifier,
            'sso_client_name': oauth2_client.name,
            'sso_client_domain': oauth2_client.domain,
        })

        # We trust the email address; therefore, we will add this login method to any existing user with that email address.
        # We do so by creating a SocialAccount if it does not exist.
        email = extra_data[oauth2_client.email_key]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            object_identifier = {'provider': self.provider_id, 'uid': email}
            if not SocialAccount.objects.filter(**object_identifier).exists():
                social_account = SocialAccount(user_id=user.id, extra_data=extra_data, **object_identifier)
                social_account.save()

        login = self.get_provider() \
            .sociallogin_from_response(request,
                                       extra_data)
        return login


class SsoOAuth2LoginView(OAuth2LoginView):

    def get_client(self, request, app):
        client_identifier = request.path.split('/')[-2]
        oauth2_client = Client.objects.get(identifier=client_identifier)
        client = super().get_client(request, app)
        client.consumer_key = oauth2_client.client_id
        client.consumer_secret = oauth2_client.client_secret
        return client


class SsoOAuth2CallbackView(OAuth2CallbackView):

    def get_client(self, request, app):
        client_identifier = request.path.split('/')[-2]
        oauth2_client = Client.objects.get(identifier=client_identifier)
        client = super().get_client(request, app)
        client.consumer_key = oauth2_client.client_id
        client.consumer_secret = oauth2_client.client_secret
        return client


oauth2_login = SsoOAuth2LoginView.adapter_view(SsoOAuth2Adapter)
oauth2_callback = SsoOAuth2CallbackView.adapter_view(SsoOAuth2Adapter)
