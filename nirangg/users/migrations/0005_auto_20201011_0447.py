# Generated by Django 2.2.6 on 2020-10-11 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20201011_0445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='niranguser',
            name='mobile',
            field=models.CharField(max_length=150),
        ),
    ]
