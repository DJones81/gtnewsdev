# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('coords', django.contrib.gis.db.models.fields.GeometryField(srid=4326)),
                ('title', models.CharField(max_length=200)),
                ('url', models.URLField(max_length=300)),
            ],
        ),
    ]
