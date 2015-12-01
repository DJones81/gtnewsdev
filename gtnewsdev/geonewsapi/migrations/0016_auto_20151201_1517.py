# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geonewsapi', '0015_auto_20151119_0520'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='articlecategory',
            new_name='sectionname',
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
