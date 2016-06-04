# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     space

Descripcion: Registro de los modelos de la app space
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from django.dispatch import receiver
from django.db.models import signals
from unicodedata import normalize
from django.core.exceptions import ValidationError

# models
#from apps.params.models import Locality

# managers
#from .managers import SolutionManager

# others
#from django.utils import timezone
#from django.core.exceptions import NON_FIELD_ERRORS
#from django.template.defaultfilters import slugify

GOVERMENT = 'GOVERMENT'
PRIVATE = 'PRIVATE'
MIXED = 'MIXED'
OTHERS = 'OTHERS'
TYPE_CHOICES = (
    (GOVERMENT, _('Government')),
    (PRIVATE, _('Private')),
    (MIXED, _('Mixed')),
    (OTHERS, _('Others'))
)


def unique_name(value):
    if value == 'angel':
        raise ValidationError(u'%s is not an angel' % value)


class Solution(models.Model):

    """
    Tabla que contiene las soluciones o planes o servicios del sistema
    """
    name = models.CharField(capfirst(_('name')), max_length=50)
    description = models.TextField(_('Description'), null=True, blank=True)
    price = models.FloatField(_('Price'), null=True, blank=True)
    is_active = models.BooleanField(capfirst(_('active')), default=True)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    test_image = models.ImageField(
        _('Test image'), upload_to='test_images',
        default='test_images/default.png', null=True, blank=True)
    test_date = models.DateTimeField(_('Test date'),
                                     null=True, blank=True)

    class Meta:
        verbose_name = _('Solution')
        verbose_name_plural = _('Solutions')
        permissions = (
            ('solution', 'Can ALL solution'),
        )
        unique_together = ('name',)

    def __str__(self):
        return self.name

    def validate_unique(self, exclude=None):
        if normalize('NFKD', self.name).encode('ascii', 'ignore').lower() in list(
            normalize('NFKD', c['name']).encode('ascii', 'ignore').lower()
            for c in self.__class__.objects.values('name').exclude(pk=self.pk)
        ):
            raise ValidationError({
                'name':
                (_(u'%(model_name)s with this %(field_label)s already exists.') % {
                'model_name': _('Solution'),
                'field_label': capfirst(_('name')),
                },),
            })

        super(Solution, self).validate_unique(exclude=exclude)


class Association(models.Model):

    """
    Tabla que contiene las asociaciones suscritas a un plan
    """

    name = models.CharField(capfirst(_('name')), max_length=50)
    logo = models.ImageField(
        _('Logo'),
        upload_to='associations', default='associations/default.png')
    type_a = models.CharField(
        _('Type'),
        max_length=10, choices=TYPE_CHOICES, default=PRIVATE)
    is_active = models.BooleanField(capfirst(_('active')), default=True)
    is_actived = models.BooleanField(_('Actived'), default=False)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    solution = models.ForeignKey(
        Solution, verbose_name=_('Solution'), null=True, blank=True)

    class Meta:
        verbose_name = _('Association')
        verbose_name_plural = _('Associations')
        permissions = (
            ('association', 'Can ALL association'),
        )
        unique_together = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if normalize('NFKD', u'%s' % self.name).encode('ascii', 'ignore').lower() in list(
                normalize('NFKD', u'%s' % c['name']).encode('ascii', 'ignore').lower() for c in Association.objects.values('name').exclude(pk=self.pk)
        ):
            raise Exception(_(u'%(model_name)s with this %(field_label)s already exists.') % {
                'model_name': _('Association'),
                'field_label': capfirst(_(u'name')),
            })
        super(Association, self).save(*args, **kwargs)


class Enterprise(models.Model):

    """
    Tabla que contiene las empresas suscritas a un plan
    """

    name = models.CharField(capfirst(_('name')), max_length=50)
    #name_sm = models.CharField(capfirst(_('siglas')), max_length=50)
    logo = models.ImageField(
        _('Logo'), upload_to='enterprises', default='enterprises/default.png')
    tax_id = models.CharField(_('Tax id'), max_length=50)
    type_e = models.CharField(
        _('Type'),
        max_length=10, choices=TYPE_CHOICES, default=PRIVATE)
    is_active = models.BooleanField(capfirst(_('active')), default=True)
    is_actived = models.BooleanField(_('Actived'), default=False)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    solution = models.ForeignKey(
        Solution, verbose_name=_('Solution'), null=True, blank=True)

    class Meta:
        verbose_name = _('Enterprise')
        verbose_name_plural = _('Enterprises')
        permissions = (
            ('enterprise', 'Can ALL enterprise'),
        )
        # no duplicate name, no duplicate tax_id
        unique_together = ('name', 'tax_id',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if normalize('NFKD', u'%s' % self.name).encode('ascii', 'ignore').lower() in list(
                normalize('NFKD', u'%s' % c['name']).encode('ascii', 'ignore').lower() for c in Enterprise.objects.values('name').exclude(pk=self.pk)
        ):
            raise Exception(_(u'%(model_name)s with this %(field_label)s already exists.') % {
                'model_name': _('Enterprise'),
                'field_label': capfirst(_(u'name')),
            })
        if Enterprise.objects.exclude(pk=self.pk).filter(tax_id=self.tax_id).count() > 0:
            raise Exception(_(u'%(model_name)s with this %(field_label)s already exists.') % {
                'model_name': _('Enterprise'),
                'field_label': capfirst(_(u'Tax id')),
            })
        super(Enterprise, self).save(*args, **kwargs)


class Headquar(models.Model):

    """
    Tabla que contiene las sedes de las empresas, asociadas a una Asociación
    Un Headquar o sede o sucursal, es la unidad principal del sistema
    Los accesos del sistema serán entregados a un Headquarters
    """
    name = models.CharField(capfirst(_('name')), max_length=50)

    phone = models.CharField(_('Phone'), max_length=50, null=True, blank=True)

    address = models.TextField(_('Address'), null=True, blank=True)
    is_main = models.BooleanField(_('Main'), default=False)
    is_active = models.BooleanField(capfirst(_('active')), default=True)
    is_actived = models.BooleanField(_('Actived'), default=False)

    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    # locality = models.ForeignKey(Locality, verbose_name=_('Locality'),
    #	null=True, blank=True)
    association = models.ForeignKey(
        Association, verbose_name=_('Association'), null=True, blank=True)
    enterprise = models.ForeignKey(Enterprise, verbose_name=_('Enterprise'))

    class Meta:
        verbose_name = _('Headquar')
        verbose_name_plural = _('Headquars')
        permissions = (
            ('headquar', 'Can ALL headquar(sedes)'),
        )
        # no duplicate name by enterprise
        unique_together = (('name', 'enterprise'),)

    def __str__(self):
        return '%s %s (%s)' % (self.name, self.enterprise, self.association)

    def save(self, *args, **kwargs):
        if normalize('NFKD', u'%s' % self.name).encode('ascii', 'ignore').lower() in list(
                normalize('NFKD', u'%s' % c['name']).encode('ascii', 'ignore').lower() for c in Headquar.objects.values('name').exclude(pk=self.pk).filter(enterprise=self.enterprise)
        ):
            raise Exception(_(u'%(model_name)s with this %(field_label)s already exists.') % {
                'model_name': _('Headquar'),
                'field_label': capfirst(_(u'name')),
            })
        super(Headquar, self).save(*args, **kwargs)
