# Generated by Django 4.2.17 on 2024-12-19 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_transaction_time_alter_savings_amount_saved'),
    ]

    operations = [
        migrations.RenameField(
            model_name='savings',
            old_name='user',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='user',
            new_name='user_id',
        ),
    ]
