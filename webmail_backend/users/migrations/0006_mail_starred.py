# Generated by Django 4.1.7 on 2023-03-15 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_rename_send_to_mail_receiver'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='starred',
            field=models.BooleanField(default=False),
        ),
    ]
