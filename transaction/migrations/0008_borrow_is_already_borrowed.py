# Generated by Django 4.2.3 on 2023-07-20 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0007_alter_borrow_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrow',
            name='is_already_borrowed',
            field=models.BooleanField(default=False),
        ),
    ]
