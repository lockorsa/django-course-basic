# Generated by Django 3.2.8 on 2021-10-29 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_alter_shopuser_birth_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shopuser',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
