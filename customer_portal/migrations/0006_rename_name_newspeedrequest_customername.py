# Generated by Django 4.1.3 on 2023-10-09 04:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer_portal', '0005_alter_newspeedrequest_address_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newspeedrequest',
            old_name='name',
            new_name='customerName',
        ),
    ]
