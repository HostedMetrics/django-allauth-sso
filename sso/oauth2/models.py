from django.db import models


EMAIL_KEY = 'email'
NAME_KEY = 'name'
PROFILE_URL_KEY = 'link'
PHOTO_URL_KEY = 'picture'


class Client(models.Model):
    identifier = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    domain = models.CharField(max_length=128)
    client_id = models.CharField(max_length=128)
    client_secret = models.CharField(max_length=128)
    authorize_url = models.CharField(max_length=256)
    access_token_url = models.CharField(max_length=256)
    profile_url = models.CharField(max_length=256)
    scopes = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = 'sso_oauth2_client'
        unique_together = ('domain', )

    def __str__(self):
        return '%s - %s' % (self.name, self.domain, )

# TODO: There has to be a way to not need to register it manually! Seems to be caused by the directory nesting?
from sso.oauth2.provider import SsoOAuth2Provider
from allauth.socialaccount import providers
providers.registry.register(SsoOAuth2Provider)
