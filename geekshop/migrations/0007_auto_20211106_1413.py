# Generated by Django 3.2.8 on 2021-11-06 14:13

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geekshop', '0006_auto_20211106_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=True, populate_from='name', unique=True, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=True, populate_from='name', unique=True, verbose_name='URL'),
        ),
    ]