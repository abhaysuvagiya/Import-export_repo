# Generated by Django 3.2.18 on 2023-04-10 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_rename_index_csvdata_m2_declaration_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvdata',
            name='M2_Declaration_Number',
            field=models.CharField(max_length=255),
        ),
    ]
