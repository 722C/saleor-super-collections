# Generated by Django 2.0.10 on 2019-08-01 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('super_collections', '0016_supercollection_show_collections'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supercollection',
            name='show_children_in_side_nav',
        ),
    ]
