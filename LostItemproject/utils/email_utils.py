# email sand templates

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from smtplib import SMTPException
import logging
import base64


# Asynchronous waiting to send mail
@shared_task(bind=True, max_retries=3)
def send_email_async(self, subject, to_emails, template_name, context=None, from_email=None, attachments=None):
    logger = logging.getLogger(__name__)
    try:
        send_email(subject, to_emails, template_name, context, from_email, attachments)
        logger.info(f"Email successfully sent to: {to_emails}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_emails}: {e}")
        logger.exception("Exception occurred while sending email")
        raise self.retry(exc=e, countdown=60)  # 在 60 秒后重试 # 60秒後に再試行


# Send email directly
def send_email(subject, to_emails, template_name, context=None, from_email=None, attachments=None):
    """
        添付ファイルをサポートする HTML 電子メールを複数の受信者に送信します。

        :param 件名: 電子メールの件名
        :param to_emails: 受信者リスト (リスト)
        :param template_name: メールコンテンツテンプレートのパス（テンプレートフォルダ下の相対パス）
        :param context: テンプレートをレンダリングするためのコンテキスト変数 (dict)
        :param from_email: 送信者アドレス (デフォルトは settings.DEFAULT_FROM_EMAIL)
        :param 添付ファイル: 添付ファイルのリスト。各添付ファイルは (ファイル名、コンテンツ、MIME タイプ) 形式のタプルです。
    """
    if context is None:
        context = {}

    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    html_content = render_to_string(template_name, context)

    email = EmailMultiAlternatives(
        subject=subject,
        body=html_content,
        from_email=from_email,
        to=to_emails
    )

    email.attach_alternative(html_content, "text/html")

    if attachments and attachments != []:
        for attachment in attachments:
            filename, content, mimetype = attachment
            email.attach(filename, content, mimetype)

    try:
        email.send()
    except SMTPException as e:
        print(f"SMTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# 使用例
# 紛失物が見つかった場合は、電子メールを送信して所有者に通知します。
# send_email(
#     subject="落とし物が見つかるかもしれない",
#     to_emails=["user@example.com"],
#     template_name="emails/found_item.html",
#     context={"item_name": "財布", "found_location": "図書館", "storage_location": "図書館"},
#     attachments=[("item.jpg", image_content, "image/jpeg")]
# )
