django-allauth-sso is a library that builds upon the django-allauth library to provide single sign-on capabilities. It currently supports OAuth2.

Installation and Configuration
===

Once you have a working and fully configured integration of django-allauth, follow these steps.

- Create a database entry in the table `socialaccount_socialapp`, with id `sso_oauth2`.
- Link it to the django site in the table `socialaccount_socialapp_sites`.

- Depending on how you want to design your login and signup pages,
    you might need to customize your login and signup pages, if they
    iterate over the providers, to not show this one.

- Add `sso.oauth2` to `INSTALLED_APPS` in your project settings.

- Run the database migrations.

- Each provider needs to define a client on their end. The callback url to use is `https://your-domain.com/account/sso_oauth2/login/callback/their-identifier-from-the-database/`

- Add your SSO clients in the table `sso_oauth2_client`.

- Your SSO login page needs to send the user to:
    `reverse('sso_oauth2_login', kwargs={'client_identifier': 'their-identifier-from-the-database'})`
    or
    `{% url "sso_oauth2_login" client_identifier="their-identifier-from-the-database" %}`

Warning
===
This library assumes you require users to verify their email addresses before being able to log in. Unlike django-allauth, it will link the SSO login to any existing account with the same email, instead of complaining about a conflict.