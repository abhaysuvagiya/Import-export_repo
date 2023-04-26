# Generated by Django 3.2.18 on 2023-04-10 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_auto_20230410_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvdata',
            name='CIF_Value',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='csvdata',
            name='COMMODITY_DESC',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='csvdata',
            name='GOODS_DESCRIPTION',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='csvdata',
            name='M2_Declaration_Number',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='csvdata',
            name='Stat_Quantity',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='csvdata',
            name='Test',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='csvdata',
            name='Test2',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='csvdata',
            name='unit_price',
            field=models.FloatField(),
        ),
    ]