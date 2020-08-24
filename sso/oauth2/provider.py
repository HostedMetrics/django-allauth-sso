import importlib

from allauth.account.models import EmailAddress
from allauth.socialaccount.app_settings import QUERY_EMAIL
from allauth.socialaccount.providers.base import AuthAction, ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider

from sso.oauth2.models import Client


class SsoOAuth2Account(ProviderAccount):
    def get_profile_url(self):
        oauth2_client = self.get_oauth2_client(self.account.extra_data['sso_client_identifier'])
        return self.account.extra_data.get(oauth2_client.profile_url_key)

    def get_avatar_url(self):
        oauth2_client = self.get_oauth2_client(self.account.extra_data['sso_client_identifier'])
        return self.account.extra_data.get(oauth2_client.photo_url_key)

    def to_str(self):
        oauth2_client = self.get_oauth2_client(self.account.extra_data['sso_client_identifier'])
        dflt = super(SsoOAuth2Account, self).to_str()
        return self.account.extra_data.get(oauth2_client.email_key, dflt)

    def get_oauth2_client(self, client_identifier):
        oauth2_client = Client.objects.get(identifier=client_identifier)
        return oauth2_client


class SsoOAuth2Provider(OAuth2Provider):
    id = 'sso_oauth2'
    name = 'SsoOAuth2'
    account_class = SsoOAuth2Account

    def get_oauth2_client(self):
        client_identifier = self.request.path.split('/')[-2]
        oauth2_client = Client.objects.get(identifier=client_identifier)
        return oauth2_client

    def get_default_scope(self):
        oauth2_client = self.get_oauth2_client()
        scope = oauth2_client.scopes and oauth2_client.scopes.split(' ') or []
        return scope

    def get_auth_params(self, request, action):
        ret = super(SsoOAuth2Provider, self).get_auth_params(request,
                                                          action)
        if action == AuthAction.REAUTHENTICATE:
            ret['prompt'] = 'select_account consent'
        return ret

    def extract_uid(self, data):
        oauth2_client = self.get_oauth2_client()
        return str(data[oauth2_client.email_key])

    def extract_email_addresses(self, data):
        ret = []
        oauth2_client = self.get_oauth2_client()
        email = data.get(oauth2_client.email_key)
        if email:
            ret.append(EmailAddress(email=email, verified=True, primary=True))
        return ret

    def extract_common_fields(self, data):
        oauth2_client = self.get_oauth2_client()
        if oauth2_client.name_parser:
            name_parser_fn = self.import_attribute(oauth2_client.name_parser)
            first_name, last_name = name_parser_fn(data, oauth2_client)
        else:
            if oauth2_client.full_name_key:
                full_name = data.get(oauth2_client.full_name_key)
                first_name, last_name = self.__class__.full_name_to_first_name_last_name(full_name)
            else:
                if oauth2_client.first_name_key:
                    first_name = data.get(oauth2_client.first_name_key)
                else:
                    first_name = None
                if oauth2_client.last_name_key:
                    last_name = data.get(oauth2_client.last_name_key)
                else:
                    last_name = None

        return dict(email=data.get(oauth2_client.email_key),
                    last_name=last_name,
                    first_name=first_name)

    @staticmethod
    def full_name_to_first_name_last_name(name):
        if not name:
            return None, None
        parts = name.split(' ')
        if len(parts) == 1:
            first_name = parts[0]
            last_name = ''
        if len(parts) == 2:
            first_name = parts[0]
            last_name = parts[1]
        if len(parts) == 3:
            # This one is ambiguous. Is it "first, middle, last" or "first, last1, last2"?
            first_name = parts[0]
            last_name = parts[2]
        if len(parts) == 4:
            # assume: first, middle, last1, last2
            first_name = parts[0]
            last_name = ' '.join(parts[2:])
        return first_name, last_name

    def import_attribute(self, path):
        try:
            pkg, attr = path.rsplit('.', 1)
            result = getattr(importlib.import_module(pkg), attr)
        except ModuleNotFoundError:
            pkg, cls, attr = path.rsplit('.', 2)
            pkg = importlib.import_module(pkg)
            cls = getattr(pkg, cls)
            result = getattr(cls, attr)
        return result


provider_classes = [SsoOAuth2Provider]
