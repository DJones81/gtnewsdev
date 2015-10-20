# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geonewsapi', '0010_article_retweetcount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='category',
            new_name='articlecategory',
        ),
    ]
