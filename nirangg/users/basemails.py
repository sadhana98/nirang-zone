from django.core.mail import BadHeaderError
from django.template import Context
from django.core.mail import EmailMessage
from rest_framework.response import Response
from django.template.loader import get_template


class BaseMails:
    @classmethod
    def send(cls, subject, recipients, template_name=None, template_data=None, attachments=None,
             cc_to=None, attachments_full_path=None):

        from_email = "xx@gmail.com"
        attachments = attachments
        if template_name:
            html = get_template(template_name)
            html_content = html.render(template_data)

            if recipients and len(recipients) > 0:
                recipients_list = list(set(recipients))
                if None in recipients_list:
                    recipients.remove(None)

            cc_to = '' if (cc_to is '' or cc_to is None) else cc_to
            recipients = recipients if type(recipients) is list else [recipients]
            try:
                email = EmailMessage(subject, html_content, from_email, to=recipients, cc=cc_to)
                email.content_subtype = 'html'

                if attachments is not None:
                    if attachments is not None:
                            email.attach(attachments['filename'], attachments['content'],attachments['mimetype'])
                    elif attachments_full_path is not None:
                        for path in attachments_full_path:
                            email.attach_file(path)

                a = email.send()

            except BadHeaderError:
                return Response('invalid header found')

            return Response(True)
