# Generated by Django 2.0.3 on 2018-10-02 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_collections', '0008_merge_20180929_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='supercollection',
            name='show_in_root_list',
            field=models.BooleanField(default=False),
        ),
    ]