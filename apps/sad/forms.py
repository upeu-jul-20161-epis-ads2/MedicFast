# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     sad

Descripcion: Implementacion de los formularios de la app sad
"""
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst, get_text_list
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Field, Div, Row, HTML
from crispy_forms.bootstrap import FormActions, TabHolder, Tab

from apps.utils.forms import smtSave, btnCancel, btnReset

# models
from .models import Module, MODULE_CHOICES, Menu, User, UserStatus, ON, OFF
from django.contrib.auth.models import Permission, Group
from apps.space.models import Headquar, Solution
from apps.params.models import Person, IDENTITY_TYPE_CHOICES

# otros
from unicodedata import normalize
from apps.utils.security import UserToken
from django.db.models import Q
from django.core.exceptions import NON_FIELD_ERRORS

# TODO Falta corregir 01 mensaje

class UserDetailForm(forms.ModelForm):

    """ """

    class Meta:
        model = User
        fields = ['is_superuser', 'is_staff', 'is_active', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)

        super(UserDetailForm, self).__init__(*args, **kwargs)

        self.fields['username'] = forms.CharField(
            label=capfirst(_(u'username')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['email'] = forms.CharField(
            label=capfirst(_(u'email')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['first_name'] = forms.CharField(
            label=capfirst(_(u'first name')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['last_name'] = forms.CharField(
            label=capfirst(_(u'last name')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['identity_type'] = forms.ChoiceField(
            label=capfirst(_(u'Identity type')), required=True,
            # widget=forms.RadioSelect(),
            choices=IDENTITY_TYPE_CHOICES,

            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['identity_num'] = forms.CharField(
            label=capfirst(_(u'number')), required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['photo'] = forms.ImageField(
            label=capfirst(_(u'Photo')), required=False,
            initial='persons/default.png',
            help_text=u'<small class="help-error"></small> %s' % _(
                u'Available formats are JPG, GIF, and PNG.'),
        )

        self.fields['hgroups'] = forms.CharField(
            label=u'%s %s' % (capfirst(_(u'groups')), capfirst(_(u'Headquar'))),
        )
        self.fields['egroups'] = forms.CharField(
            label=u'%s %s' % (
                capfirst(_(u'groups')), capfirst(_(u'Enterprise'))),
        )
        self.fields['agroups'] = forms.CharField(
            label=u'%s %s' % (
                capfirst(_(u'groups')), capfirst(_(u'Association'))),
        )
        self.fields['status'] = forms.CharField(
            label=u'%s %s' % (capfirst(_(u'status')), capfirst(_(u'user'))),
        )

        self.helper = FormHelper()
        self. helper.layout = Layout(

            TabHolder(
                Tab(
                    _('Account Info'),
                    Row(
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.first_name.label }} </label>
                                <div class="controls ">{{ form.first_name.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.last_name.label }} </label>
                                <div class="controls ">{{ form.last_name.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                    ),
                    Row(
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.identity_type.label }} </label>
                                <div class="controls ">{{ form.identity_type.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.identity_num.label }} </label>
                                <div class="controls ">{{ form.identity_num.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                    ),
                    Row(
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.username.label }} </label>
                                <div class="controls ">{{ form.username.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.email.label }} </label>
                                <div class="controls ">{{ form.email.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                    ),
                    Row(
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.is_superuser.label }} </label>
                                <div class="controls ">{{ form.is_superuser.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.is_staff.label }} </label>
                                <div class="controls ">{{ form.is_staff.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                    ),
                    Row(
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.is_active.label }} </label>
                                <div class="controls ">{{ form.is_active.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),

                    ),

                    Row(
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.hgroups.label }} </label>
                                <div class="controls ">{% for x in form.hgroups.value %} 
                                {{ x.headquar.enterprise.name }}-{{ x.headquar.name }}>{{ x.group.name }}<br>
                                {% endfor %}</div>
                                </div>
                                '''),
                                    css_class='col-md-6'),
                    ),
                    Row(
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.egroups.label }} </label>
                                <div class="controls ">{% for x in form.egroups.value %} 
                                {{ x.enterprise.name }}>{{ x.group.name }}<br>
                                {% endfor %}</div>
                                </div>
                                '''),
                                    css_class='col-md-6'),
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.agroups.label }} </label>
                                <div class="controls ">{% for x in form.agroups.value %} 
                                {{ x.association.name }}>{{ x.group.name }}<br>
                                {% endfor %}</div>
                                </div>
                                '''),
                                    css_class='col-md-6'),
                    ),

                ),
                Tab(
                    _('Tracking'),
                    Row(
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.is_active.label }} </label>
                                <div class="controls ">{{ form.is_active.value }}</div>
                                </div>
                                '''),
                            css_class='col-md-6'),
                    ),
                    Row(
                        Div(HTML('''
                                <div class="form-group">
                                <label class="control-label"> {{ form.status.label }} </label>
                                <div class="controls ">{% for x in form.status.value %} 
                                {{ x.created_at }} | {{ x.description }} | {{ x.status }}<br>
                                {% endfor %}</div>
                                </div>
                                '''),
                                    css_class='col-md-6'),
                    ),

                ),

                Tab(_('Image'),
                    HTML("""
                        {% if form.photo.value %}<img class="img-responsive" src="{{ MEDIA_URL }}{{ form.photo.value }}">{% endif %}
                        """),
                    ),
            ),
            Row(
                FormActions(

                    btnCancel(),

                ),
            ),
        )


class UserActiveUpdateForm(forms.ModelForm):

    """ """

    def save(self, commit=True):
        user = super(UserActiveUpdateForm, self).save(commit=False)
        obj = user
        # if obj.pk:
        if obj.is_active:
            if UserStatus.objects.filter(user=obj.pk).count() > 0:
                if UserStatus.objects.filter(user=obj.pk).latest('id').status != ON:
                    UserStatus.objects.create(
                        status=ON,
                        description=self.cleaned_data['description'], user=obj)
            else:  # no tiene registros en UserStatus
                UserStatus.objects.create(
                    status=ON,
                    description=self.cleaned_data['description'], user=obj)
        else:
            if UserStatus.objects.filter(user=obj.pk).count() > 0:
                if UserStatus.objects.filter(user=obj.pk).latest('id').status != OFF:
                    UserStatus.objects.create(
                        status=OFF,
                        description=self.cleaned_data['description'], user=obj)
            else:
                UserStatus.objects.create(
                    status=OFF,
                    description=self.cleaned_data['description'], user=obj)
        obj.save()

        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['is_active', 'username', ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)

        super(UserActiveUpdateForm, self).__init__(*args, **kwargs)

        self.fields['description'] = forms.CharField(
            label=capfirst(_(u'Description')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )

        self.helper = FormHelper()
        self. helper.layout = Layout(

            Row(
                Div(Field('username', readonly=True),
                    css_class='col-md-6'),
                Div(Field('is_active'),
                    css_class='col-md-6'),
            ),
            Row(
                Div(Field('description',),
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


class UserForm(forms.ModelForm):

    """ """
    person_id = forms.CharField(widget=forms.HiddenInput(), required=False,)
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    # no funciona para el inser por person esto está validado en el Model como
    # debe de ser ????
    def clean_identity_numxx(self):
        identity_num = self.cleaned_data['identity_num']
        identity_type = self.cleaned_data['identity_type']

        if Person.objects.exclude(id=self.instance.person.id).filter(identity_type=self.instance.person.identity_type, identity_num=self.instance.person.identity_num).count() > 0:
            raise forms.ValidationError(
                _(u'%(model_name)s with this %(field_label)s already exists.xxx') % {
                    'model_name': capfirst(_('Person')),
                    'field_label': get_text_list((capfirst(_('number')), capfirst(_('Type'))), _('and')),
                })
        return identity_num

    def save(self, commit=True):
        ''' # así no funciona
        if Person.objects.exclude(id=self.instance.person.id).filter(identity_type=self.instance.person.identity_type, identity_num=self.instance.person.identity_num).count() > 0:

            raise forms.ValidationError({
                'identity_num':
                (_(u'%(model_name)s with this %(field_label)s already exists.xxx pp') % {
                'model_name': _('Person'),
                'field_label': get_text_list((capfirst(_('number')), capfirst(_('Type'))), _('and')),
                },),
            })
        '''
        user = super(UserForm, self).save(commit=False)

        if self.cleaned_data["password1"]:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'email', ]
        '''
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not uniquexxx.",
            }
        }
        '''

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)

        super(UserForm, self).__init__(*args, **kwargs)
        # print self.request.user
        #self.fields['hidden_field'] = forms.CharField(widget=forms.HiddenInput())
        # print self.hidden_field

        headquar = Headquar.objects.get(
            id=UserToken.get_headquar_id(self.request.session))
        solution_enterprise = Solution.objects.get(
            id=headquar.enterprise.solution.id)
        solution_association = Solution.objects.get(
            id=headquar.association.solution.id)
        module_list = Module.objects.filter(Q(solutions=solution_enterprise) | Q(
            solutions=solution_association), is_active=True).distinct()
        # trae los objetos relacionados sad.Module
        group_perm_list = Group.objects.filter(
            module_set__in=module_list).order_by("-id").distinct()
        # print group_perm_list
        # print "====================="
        # pero hay que adornarlo de la forma Module>Group
        group_list_by_module = []
        # solo para verificar que el Group no se repita si este está en dos o
        # más módulos
        group_list_by_module_unique_temp = []
        for module in module_list:
            for group in Group.objects.filter(module_set=module).distinct():
                if len(group_list_by_module) == 0:
                    group_list_by_module.append({
                                                "group": group,
                                                "module": module,
                                                })
                    group_list_by_module_unique_temp.append(group)
                else:
                    if group not in group_list_by_module_unique_temp:
                        group_list_by_module.append({
                                                    "group": group,
                                                    "module": module,
                                                    })
                        group_list_by_module_unique_temp.append(group)
        groups_final = {}
        for perm in group_list_by_module:
            groups_final[perm['group'].id] = '%s> %s' % (
                perm['module'].name,  perm['group'].name)

        # print groups_final.items()
        '''
        self.fields['hgroups'] = forms.ModelMultipleChoiceField(
            queryset=Group.objects.filter(module_set__in=module_list).order_by("-id").distinct()

            )
        self.fields['hgroups'].initial=Group.objects.filter(userheadquar__headquar__id=headquar.id, userheadquar__user__id=2).distinct() 
        
        '''
        self.fields['hgroups'] = forms.MultipleChoiceField(
            label=u'%s %s' % (capfirst(_(u'groups')), capfirst(_(u'Headquar'))), required=False,
            choices=groups_final.items(),
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        if self.object:
            self.fields['hgroups'].initial = [(e.id) for e in Group.objects.filter(
                userheadquar__headquar__id=headquar.id, userheadquar__user__id=self.object.id).distinct()]

        self.fields['egroups'] = forms.MultipleChoiceField(
            label=u'%s %s' % (capfirst(_(u'groups')), capfirst(_(u'Enterprise'))), required=False,
            choices=groups_final.items(),
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        if self.object:
            self.fields['egroups'].initial = [(e.id) for e in Group.objects.filter(
                userenterprise__enterprise__id=headquar.enterprise.id, userenterprise__user__id=self.object.id).distinct()]

        self.fields['agroups'] = forms.MultipleChoiceField(
            label=u'%s %s' % (capfirst(_(u'groups')), capfirst(_(u'Association'))), required=False,
            choices=groups_final.items(),
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        if self.object:
            self.fields['agroups'].initial = [(e.id) for e in Group.objects.filter(
                userassociation__association__id=headquar.association.id, userassociation__user__id=self.object.id).distinct()]

        self.fields['password1'] = forms.CharField(
            label=capfirst(_(u'Password')), required=False,
            widget=forms.PasswordInput, initial='',
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['password2'] = forms.CharField(
            label=capfirst(_(u'Password confirmation')), required=False,
            widget=forms.PasswordInput, initial='',
            help_text=u'<small class="help-error"></small> %s' % _(
                u'Enter the same password as above, for verification.'),
        )

        self.fields['first_name'] = forms.CharField(
            label=capfirst(_(u'first name')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['last_name'] = forms.CharField(
            label=capfirst(_(u'last name')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['identity_type'] = forms.ChoiceField(
            label=capfirst(_(u'Identity type')), required=True,
            # widget=forms.RadioSelect(),
            choices=IDENTITY_TYPE_CHOICES,

            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['identity_num'] = forms.CharField(
            label=capfirst(_(u'number')), required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['photo'] = forms.ImageField(
            label=capfirst(_(u'Photo')), required=False,
            initial='persons/default.png',
            help_text=u'<small class="help-error"></small> %s' % _(
                u'Available formats are JPG, GIF, and PNG.'),
        )

        self.helper = FormHelper()
        self. helper.layout = Layout(
            Field('person_id',),
            TabHolder(
                Tab(_('Personal Info'),
                    Row(
                        Div(Field('first_name',),
                    css_class='col-md-6'),
                        Div(Field('last_name', ),
                    css_class='col-md-6'),
                    ),
                    Row(
                        Div(Field('identity_type',),
                                    css_class='col-md-6'),
                        Div(Field('identity_num',),
                                    css_class='col-md-6'),
                    ),
                    ),
                Tab(_('Account Info'),
                    Row(
                        Div(Field('username', autofocus=True, autocomplete='off', css_class='input-required'),
                    css_class='col-md-6'),
                        Div(Field('email', ),
                    css_class='col-md-6'),
                    ),
                    Row(
                        Div(Field('password1', autocomplete='off'),
                                    css_class='col-md-6'),
                        Div(Field('password2', autocomplete='off'),
                                    css_class='col-md-6'),
                    ),
                    Row(
                        Div(Field('hgroups'),
                                    css_class='col-md-6'),
                    ),
                    Row(
                        Div(Field('egroups'),
                                    css_class='col-md-6'),
                        Div(Field('agroups'),
                                    css_class='col-md-6'),
                    ),

                    ),

                Tab(_('Image'),
                    Row(
                        Div(Field('photo'),
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


class MyModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return "%s/%s" % (obj.content_type.app_label, obj.codename)


class MenuForm(forms.ModelForm):

    """ """

    class Meta:
        model = Menu
        fields = ['module', 'title', 'parent',
                  'permission', 'pos', 'icon', 'url', ]

    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)
        self.fields['title'].help_text=u'<small class="help-error"></small> %s' % _(
                u' ')
        self.fields['pos'].help_text=u'<small class="help-error"></small> %s' % _(
                u' ')
        self.fields['url'].help_text=u'<small class="help-error"></small> %s' % _(
                u' ')
        '''
        self.fields['permission'] = MyModelChoiceField(
            label=capfirst(_(u'permission')), required=False,

            queryset=Permission.objects.all(),

            # queryset=list(
            #    c['content_type__app_label'] for c in Permission.objects.all()
            #),
            # widget=forms.CheckboxSelectMultiple(),
            # widget=forms.SelectMultiple(attrs={'class':'form-control'}),
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        '''
        self.fields['parent'].queryset = Menu.objects.filter(parent=None)

        self.fields['parent'].label_from_instance = lambda obj: "%s:%s" % (
            dict((x, y)
                 for x, y in MODULE_CHOICES)[obj.module], obj.title)

        self.fields['permission'].label_from_instance = lambda obj: "%s/%s" % (
            obj.content_type.app_label, obj.codename)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(
            Row(
                Div(Field('module', css_class=''),
                    css_class='col-md-8'),
            ),
            Row(
                Div(Field('title', css_class='input-required'),
                    css_class='col-md-4'),
                Div(Field('parent', ),
                    css_class='col-md-4'),
                Div(Field('permission', ),
                    css_class='col-md-4'),
            ),
            Row(
                Div(Field('pos', css_class='input-required input-integer mask-pint'),
                    css_class='col-md-4'),
                Div(Field('icon', ),
                    css_class='col-md-4'),
                Div(Field('url', css_class='input-required'),
                    css_class='col-md-4'),
            ),
            Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                    btnReset(),
                ),
            ),
        )


class ModuleForm(forms.ModelForm):

    """ """

    class Meta:
        model = Module
        fields = ['module', 'name', 'description', 'groups', 'initial_groups', ]

    def __init__(self, *args, **kwargs):
        super(ModuleForm, self).__init__(*args, **kwargs)
        self.fields['name'].help_text=u'<small class="help-error"></small> %s' % _(
                u' ')
        self.fields['description'].help_text=u'<small class="help-error"></small> %s' % _(
                u' ')
        self.fields['description'].widget.attrs={'rows': 3, }
        '''
        self.fields['groups'] = forms.ModelMultipleChoiceField(
            label=capfirst(_(u'groups')), required=False,
            queryset=Group.objects.all(),
            #widget=forms.CheckboxSelectMultiple(),
            widget=forms.SelectMultiple(attrs={'class':'form-control'}),
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        '''

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(
            Row(
                Div(Field('module', css_class='input-required'),
                    css_class='col-md-6'),
                Div(Field('name', css_class='input-required'),
                    css_class='col-md-6'),
            ),
            Row(
                Div(Field('groups', css_class='input-required'),
                    css_class='col-md-6'),
                Div(Field('initial_groups', css_class='input-required'),
                    css_class='col-md-6'),
            ),
            Row(
                Div(Field('description', css_class=''),
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

    def clean_namexx(self):  # esto está validado en el Model como debe de ser
        name = self.cleaned_data['name']
        if normalize('NFKD', name).encode('ascii', 'ignore').lower() in list(
            normalize('NFKD', c['name']).encode('ascii', 'ignore').lower()
            for c in Module.objects.values('name').exclude(pk=self.instance.pk).filter(module=self.instance.module)
        ):
            raise forms.ValidationError(
                _(u'%(model_name)s with this %(field_label)s already exists.') % {
                    'model_name': capfirst(_('Module')),
                    'field_label': capfirst(_('name')),
                })
        return name


def validate_unique_group_name(self):
    if normalize('NFKD', self).encode('ascii', 'ignore').lower() in list(
            normalize('NFKD', c['name']).encode('ascii', 'ignore').lower()
            for c in Group.objects.values('name')
    ):
        raise forms.ValidationError(
            _(u'%(model_name)s with this %(field_label)s already exists.') % {
                'model_name': capfirst(_('group')),
                'field_label': capfirst(_('name')),
            })


class GroupForm(forms.ModelForm):

    """ """
    class Meta:
        model = Group
        fields = ['name', ]

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        self.fields['name'].help_text=u'<small class="help-error"></small> %s' % _(
                u'Name of group the user or profile user.')
        #self.fields['name'].validators = [validate_unique_group_name]

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(
            Row(
                Div(Field('name', css_class='input-required'),
                    css_class='col-md-8'),
            ),
            Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                    btnReset(),
                ),
            ),
        )

    def clean_name(self):
        name = self.cleaned_data['name']
        if normalize('NFKD', name).encode('ascii', 'ignore').lower() in list(
            normalize('NFKD', c['name']).encode('ascii', 'ignore').lower()
            for c in Group.objects.values('name').exclude(pk=self.instance.pk)
        ):
            raise forms.ValidationError(
                _(u'%(model_name)s with this %(field_label)s already exists.') % {
                    'model_name': capfirst(_('group')),
                    'field_label': capfirst(_('name')),
                })
        return name

#TODO msg
class PermissionForm(forms.ModelForm):

    """ """
    class Meta:
        model = Permission
        fields = ['name', ]

    def __init__(self, *args, **kwargs):
        super(PermissionForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(
            label=capfirst(_(u'name')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u'Can CRUD to Model'),
        )
        self.fields['app_label'] = forms.CharField(
            label=_(u'App'), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u'Ingrese palabra de la forma [A-Z0-9_]'),
        )

        self.fields['controller_view'] = forms.CharField(
            label=_(u'Controller'), required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u'Ingrese palabra de la forma [A-Z0-9]'),
        )
        self.fields['action_view'] = forms.CharField(
            label=_(u'Action'), required=False,
            help_text=u'<small class="help-error"></small> %s' % _(
                u'Ingrese palabra de la forma [A-Z0-9_]'),
        )

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(
            Row(
                Div(Field('app_label', css_class='input-required input-word_'),
                    css_class='col-md-4'),
                Div(Field('controller_view', css_class='input-word'),
                    css_class='col-md-4'),
                Div(Field('action_view', css_class='input-word_'),
                    css_class='col-md-4'),
            ),
            Row(
                Div(Field('name', css_class='input-required'),
                    css_class='col-md-8'),  # input-alphanum
            ),
            Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                    btnReset(),
                ),
            ),
        )

    def clean(self):
        controller_view = self.cleaned_data['controller_view']
        action_view = self.cleaned_data['action_view']
        if not controller_view and action_view: # TODO cambiar mensaje
            self._errors['controller_view'] = self.error_class([
                (u'Complete controlador para la accion %(action)s.') % {
                    'action': action_view}
            ])
        controller_view = self.cleaned_data['controller_view'].lower()
        app_label = self.cleaned_data['app_label'].lower()
        action_view = self.cleaned_data['action_view'].lower()

        codename = ''
        recurso = '/%s/' % app_label
        if controller_view and action_view:
            codename = '%s_%s' % (controller_view, action_view)
            recurso = '/%s/%s/%s/' % (
                app_label, controller_view, action_view)
        if controller_view and not action_view:
            codename = '%s' % (controller_view)
            recurso = '/%s/%s/' % (app_label, controller_view)

        self.cleaned_data['codename'] = codename
        self.cleaned_data['recurso'] = recurso

        return self.cleaned_data

    '''
    def save(self, commit=True):
        #self.cleaned_data['content_type'] = '1'
        content_type, is_content_type_created = ContentType.objects.get_or_create(
            name=self.cleaned_data['controller_view'].lower(),
            model=self.cleaned_data['controller_view'].lower(),
            app_label=self.cleaned_data['app_label'].lower(),
        )
        self.cleaned_data['content_type'] = content_type

        return super(PermissionForm, self).save(commit)
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        #permission = super(PermissionForm, self).save(commit=False)

        controller_view = self.cleaned_data['controller_view']
        app_label = self.cleaned_data['app_label']
        action_view = self.cleaned_data['action_view']

        codename = ''
        recurso = '/%s/' % app_label.lower()
        if controller_view and action_view:
            codename = '%s_%s' % (controller_view.lower(), action_view.lower())
            recurso = '/%s/%s/%s/' % (
                app_label.lower(), controller_view.lower(), action_view.lower())
        if controller_view and not action_view:
            codename = '%s' % (controller_view.lower())
            recurso = '/%s/%s/' % (app_label.lower(), controller_view.lower())
        if not controller_view and action_view:
            raise forms.ValidationError(
                ('Complete controlador para la acción <b>%(action)s</b>.') % {
                    'action': action_view
                })
        self.cleaned_data['codename'] = codename
        # permission.codename=codename
        # if commit:
        #    permission.save()
        # return permission

        content_type, is_content_type_created = ContentType.objects.get_or_create(
            name=self.cleaned_data['controller_view'].lower(),
            model=self.cleaned_data['controller_view'].lower(),
            app_label=self.cleaned_data['app_label'].lower(),
        )
        self.cleaned_data['content_type'] = content_type

        return super(PermissionForm, self).save(commit)
    '''
