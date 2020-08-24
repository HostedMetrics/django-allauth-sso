django-allauth-sso is a library that builds upon the django-allauth library to provide single sign-on capabilities. It currently supports OAuth2.

Installation and Configuration
===

Once you have a working and fully configured integration of django-allauth, follow these steps.

- Create a database entry in the table `socialaccount_socialapp`, with id `sso_oauth2`.
- Link it to the django site in the table `socialaccount_socialapp_sites`.

- If your login and signup pages iterate over the list of social providers,
    you might need to customize them to exclude this newly added provider so that it won't be displayed to the user.

- Add `sso.oauth2` to `INSTALLED_APPS` in your project settings.

- Run the database migrations: `python manage.py migrate`.

- Each provider (organizations using your SSO mechanism) needs to define an OAuth2 client on their end. Or maybe you can do this yourself on their website. The callback url to use is: https://`your-domain.com`/account/sso_oauth2/login/callback/`their-identifier-from-the-sso_oauth2_client-database-table`/

- Add your SSO clients in the table `sso_oauth2_client`.

- Your SSO login page needs to send the user to:
    `reverse('sso_oauth2_login', kwargs={'client_identifier': 'their-identifier-from-the-database'})`
    or
    `{% url "sso_oauth2_login" client_identifier="their-identifier-from-the-database" %}`

Warning - user account security implications
===
This library assumes you require users to verify their email addresses before being able to log in (as just about every website does).

Why? 
To provide for a smooth user experience for this most common scenario, unlike django-allauth, this library will link the SSO/social user to any existing account with the same email, instead of complaining about a conflict.

To require email address verification before users can log in means that you have set the following settings for django-allauth:
`ACCOUNT_EMAIL_REQUIRED = True`
`ACCOUNT_EMAIL_VERIFICATION = 'mandatory'`.

Refer to the comment in `sso.oauth2.views.SsoOAuth2Adapter.complete_login` for more details.

