# Generated by Django 4.2.7 on 2023-11-23 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_managers_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created',)},
        ),
        migrations.RemoveIndex(
            model_name='comment',
            name='blog_commen_created_0e6ed4_idx',
        ),
    ]
