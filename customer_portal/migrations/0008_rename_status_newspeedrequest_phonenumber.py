# Generated by Django 4.1.3 on 2023-10-10 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer_portal', '0007_rename_mrc_newspeedrequest_newmrc_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newspeedrequest',
            old_name='status',
            new_name='phoneNumber',
        ),
    ]
