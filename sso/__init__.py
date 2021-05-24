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
    or in your Django templates:
    {% load socialaccount %}
    {% provider_login_url "sso_oauth2" domain="example.com" %}
"""
