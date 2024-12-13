# 定时检查数据中可能登记或者时间超时（1个月）


from celery import shared_task
from utils import email_utils, item_utils


@shared_task
def my_scheduled_task():
    print("Executing scheduled task...")
    # 在此处添加您的定时任务逻辑
    return "Task completed!"


@shared_task
def send_periodic_email():
    subject = "定时任务测试邮件"
    message = "这是 Celery 定时任务发送的测试邮件。"
    email_utils.send_email_async(subject=subject,
                                 to_emails=['cralpbin@gmail.com'],
                                 template_name="emails/found_item.html",
                                 context={"item_name": "財布", "found_location": "図書館", "storage_location": "図書館"},
                                 attachments=None)
