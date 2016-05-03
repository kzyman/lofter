# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0012_picture_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='picture',
            old_name='description',
            new_name='description1',
        ),
    ]
