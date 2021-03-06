# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-20 06:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('viewflow', '0005_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=250)),
                ('port', models.CharField(max_length=250)),
                ('username', models.CharField(max_length=250)),
                ('password', models.CharField(max_length=250)),
                ('vendor', models.CharField(choices=[(b'cisco', b'Cisco'), (b'juniper', b'Juniper'), (b'huawei', b'Huawei')], default=b'cisco', max_length=250)),
                ('coninfo', models.TextField(blank=True, default=b'\n             \n             Device information\n\n\n         ', max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProcess',
            fields=[
                ('process_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='viewflow.Process')),
                ('trusted', models.NullBooleanField(default=False)),
                ('permit_ip', models.CharField(max_length=250)),
                ('host', models.CharField(max_length=250)),
                ('content', models.TextField(blank=True, default=b'\n             \n             Device information\n\n\n         ', max_length=250)),
                ('content2', models.TextField(blank=True, default=b'\n             \n             Device information\n\n\n         ', max_length=250)),
            ],
            options={
                'abstract': False,
            },
            bases=('viewflow.process',),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.OrderProcess'),
        ),
    ]
