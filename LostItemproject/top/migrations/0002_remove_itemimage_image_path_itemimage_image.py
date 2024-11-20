# Generated by Django 4.2.16 on 2024-11-20 03:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("top", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="itemimage",
            name="image_path",
        ),
        migrations.AddField(
            model_name="itemimage",
            name="image",
            field=models.ImageField(
                blank=True,
                max_length=255,
                null=True,
                upload_to="item_images/",
                verbose_name="Item Images",
            ),
        ),
    ]