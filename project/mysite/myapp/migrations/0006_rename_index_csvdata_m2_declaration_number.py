# Generated by Django 3.2.18 on 2023-04-10 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20230410_1233'),
    ]

    operations = [
        migrations.RenameField(
            model_name='csvdata',
            old_name='index',
            new_name='M2_Declaration_Number',
        ),
    ]
