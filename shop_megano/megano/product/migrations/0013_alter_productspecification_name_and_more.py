# Generated by Django 4.2 on 2024-06-04 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_alter_productspecification_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productspecification',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='productspecification',
            name='value',
            field=models.CharField(default='', max_length=200),
        ),
    ]
