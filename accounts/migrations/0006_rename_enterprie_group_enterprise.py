# Generated by Django 5.0.6 on 2024-07-25 01:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_usergroups_delete_userpermission'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='enterprie',
            new_name='enterprise',
        ),
    ]
