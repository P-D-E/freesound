#
# Freesound is (c) MUSIC TECHNOLOGY GROUP, UNIVERSITAT POMPEU FABRA
#
# Freesound is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Freesound is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#     See AUTHORS file.
#

from django.conf import settings
from django.core.mail.message import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import get_connection
from django.core.exceptions import ObjectDoesNotExist


def transform_unique_email(email):
    """
    To avoid duplicated emails, in migration accounts.0009_sameuser we automatically change existing
    duplicated user emails by the contents returned in this function. This is reused for further
    checks in utils.mail.replace_email_to and accounts.views.multi_email_cleanup. 
    """
    return "dupemail+%s@freesound.org" % (email.replace("@", "%"), )


def _ensure_list(item):
    if not isinstance(item, tuple) and not isinstance(item, list):
        return [item]
    return item


def send_mail(subject, email_body, user_to=None, email_to=None, email_from=None, reply_to=None,
              email_type_preference_check=None):
    """Sends email with a lot of defaults.

    The function will check if user's email is valid based on bounce info. The function will also check email
    preferences of destinataries of the email. Parameters user_to and email_to are mutually exclusive, if one is set,
    other should be None.

    Args:
        subject (str): subject of the email.
        email_body (str): body of the email.
        user_to (Union[User, List[User]]): a User object or a list of User objects to send the email to. If user_to
            is set, email_to should be None.
        email_to (Union[str, List[str]]): a string representing an email address or a list of strings representing
            email addresses who to send the email to.  If email_to is set, user_to should be None.
        email_from (str): email string that shows up as sender. The default value is DEFAULT_FROM_EMAIL in config.
        reply_to (str): cemail string that will be added as a "Reply-To" header to all mails being sent.
        email_type_preference_check (str): name of EmailPreferenceType that users should have enabled for the email to
            be sent. If set to None, no checks will be carried out.

    Returns:
        (bool): True if all emails were sent successfully, False otherwise.
    """

    assert bool(user_to) != bool(email_to), "One of parameters user_to and email_to should be set, but not both"

    if email_from is None:
        email_from = settings.DEFAULT_FROM_EMAIL

    if user_to:
        user_to = _ensure_list(user_to)
        email_to = []
        for user in user_to:

            # Check that user has preference enabled for that type of email
            email_type_enabled = user.profile.email_type_enabled(email_type_preference_check) \
                if email_type_preference_check is not None else True

            # Check if user's email is valid for delivery and add the correct email address to the list of email_to
            if user.profile.email_is_valid() and email_type_enabled:
                email_to.append(user.profile.get_email_for_delivery())

        # If all users have invalid emails or failed preference check, send no emails
        if len(email_to) == 0:
            return False

    if email_to:
        email_to = _ensure_list(email_to)

    if settings.ALLOWED_EMAILS:  # for testing purposes, so we don't accidentally send emails to users
        email_to = [email for email in email_to if email in settings.ALLOWED_EMAILS]

    try:
        emails = tuple(((settings.EMAIL_SUBJECT_PREFIX + subject, email_body, email_from, [email])
                        for email in email_to))

        # Replicating send_mass_mail functionality and adding reply-to header if requires
        connection = get_connection(username=None, password=None, fail_silently=False)
        headers = None
        if reply_to:
            headers = {'Reply-To': reply_to}
        messages = [EmailMessage(subject, message, sender, recipient, headers=headers)
                    for subject, message, sender, recipient in emails]

        connection.send_messages(messages)
        return True

    except Exception:
        return False


def send_mail_template(subject, template, context, user_to=None, email_to=None, email_from=None, reply_to=None,
                       email_type_preference_check=None):
    context["settings"] = settings
    return send_mail(subject, render_to_string(template, context), user_to, email_to, email_from, reply_to,
                     email_type_preference_check)


def send_mail_template_to_support(subject, template, context, email_from=None, reply_to=None):
    email_to = []
    for email in settings.SUPPORT:
        email_to.append(email[1])
    return send_mail_template(subject, template, context, email_to=email_to, email_from=email_from, reply_to=reply_to)


def render_mail_template(template, context):
    context["settings"] = settings
    return render_to_string(template, context)
