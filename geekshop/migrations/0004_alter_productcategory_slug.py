# Generated by Django 3.2.8 on 2021-10-27 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geekshop', '0003_alter_productcategory_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='URL'),
        ),
    ]