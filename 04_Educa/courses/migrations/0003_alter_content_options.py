# Generated by Django 5.1.1 on 2024-09-13 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_file_image_module_content_text_video'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={'ordering': ['order']},
        ),
    ]