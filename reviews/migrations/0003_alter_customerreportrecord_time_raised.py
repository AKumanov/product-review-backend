# Generated by Django 4.1.2 on 2022-10-06 14:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_customerreportrecord_image_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerreportrecord',
            name='time_raised',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 6, 17, 27, 49, 509530), editable=False),
        ),
    ]
