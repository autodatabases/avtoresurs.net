# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('manufacturer', models.CharField(null=True, max_length=255, blank=True)),
                ('title', models.CharField(max_length=255)),
                ('sku', models.CharField(max_length=255)),
                ('quantity', models.IntegerField(null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('price', models.DecimalField(max_digits=20, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('image', models.ImageField(null=True, upload_to=products.models.image_upload_to, blank=True)),
                ('product', models.ForeignKey(to='products.Product')),
            ],
        ),
    ]
