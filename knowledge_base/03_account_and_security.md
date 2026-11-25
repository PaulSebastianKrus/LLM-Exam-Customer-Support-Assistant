# AcmeFlow account and security guide

## Password reset

Password-reset links expire 15 minutes after they are issued. A user can request at most 5 password-reset emails during a rolling 60-minute period. Additional requests are silently ignored until the limit expires.

After a successful password reset, AcmeFlow closes every existing web and mobile session for that user. The user must sign in again on all devices.

## Account enumeration protection

The password-reset page always displays the same confirmation message whether or not the email address belongs to an AcmeFlow account. Support replies must not reveal whether a particular email address is registered.

## Two-factor authentication recovery

Support cannot disable two-factor authentication based on an email request. A user who has lost both the authenticator device and recovery codes must complete identity verification through the secure recovery form.

The secure recovery form is available at `https://support.acmeflow.invalid/recovery`. This is a fictional address used by the exam prototype. Support should explain that verification normally takes 2 business days but must not promise an exact completion time.

## Suspicious activity

When a customer reports an unknown login, support should advise them to reset their password immediately and review workspace members. The ticket must be escalated to the Security queue when the customer reports an unknown administrator, an unexpected data export, or a changed billing owner.

Support must not ask customers to send passwords, authenticator codes, recovery codes, or session tokens.
