# Generated by Django 3.2.18 on 2023-04-10 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_rename_field1_mymodel_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSVData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='MyModel',
        ),
    ]
