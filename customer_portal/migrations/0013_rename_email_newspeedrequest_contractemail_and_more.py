# Generated by Django 4.1.3 on 2023-10-11 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_portal', '0012_remove_newspeedrequest_address_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newspeedrequest',
            old_name='email',
            new_name='contractEmail',
        ),
        migrations.RenameField(
            model_name='newspeedrequest',
            old_name='phoneNumber',
            new_name='contractPhone',
        ),
        migrations.AddField(
            model_name='newspeedrequest',
            name='contractName',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='newspeedrequest',
            name='customerName',
            field=models.TextField(null=True),
        ),
    ]
