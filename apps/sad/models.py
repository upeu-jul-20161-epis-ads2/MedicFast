# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     auth
@Descripcion Definición de los modelos
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst, get_text_list
from django.dispatch import receiver
from django.db.models import signals
from unicodedata import normalize
from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS
import datetime
# models
from django.contrib.auth.models import AbstractUser# managers
from .managers import UserManager
from apps.params.models import Person
from django.contrib.auth.models import Group, Permission
from apps.space.models import Solution, Association, Enterprise, Headquar



# others


# TODO Is done por ahora


ON = 'ON'
OFF = 'OFF'
USER_STATUS_CHOICES = (
    (ON, _('Activate')),
    (OFF, _('Deactivate')),

)


class User(AbstractUser):

    """
    Tabla para usuarios
    """

    class Meta:
        # swappable = 'AUTH_USER_MODEL' #ver django-angular-seed
        verbose_name = capfirst(_('user'))
        verbose_name_plural = capfirst(_('users'))
        permissions = (
            ('user', 'Can ALL user'),
        )
        db_table = 'auth_user'

    # comentar desde aqui
    last_headquar_id = models.CharField(max_length=50, null=True, blank=True)
    last_module_id = models.CharField(max_length=50, null=True, blank=True)
    person = models.OneToOneField(
        Person, verbose_name=_('Person'), null=True, blank=True,
        # unique=True OneToOneField ya es unico
        # related_name='user'
    )
    # hgroups = models.ManyToManyField(Group, verbose_name=_(u'groups'),
    #                                   through='UserHeadquar',
    # related_name='users_as_group', null=True, blank=True)

    objects = UserManager()  # override the default manager

    def __str__(self):
        return self.username

    '''
    def validate_unique(self, exclude=None):

        raise ValidationError(
            {
                NON_FIELD_ERRORS:
                ('Person with same ... already exists.',)
            }
        )
        super(User, self).validate_unique(exclude=exclude)
    '''
    '''
    def clean(self):
        #raise ValidationError('foo must not be empty')
        raise ValidationError(
            {
                'identity_num':
                ('Person with same ... already exists.',)
            }
        )
    '''

    '''
    def save(self, *args, **kwargs):
        # TODO Mandar con Exception no con ValidationError
        if Person.objects.exclude(id=self.person.id).filter(identity_type=self.person.identity_type, identity_num=self.person.identity_num).count() > 0:
            raise ValidationError({
                'identity_num':
                (_(u'%(model_name)s with this %(field_label)s already exists.') % {
                    'model_name': _('Person'),
                    'field_label': get_text_list( (capfirst(_('number')), capfirst(_('Type')) ),_('and') ),
                },),
            })
        return super(User, self).save(*args, **kwargs)
    '''
    '''
    def validate_unique(self, exclude=None):
        # if self.person:
        if Person.objects.exclude(id=self.person.id).filter(identity_type=self.person.identity_type, identity_num=self.person.identity_num).count() > 0:
            raise ValidationError({
                'identity_num':
                (_(u'%(model_name)s with this %(field_label)s already exists.') % {
                    'model_name': _('Person'),
                    'field_label': get_text_list( (capfirst(_('number')), capfirst(_('Type')) ),_('and') ),
                },),
            })

        return super(User, self).validate_unique(exclude=exclude)
    '''
    '''
    def save(self, *args, **kwargs):
        pk = self.pk
        if self.person:
            self.first_name = self.person.first_name
            self.last_name = self.person.last_name

        super(User, self).save(*args, **kwargs)
        if not pk: # solo despues de crear un nuevo usuario
            UserStatus.objects.create(description='alta', user=self)
    '''


def user_pre_save(sender, instance, raw, **kwargs):
    instance.last_login = datetime.datetime.now()
    if instance.person:
        instance.first_name = instance.person.first_name
        instance.last_name = instance.person.last_name


@receiver(signals.post_save, sender=User)
def user_post_save(sender, instance, created, raw, **kwargs):
    if created:  # solo despues de crear un nuevo usuario
        UserStatus.objects.create(description='Alta', user=instance)

signals.pre_save.connect(user_pre_save, sender=User)
#signals.post_save.connect(user_post_save, sender=User)


class UserStatus(models.Model):

    """
    Tabla para el historial de los estados de los usuarios
    """

    status = models.CharField(
        _('Status'), max_length=50, choices=USER_STATUS_CHOICES, default=ON
    )
    description = models.TextField(_('Description'), null=True, blank=True)
    # related_name=userstatus_set
    user = models.ForeignKey(User, verbose_name=capfirst(_('user')))
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _('User status')
        verbose_name_plural = _('User statuses')
        db_table = 'sad_user_status'

    def __str__(self):
        return '%s %s' % (self.user.username, self.status)


INPUT = "INPUT"
OUTPUT = "OUTPUT"

ACCESS_TYPE_CHOICES = (
    (INPUT, "Input"),
    (OUTPUT, "Output"),

)


class Access(models.Model):

    """
    Tabla que registra los accesos de los usuarios al sistema
    """

    access_type = models.CharField(
        _('Access type'),
        max_length=50, choices=ACCESS_TYPE_CHOICES, default=INPUT)
    ip = models.CharField(_('IP'), max_length=50, null=True, blank=True)
    session_key = models.TextField(_('Session key'), null=True, blank=True)

    user = models.ForeignKey(User, verbose_name=capfirst(_('user')))
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Access')
        verbose_name_plural = _('Accesses')
        permissions = (
            ("access", "Can ALL access"),
        )

    def __str__(self):
        return "%s %s" % (self.user.username, self.access_type)

PRO = 'PRO'
WEB = 'WEB'
VENTAS = 'VENTAS'
BACKEND = 'BACKEND'
HOTEL = 'HOTEL'
MODULE_CHOICES = (
    (PRO, 'Profesional'),
    (WEB, 'Web informativa'),
    (VENTAS, 'Ventas'),
    (BACKEND, 'Backend Manager'),
    (HOTEL, 'Hotel'),
)


class Module(models.Model):

    """
    Modulos del sistema
    """

    module = models.CharField(
        _('Module'), max_length=50, choices=MODULE_CHOICES, default=BACKEND)
    name = models.CharField(capfirst(_('name')), max_length=50)
    is_active = models.BooleanField(capfirst(_('active')), default=True)
    icon = models.CharField(_('Icon'), max_length=50, null=True, blank=True)
    description = models.TextField(_('Description'), null=True, blank=True)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    solutions = models.ManyToManyField(
        Solution, verbose_name=_('Solutions'), null=True, blank=True)  # , through='ModuleSolution'

    groups = models.ManyToManyField(
        Group, related_name='module_set', verbose_name=capfirst(_('groups')),
        null=True, blank=True)  # , through='ModuleGroup'
    # related_name cambia module_set x initial_groups_module_set
    initial_groups = models.ManyToManyField(
        Group, related_name='initial_groups_module_set',
        verbose_name=_('Initial groups'), null=True, blank=True)  # , through='ModuleInitialGroup'

    class Meta:

        ordering = ['-id', ]
        verbose_name = _('Module')
        verbose_name_plural = _('Modules')
        permissions = (
            ('module', 'Can ALL module'),
        )
        unique_together = ('module', 'name',)

    def __str__(self):
        return '%s (%s)' % (self.name, dict((x, y)
                                            for x, y in MODULE_CHOICES)[self.module])

    def validate_unique(self, exclude=None):
        if normalize('NFKD', self.name).encode('ascii', 'ignore').lower() in list(
            normalize('NFKD', c['name']).encode('ascii', 'ignore').lower()
            for c in self.__class__.objects.values('name').exclude(pk=self.pk).filter(module=self.module)
        ):
            raise ValidationError({
                'name':
                (_(u'%(model_name)s with this %(field_label)s already exists.') % {
                    'model_name': '%s "%s"' % (capfirst(_('Module')) + '', dict(MODULE_CHOICES).get(self.module)),
                    'field_label': capfirst(_('name')),
                }, ),
            })
        super(Module, self).validate_unique(exclude=exclude)


class Menu(models.Model):

    """
    Menus del sistema
    """

    module = models.CharField(
        _('Module'), max_length=50, choices=MODULE_CHOICES, default=BACKEND)
    title = models.CharField(capfirst(_('title')), max_length=50)
    url = models.CharField(max_length=150, default='#')
    pos = models.IntegerField(_('Position'), default=1)
    icon = models.CharField(
        _('Icon'), max_length=50, null=True, blank=True, default='')
    is_active = models.BooleanField(capfirst(_('active')), default=True)
    description = models.TextField(_('Description'), null=True, blank=True)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    permission = models.ForeignKey(
        Permission, verbose_name=_('permission'), null=True, blank=True)
    # related_name='parent',
    parent = models.ForeignKey(
        'self', verbose_name=_('Parent'), null=True, blank=True)

    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menus')
        permissions = (
            ('menu', 'Can ALL menu'),
        )

    def __str__(self):
        return '%s (%s)' % (self.title, dict((x, y)
                                             for x, y in MODULE_CHOICES)[self.module])


class UserEnterprise(models.Model):

    """
    Permisos a nivel de empresa
    """
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    user = models.ForeignKey(User, verbose_name=_('user'))
    group = models.ForeignKey(Group, verbose_name=_('group'))
    enterprise = models.ForeignKey(Enterprise, verbose_name=_('Enterprise'))

    class Meta:
        verbose_name = _('User enterprise')
        verbose_name_plural = _('User enterprises')
        db_table = 'sad_user_enterprise'

    def __str__(self):
        return '%s %s - %s' % (self.user.username, self.enterprise.name,
                               self.group.name)


class UserHeadquar(models.Model):

    """
    Permisos a nivel de sede headquar
    """
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    user = models.ForeignKey(User, verbose_name=_('user'))
    group = models.ForeignKey(Group, verbose_name=_('group'))
    headquar = models.ForeignKey(Headquar, verbose_name=_('Headquar'))

    class Meta:
        verbose_name = _('User headquar')
        verbose_name_plural = _('User headquars')
        db_table = 'sad_user_headquar'

    def __str__(self):
        return '%s %s %s - %s' % (self.user.username, self.headquar.name,
                                  self.headquar.enterprise.name, self.group.name)


class UserAssociation(models.Model):

    """
    Permisos a nivel de association
    """
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    user = models.ForeignKey(User, verbose_name=_('user'))
    group = models.ForeignKey(Group, verbose_name=_('group'))
    association = models.ForeignKey(Association, verbose_name=_('Association'))

    class Meta:
        verbose_name = _('User association')
        verbose_name_plural = _('User association')
        db_table = 'sad_user_association'

    def __str__(self):
        return '%s %s - %s' % (self.user.username, self.association.name,
                               self.group.name)


class Ticket(models.Model):

    """
    Tabla para impresiones de tickets
    """
    text = models.CharField(_('Text'), max_length=150, null=True, blank=True)
    row = models.IntegerField(_('Row'), default=1)

    user = models.ForeignKey(
        User, verbose_name=_('user'), null=True, blank=True)

    class Meta:
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')
        permissions = (
            ('ticket', 'Can ALL ticket'),
        )

    def __str__(self):
        return '%s %s' % (self.user.username, self.text)


class Backup(models.Model):

    """
    Tabla para registro de las copias de la db
    """

    file_name = models.CharField(_('File name'), max_length=50)
    description = models.TextField(_('Description'), null=True, blank=True)
    size = models.CharField(_('Size'), max_length=50, null=True, blank=True)

    user = models.ForeignKey(User, verbose_name=_('user'))
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Backup')
        verbose_name_plural = _('Backups')
        permissions = (
            ('backup', 'Can ALL backup'),
        )

    def __str__(self):
        return self.file_name


''' 
Mantener esto desactivado hasta poner en producción
Modelos que se usan solo para cambiar el verbose_name de las relaciones.
Desactivar antes de hacer una migración a sad o un backup
$python manage.py makemigrations sad
$python manage.py migrate sad

$python manage.py dumpdata > fixtures/backup_datayyyymmdd.json


class GroupPermission(models.Model):

    """ """
    permission = models.ForeignKey(
        Permission, verbose_name=capfirst(_('permission')), null=True, blank=True)
    group = models.ForeignKey(
        Group, verbose_name=capfirst(_('group')), null=True, blank=True)

    class Meta:
        verbose_name = _('Group-permission')
        verbose_name_plural = _('Group-permissions')
        db_table = 'auth_group_permissions'

    def __str__(self):
        return '%s-%s' % (self.group, self.permission.codename)


class UserGroup(models.Model):

    """ """
    user = models.ForeignKey(
        User, verbose_name=capfirst(_('user')), null=True, blank=True)
    group = models.ForeignKey(
        Group, verbose_name=capfirst(_('group')), null=True, blank=True)

    class Meta:
        verbose_name = _('User-group')
        verbose_name_plural = _('User-groups')
        db_table = 'auth_user_groups'

    def __str__(self):
        return '%s-%s' % (self.user, self.group)

class ModuleSolution(models.Model):

    """
    Solo para cambiar el mensaje de 
    Module-group relationship: "Module_initial_groups object" para
    Module-group: "Backend-MASTER"
    """
    module = models.ForeignKey(
        Module, verbose_name=_('Module'), null=True, blank=True)
    solution = models.ForeignKey(
        Solution, verbose_name=_('Solution'), null=True, blank=True)

    class Meta:
        verbose_name = _('Module-solution')
        verbose_name_plural = _('Module-solutions')
        db_table = 'sad_module_solutions'

    def __str__(self):
        return '%s-%s' % (self.module, self.solution)


class ModuleGroup(models.Model):

    """ """
    module = models.ForeignKey(
        Module, verbose_name=_('Module'), null=True, blank=True)
    group = models.ForeignKey(
        Group, verbose_name=capfirst(_('group')), null=True, blank=True)

    class Meta:
        verbose_name = _('Module-group')
        verbose_name_plural = _('Module-groups')
        db_table = 'sad_module_groups'

    def __str__(self):
        return '%s-%s' % (self.module, self.group)


class ModuleInitialGroup(models.Model):

    """ """
    module = models.ForeignKey(
        Module, verbose_name=_('Module'), null=True, blank=True)
    group = models.ForeignKey(
        Group, verbose_name=capfirst(_('group')), null=True, blank=True)

    class Meta:
        verbose_name = _('Module-initial group')
        verbose_name_plural = _('Module-initial groups')
        db_table = 'sad_module_initial_groups'

    def __str__(self):
        return '%s-%s' % (self.module, self.group)

'''
