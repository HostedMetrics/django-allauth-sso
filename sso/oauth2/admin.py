from django.contrib import admin
from sso.oauth2.models import (
    Client,
)

admin.site.register(Client)
