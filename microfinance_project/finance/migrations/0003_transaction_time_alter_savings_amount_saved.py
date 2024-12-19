# Generated by Django 4.2.17 on 2024-12-19 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_user_user_type_alter_user_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='time',
            field=models.TimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='savings',
            name='amount_saved',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
