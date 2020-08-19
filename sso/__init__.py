"""
Installation:
Create a database entry in socialaccount_socialapp with id: sso_oauth2
Depending on how you want to design your login and signup pages,
    you might need to customize your login and signup pages, if they
    iterate over the providers, to not show this one.
Add 'sso' to your project settings in INSTALLED_APPS.
Run the database migrations.
Each provider needs to define a client on their end.
    Callback url to use: /account/sso_oauth2/login/callback/
Add your SSO clients in the table: sso_oauth2client
Your SSO login page needs to redirect to:
    reverse('provider_login_url', 'sso_oauth2', kwargs={'domain': 'example.com'})
    or
    {% load socialaccount %}
    {% provider_login_url "sso_oauth2" domain="example.com" %}

2	2020-08-07 14:17:39.840606+00	2020-08-07 14:17:39.840606+00	airthings	Airthings	5b37bbf3-6001-4068-87e3-87aeaa374349	956d9b7d-99fd-478e-9ff7-2fd5a16fcacd	386	https://accounts-api.airthings.com/v1/token	https://accounts.airthings.com/authorize	https://accounts-api.airthings.com/v1/profile	profile
"""
