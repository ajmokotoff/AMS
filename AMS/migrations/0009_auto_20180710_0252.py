# Generated by Django 2.0.7 on 2018-07-10 02:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AMS', '0008_auto_20180710_0226'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='holdings',
            unique_together={('portfolio', 'stock')},
        ),
    ]
