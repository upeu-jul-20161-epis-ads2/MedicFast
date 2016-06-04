# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('logo', models.ImageField(default=b'associations/default.png', upload_to=b'associations', verbose_name='Logo')),
                ('type_a', models.CharField(default=b'PRIVATE', max_length=10, verbose_name='Type', choices=[(b'GOVERMENT', 'Government'), (b'PRIVATE', 'Private'), (b'MIXED', 'Mixed'), (b'OTHERS', 'Others')])),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_actived', models.BooleanField(default=False, verbose_name='Actived')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name': 'Association',
                'verbose_name_plural': 'Associations',
                'permissions': (('association', 'Can ALL association'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('logo', models.ImageField(default=b'enterprises/default.png', upload_to=b'enterprises', verbose_name='Logo')),
                ('tax_id', models.CharField(max_length=50, verbose_name='Tax id')),
                ('type_e', models.CharField(default=b'PRIVATE', max_length=10, verbose_name='Type', choices=[(b'GOVERMENT', 'Government'), (b'PRIVATE', 'Private'), (b'MIXED', 'Mixed'), (b'OTHERS', 'Others')])),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_actived', models.BooleanField(default=False, verbose_name='Actived')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name': 'Enterprise',
                'verbose_name_plural': 'Enterprises',
                'permissions': (('enterprise', 'Can ALL enterprise'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Headquar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('phone', models.CharField(max_length=50, null=True, verbose_name='Phone', blank=True)),
                ('address', models.TextField(null=True, verbose_name='Address', blank=True)),
                ('is_main', models.BooleanField(default=False, verbose_name='Main')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_actived', models.BooleanField(default=False, verbose_name='Actived')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('association', models.ForeignKey(verbose_name='Association', blank=True, to='space.Association', null=True)),
                ('enterprise', models.ForeignKey(verbose_name='Enterprise', to='space.Enterprise')),
            ],
            options={
                'verbose_name': 'Headquar',
                'verbose_name_plural': 'Headquars',
                'permissions': (('headquar', 'Can ALL headquar(sedes)'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('price', models.FloatField(null=True, verbose_name='Price', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('test_image', models.ImageField(default=b'test_images/default.png', upload_to=b'test_images', null=True, verbose_name='Test image', blank=True)),
                ('test_date', models.DateTimeField(null=True, verbose_name='Test date', blank=True)),
            ],
            options={
                'verbose_name': 'Solution',
                'verbose_name_plural': 'Solutions',
                'permissions': (('solution', 'Can ALL solution'),),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='solution',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='headquar',
            unique_together=set([('name', 'enterprise')]),
        ),
        migrations.AddField(
            model_name='enterprise',
            name='solution',
            field=models.ForeignKey(verbose_name='Solution', blank=True, to='space.Solution', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='enterprise',
            unique_together=set([('name', 'tax_id')]),
        ),
        migrations.AddField(
            model_name='association',
            name='solution',
            field=models.ForeignKey(verbose_name='Solution', blank=True, to='space.Solution', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='association',
            unique_together=set([('name',)]),
        ),
    ]
