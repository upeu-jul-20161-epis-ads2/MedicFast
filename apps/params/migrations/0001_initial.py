# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identity_type', models.CharField(default=b'NID', max_length=10, verbose_name='Identity type', choices=[(b'NID', 'N.I.D.'), (b'FC', 'Foreign card'), (b'CB', 'Certificate birth'), (b'OTHER', 'Other')])),
                ('identity_num', models.CharField(blank=True, max_length=20, null=True, verbose_name='Identity num', error_messages={b'unique': b'eeeee ee'})),
                ('first_name', models.CharField(max_length=50, null=True, verbose_name='First name', blank=True)),
                ('last_name', models.CharField(max_length=50, null=True, verbose_name='Last name', blank=True)),
                ('birth_date', models.DateField(null=True, verbose_name='birth date', blank=True)),
                ('photo', models.ImageField(default=b'persons/default.png', upload_to=b'persons', null=True, verbose_name='Photo', blank=True)),
                ('photo2', models.ImageField(default=b'persons/default.png', upload_to=b'persons', null=True, verbose_name='Photo2', blank=True)),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'Persons',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='person',
            unique_together=set([('first_name', 'last_name', 'identity_type', 'identity_num'), ('identity_type', 'identity_num')]),
        ),
    ]
