# email sand templates
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import base64

def send_email(subject, to_emails, template_name, context=None, from_email=None, attachments=None):
    """
    发送HTML邮件给多个收件人，支持附件。

    :param subject: 邮件主题
    :param to_emails: 收件人列表 (list)
    :param template_name: 邮件内容模板路径 (templates 文件夹下的相对路径)
    :param context: 渲染模板的上下文变量 (dict)
    :param from_email: 发件人地址 (默认为 settings.DEFAULT_FROM_EMAIL)
    :param attachments: 附件列表，每个附件为 (filename, content, mimetype) 格式的元组
    """
    if context is None:
        context = {}

    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    # embedded_images = []
    # if images:
    #     for image in images:
    #         # 读取图片内容并转为 Base64
    #         image.seek(0)  # 确保从文件开头读取
    #         image_base64 = base64.b64encode(image.read()).decode('utf-8')
    #         embedded_images.append({"name": image.name, "base64": image_base64, "mimetype": image.content_type})

    # 将图片 Base64 数据添加到上下文
    # context["embedded_images"] = embedded_images

    # 渲染HTML内容
    html_content = render_to_string(template_name, context)

    # 创建邮件对象
    email = EmailMultiAlternatives(
        subject=subject,
        body=html_content,  # 默认文本内容
        from_email=from_email,
        to=to_emails
    )

    # 添加HTML内容
    email.attach_alternative(html_content, "text/html")
    print(attachments)
    # 添加附件
    if attachments and attachments != []:
        for attachment in attachments:
            filename, content, mimetype = attachment
            email.attach(filename, content, mimetype)

    # 发送邮件
    email.send()

# 示例用法
# 假设找到了遗失物品，发送邮件通知失主：
# from django.core.files.base import ContentFile
# with open("path/to/image.jpg", "rb") as img_file:
#     image_content = img_file.read()
# send_email(
#     subject="遗失物品已找到",
#     to_emails=["user@example.com"],
#     template_name="emails/found_item.html",
#     context={"item_name": "钱包", "found_location": "办公室", "contact_info": "12345678"},
#     attachments=[("item.jpg", image_content, "image/jpeg")]
# )
