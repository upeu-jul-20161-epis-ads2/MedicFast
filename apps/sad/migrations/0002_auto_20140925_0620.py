# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0001_initial'),
        ('auth', '0001_initial'),
        ('params', '0001_initial'),
        ('sad', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Access',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('access_type', models.CharField(default=b'INPUT', max_length=50, verbose_name='Access type', choices=[(b'INPUT', b'Input'), (b'OUTPUT', b'Output')])),
                ('ip', models.CharField(max_length=50, null=True, verbose_name='IP', blank=True)),
                ('session_key', models.TextField(null=True, verbose_name='Session key', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Access',
                'verbose_name_plural': 'Accesses',
                'permissions': (('access', 'Can ALL access'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Backup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=50, verbose_name='File name')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('size', models.CharField(max_length=50, null=True, verbose_name='Size', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Backup',
                'verbose_name_plural': 'Backups',
                'permissions': (('backup', 'Can ALL backup'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('module', models.CharField(default=b'BACKEND', max_length=50, verbose_name='Module', choices=[(b'PRO', b'Profesional'), (b'WEB', b'Web informativa'), (b'VENTAS', b'Ventas'), (b'BACKEND', b'Backend Manager')])),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('url', models.CharField(default=b'#', max_length=150)),
                ('pos', models.IntegerField(default=1, max_length=50, verbose_name='Position')),
                ('icon', models.CharField(default=b'', max_length=50, null=True, verbose_name='Icon', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('parent', models.ForeignKey(verbose_name='Parent', blank=True, to='sad.Menu', null=True)),
                ('permission', models.ForeignKey(verbose_name='permission', blank=True, to='auth.Permission', null=True)),
            ],
            options={
                'verbose_name': 'Menu',
                'verbose_name_plural': 'Menus',
                'permissions': (('menu', 'Can ALL menu'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('module', models.CharField(default=b'BACKEND', max_length=50, verbose_name='Module', choices=[(b'PRO', b'Profesional'), (b'WEB', b'Web informativa'), (b'VENTAS', b'Ventas'), (b'BACKEND', b'Backend Manager')])),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('icon', models.CharField(max_length=50, null=True, verbose_name='Icon', blank=True)),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('groups', models.ManyToManyField(related_name=b'module_set', null=True, verbose_name='Groups', to='auth.Group', blank=True)),
                ('initial_groups', models.ManyToManyField(related_name=b'initial_groups_module_set', null=True, verbose_name='Initial groups', to='auth.Group', blank=True)),
                ('solutions', models.ManyToManyField(to='space.Solution', null=True, verbose_name='Solutions', blank=True)),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name': 'Module',
                'verbose_name_plural': 'Modules',
                'permissions': (('module', 'Can ALL module'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=150, null=True, verbose_name='Text', blank=True)),
                ('row', models.IntegerField(default=1, verbose_name='Row')),
                ('user', models.ForeignKey(verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
                'permissions': (('ticket', 'Can ALL ticket'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserAssociation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('association', models.ForeignKey(verbose_name='Association', to='space.Association')),
                ('group', models.ForeignKey(verbose_name='group', to='auth.Group')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'sad_user_association',
                'verbose_name': 'User association',
                'verbose_name_plural': 'User association',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserEnterprise',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('enterprise', models.ForeignKey(verbose_name='Enterprise', to='space.Enterprise')),
                ('group', models.ForeignKey(verbose_name='group', to='auth.Group')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'sad_user_enterprise',
                'verbose_name': 'User enterprise',
                'verbose_name_plural': 'User enterprises',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserHeadquar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('group', models.ForeignKey(verbose_name='group', to='auth.Group')),
                ('headquar', models.ForeignKey(verbose_name='Headquar', to='space.Headquar')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'sad_user_headquar',
                'verbose_name': 'User headquar',
                'verbose_name_plural': 'User headquars',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'ON', max_length=50, verbose_name='Status', choices=[(b'ON', 'Activate'), (b'OFF', 'Deactivate')])),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'sad_user_status',
                'verbose_name': 'User status',
                'verbose_name_plural': 'User statuses',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='module',
            unique_together=set([('module', 'name')]),
        ),
        migrations.AddField(
            model_name='user',
            name='last_headquar_id',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='last_module_id',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='person',
            field=models.OneToOneField(null=True, blank=True, to='params.Person', verbose_name='Person'),
            preserve_default=True,
        ),
    ]
