# Generated by Django 3.2.7 on 2021-09-11 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='subtitle',
            field=models.CharField(default=1, max_length=250),
            preserve_default=False,
        ),
    ]
