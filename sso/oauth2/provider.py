from allauth.account.models import EmailAddress
from allauth.socialaccount.app_settings import QUERY_EMAIL
from allauth.socialaccount.providers.base import AuthAction, ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider

from sso.oauth2.models import (
    Client,
    EMAIL_KEY, NAME_KEY, PROFILE_URL_KEY, PHOTO_URL_KEY)


class SsoOAuth2Account(ProviderAccount):
    def get_profile_url(self):
        return self.account.extra_data.get(PROFILE_URL_KEY)

    def get_avatar_url(self):
        return self.account.extra_data.get(PHOTO_URL_KEY)

    def to_str(self):
        dflt = super(SsoOAuth2Account, self).to_str()
        return self.account.extra_data.get(NAME_KEY, dflt)


class SsoOAuth2Provider(OAuth2Provider):
    id = 'sso_oauth2'
    name = 'SsoOAuth2'
    account_class = SsoOAuth2Account

    def get_default_scope(self):
        client_identifier = self.request.path.split('/')[-2]
        oauth2_client = Client.objects.get(identifier=client_identifier)
        scope = oauth2_client.scopes and oauth2_client.scopes.split(' ') or []
        return scope

    def get_auth_params(self, request, action):
        ret = super(SsoOAuth2Provider, self).get_auth_params(request,
                                                          action)
        if action == AuthAction.REAUTHENTICATE:
            ret['prompt'] = 'select_account consent'
        return ret

    def extract_uid(self, data):
        return str(data['email'])

    def extract_email_addresses(self, data):
        ret = []
        email = data.get(EMAIL_KEY)
        if email:
            ret.append(EmailAddress(email=email, verified=True, primary=True))
        return ret

    def extract_common_fields(self, data):
        first_name, last_name = self.full_name_to_first_name_last_name(data.get(NAME_KEY))
        return dict(email=data.get(EMAIL_KEY),
                    last_name=last_name,
                    first_name=first_name)

    def full_name_to_first_name_last_name(self, name):
        if not name:
            name = ''
        parts = name.split(' ')
        if len(parts) == 1:
            first_name = parts[0]
            last_name = ''
        if len(parts) == 2:
            first_name = parts[0]
            last_name = parts[1]
        if len(parts) == 3:
            # This one is tricky. Is it "first, middle, last" or "first, last1, last2"?
            first_name = parts[0]
            last_name = parts[2]
        if len(parts) == 4:
            # assume: first, middle, last1, last2
            first_name = parts[0]
            last_name = ' '.join(parts[2:])
        return first_name, last_name


provider_classes = [SsoOAuth2Provider]
