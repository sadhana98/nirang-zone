# Generated by Django 2.2.6 on 2020-10-11 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_niranguser_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='niranguser',
            name='mobile',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
