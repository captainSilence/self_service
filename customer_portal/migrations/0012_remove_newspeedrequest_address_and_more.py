# Generated by Django 4.1.3 on 2023-10-10 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer_portal', '0011_newspeedrequest_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newspeedrequest',
            name='address',
        ),
        migrations.RemoveField(
            model_name='newspeedrequest',
            name='nodeID',
        ),
    ]
