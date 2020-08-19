Installation
===

Once you have working and fully configured integration of djangoa-allauth, follow these steps.
Create a database entry in socialaccount_socialapp with id: sso_oauth2
    Link to to the django site in the table socialaccount_socialapp_sites.
Depending on how you want to design your login and signup pages,
    you might need to customize your login and signup pages, if they
    iterate over the providers, to not show this one.
Add 'sso.oauth2' to your project settings in INSTALLED_APPS.
Run the database migrations.
Each provider needs to define a client on their end.
    Callback url to use: https://your-domain.com/account/sso_oauth2/login/callback/their-identifier-from-the-database/
Add your SSO clients in the table: sso_oauth2_client
Your SSO login page needs to send the user to:
    reverse('sso_oauth2_login', kwargs={'client_identifier': 'their-identifier-from-the-database'})
    or
    {% url "sso_oauth2_login" client_identifier="their-identifier-from-the-database" %}
