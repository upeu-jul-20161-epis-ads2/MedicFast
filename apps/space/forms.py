# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     space

Descripcion: Implementacion de los formularios de la app space
"""
from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.text import capfirst
#from django.core.exceptions import ValidationError
from django.contrib import messages

from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab, \
    PrependedAppendedText, PrependedText

from apps.utils.forms import smtSave, btnCancel, btnReset
#from apps.utils.forms import Submit, Button, Reset

# models
from .models import Solution, Association, Enterprise, Headquar

# others
from django.utils.timezone import get_current_timezone
from datetime import datetime

# from django.contrib.admin import widgets
# https://docs.djangoproject.com/en/dev/topics/i18n/translation/
#from django.core.exceptions import NON_FIELD_ERRORS

# TODO Is done por ahora


class HeadquarAssociationForm(forms.ModelForm):

    """ """
    class Meta:
        model = Headquar
        fields = []  # 'association',

    def __init__(self, *args, **kwargs):
        super(HeadquarAssociationForm, self).__init__(*args, **kwargs)
        self.fields['association_name'] = forms.CharField(
            label=capfirst(_(u'Association')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.helper = FormHelper()
        self.helper.form_id = 'form'
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(

            Row(
                Div(Field('association_name', css_class='input-required',
                    autocomplete='off'),
                    css_class='col-md-6'),

            ),
            # Row(
            #    Div(Field('association',),
            #        css_class='col-md-6'),
            #),

            Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                    btnReset(),
                ),
            ),
        )


class HeadquarForm(forms.ModelForm):

    """ """
    class Meta:
        model = Headquar
        fields = ['name', 'phone', 'address', ]

    def __init__(self, *args, **kwargs):
        super(HeadquarForm, self).__init__(*args, **kwargs)
        self.fields['name'].help_text=u'<small class="help-error"></small> %s' % _(
                u' ')
        self.fields['phone'].help_text=u'<small class="help-error"></small> %s' % _(
                u' ')
        self.fields['address'].widget.attrs = {'rows': 3, }

        self.helper = FormHelper()
        self.helper.form_id = 'form'
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(

            Row(
                Div(Field('name', css_class='input-required'),
                    css_class='col-md-6'),
                Div(Field('phone', css_class='input-integer' ),
                    css_class='col-md-6'),
            ),
            Row(
                Div(Field('address',),
                    css_class='col-md-6'),
            ),

            Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                    btnReset(),
                ),
            ),
        )


class EnterpriseForm(forms.ModelForm):

    """ """
    class Meta:
        model = Enterprise
        fields = ['name', 'logo', 'tax_id', 'type_e', 'solution', ]

    def __init__(self, *args, **kwargs):
        self.create = kwargs.pop('create', None)

        super(EnterpriseForm, self).__init__(*args, **kwargs)
        self.fields['name'].help_text=u'<small class="help-error"></small> %s' % _(
                u' ')
        self.fields['tax_id'].help_text=u'<small class="help-error"></small> %s' % _(
                u' ')

        if self.create:
            self.fields['sede'] = forms.CharField(
                label=capfirst(_(u'Sede')), required=True,
                initial='Principal',
                help_text=u'<small class="help-error"></small> %s' % _(
                    u' '),
                 widget=forms.TextInput(attrs={'class': 'input-required', }),
            )
        else:
            self.fields['sede'] = forms.CharField(
                widget=forms.HiddenInput(), required=False)

        self.fields['logo'].help_text = u'<small class="help-error"></small> %s' % _(
            u'Available formats are JPG, GIF, and PNG.')
        self.fields['solution'].required = True
        self.fields['solution'].help_text = u'<small class="help-error"></small> %s' % _(
            u' ')

        self.helper = FormHelper()
        self.helper.form_id = 'form'
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(

            TabHolder(
                Tab(_('Enterprise'),
                    Row(

                        Div(Field('tax_id', css_class='input-required',
                            autofocus=True),
                    css_class='col-md-6'),
                    ),
                    Row(
                        Div(Field('name', css_class='input-required'),
                    css_class='col-md-6'),
                        Div(Field('type_e', css_class='input-required'),
                            css_class='col-md-6'),
                    ),
                    Row(
                        Div(Field('solution', css_class='input-required',),
                            css_class='col-md-6'),
                        Div(Field('sede', ),
                            css_class='col-md-6'),
                    ),


                    ),
                Tab(_('Image'),
                    Field('logo', css_class="")
                    ),
            ),
            Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                    btnReset(),
                ),
            ),
        )


class AssociationForm(forms.ModelForm):

    """ """
    class Meta:
        model = Association
        fields = ['name', 'type_a', 'solution', 'logo', ]

    def __init__(self, *args, **kwargs):
        super(AssociationForm, self).__init__(*args, **kwargs)
        self.fields['name'].help_text = u'<small class="help-error"></small> %s' % _(
            u' ')
        self.fields['solution'].required = True
        self.fields['solution'].help_text = u'<small class="help-error"></small> %s' % _(
            u' ')
        self.fields['logo'].help_text = u'<small class="help-error"></small> %s' % _(
            u'Available formats are JPG, GIF, and PNG.')

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(
            TabHolder(
                Tab(_('Association'),
                    Row(
                    Div(Field('name', css_class='input-required'),
                    css_class='col-md-6'),
                    Div(Field('type_a', css_class='input-required'),
                    css_class='col-md-6'),
                    ),
                    Row(
                    Div(Field('solution', css_class='input-required'),
                    css_class='col-md-6'),
                    ),
                    ),
                Tab(_('Image'),
                    Row(
                    Div(Field('logo', css_class=''),
                        css_class='col-md-6'),
                    ),
                    ),
            ),
            Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                    btnReset(),
                ),
            ),
        )


class SolutionForm(forms.ModelForm):

    """ """
    class Meta:
        model = Solution
        fields = ['name', 'description', 'price', 'test_date', 'test_image', ]

    def __init__(self, *args, **kwargs):
        super(SolutionForm, self).__init__(*args, **kwargs)
        '''
        self.fields['name'] = forms.CharField(
            label=capfirst(_(u'name')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['description'] = forms.CharField(
            label=_(u'Description'), required=False,
            widget=forms.Textarea(attrs={'rows': 3, }),
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['test_image'] = forms.ImageField(
            label=capfirst(_(u'Test image')), required=False,
            initial='test_images/default.png',
            help_text=u'<small class="help-error"></small> %s' % _(
                u'Available formats are JPG, GIF, and PNG.'),
        )
        '''
        self.fields['name'].help_text = u'<small class="help-error"></small> %s' % _(
            u' ')
        self.fields['description'].help_text = u'<small class="help-error"></small> %s' % _(
            u' ')
        self.fields['description'].widget.attrs = {'rows': 3, }
        self.fields['test_image'].help_text = u'<small class="help-error"></small> %s' % _(
            u'Available formats are JPG, GIF, and PNG.')
        self.fields['price'].help_text = u'<small class="help-error"></small> %s' % _(
            u' ')

        self.fields['test_date'] = forms.DateTimeField(
            label=_(u'Test date'), required=False,
            initial=datetime.now().replace(tzinfo=get_current_timezone()),
            widget=forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S',),
            input_formats=(
                '%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y', '%Y-%m-%d',
                '%Y-%m-%d %H:%M:%S'),
            help_text=u'<small class="help-error"></small> %s' % _(
                u'Some useful help text.'),
        )
        self.helper = FormHelper()
        #self.helper.form_tag = False
        # http://bixly.com/blog/awesome-forms-django-crispy-forms/
        self.helper.form_method = 'post'
        self.helper.form_class = 'js-validate form-vertical'
        #self.helper.form_show_labels = False
        #self.fields['name'].label = False
        self.helper.layout = Layout(
            Row(
                Div(Field('name', css_class='input-required'),
                    css_class='col-md-6'),
                Div(Field('description', css_class=''),
                    css_class='col-md-6'),
            ),
            Row(
                Div(Field('price', css_class='input-numeric mask-num'),
                    css_class='col-md-6'),
                Div(Field('test_date', css_class='input-datex'),
                    css_class='col-md-6'),  # falta validar un input-datetime
            ),
            Row(
                Div(Field('test_image', css_class=''),
                    css_class='col-md-6'),
            ),
            Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                    btnReset(),
                ),
            ),
        )
