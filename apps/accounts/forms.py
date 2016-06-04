from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# _*_ coding: utf-8 _*_
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _

from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import HTML, Field, Fieldset, Div, Row, ButtonHolder, Submit, Button, Reset
from crispy_forms.bootstrap import FormActions, AppendedText,\
    PrependedAppendedText, PrependedText, TabHolder, Tab
from django.utils.text import capfirst
from django.utils.encoding import force_text

from apps.sad.models import User
from apps.space.models import Solution, TYPE_CHOICES, Enterprise, Association
from apps.params.models import NID, IDENTITY_TYPE_CHOICES
#from timezone_field import TimeZoneFormField

from apps.utils.forms import smtSave, btnCancel, btnReset


class RegistrationEnterpriseAssociationForm(forms.ModelForm):

    """ """
    class Meta:
        model = Enterprise
        fields = ['name', 'logo', 'tax_id', 'type_e', 'solution', ]

    def __init__(self, *args, **kwargs):
        super(RegistrationEnterpriseAssociationForm,
              self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(
            label=capfirst(_(u'Enterprise')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['association_name'] = forms.CharField(
            label=capfirst(_(u'Association')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )

        self.fields['acept'] = forms.BooleanField(
            label=capfirst(_(u'I accept the Terms of Service and Privacy Policy.')), required=True,
            # widget=forms.CheckboxInput(),
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['logo'] = forms.ImageField(
            label=capfirst(_(u'logo')), required=False,
            initial='enterprises/default.png',
            help_text=u'<small class="help-error"></small> %s' % _(
                u'Available formats are JPG, GIF, and PNG.'),
        )
        self.fields['solution'].required = True
        self.fields['solution'].help_text = u'<small class="help-error"></small> %s' % _(
            u' ')
        self.fields['type_e'].help_text = u'<small class="help-error"></small> %s' % _(
            u' ')
        self.fields['tax_id'].help_text = u'<small class="help-error"></small> %s' % _(
            u' ')

        self.helper = FormHelper()
        self.helper.form_id = 'form'
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(

            TabHolder(
                Tab(_('Enterprise'),
                    Row(
                        Div(Field('name', autofocus=True, css_class='input-required'),
                    css_class='col-md-6'),
                        Div(Field('tax_id', css_class='input-required', ),
                    css_class='col-md-6'),
                    ),
                    Row(
                        Div(Field('association_name', css_class='input-required',),
                            css_class='col-md-6'),
                        Div(Field('type_e', css_class='input-required', ),
                            css_class='col-md-6'),
                    ),
                    Row(
                        Div(Field('solution', css_class='input-required',),
                            css_class='col-md-6'),
                    ),


                    ),
                Tab(_('Image'),
                    Field('logo', css_class="")
                    ),
            ),
            Row(
                Div(Field('acept', css_class='input-required',),
                    css_class='col-md-12'),
            ),
            Row(
                FormActions(
                    smtSave(),
                    btnCancel(),
                    btnReset(),
                ),
            ),
        )


class LoginForm(AuthenticationForm):

    """ """
    remember_me = forms.BooleanField(label=_('Keep me logged in'), initial=False,
                                     required=False)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'js-validate form-vertical'
        self.helper.layout = Layout(
            'username',
            'password',
            'remember_me',
            ButtonHolder(
                Submit('login', _('Log in'), css_class='btn-primary')
            )
        )


class RegistrationForm(UserCreationForm):

    """ """
    class Meta:
        model = User
        fields = ['username', 'email', ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
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
        self.fields['identity_num'] = forms.CharField(
            label=dict((x, y)
                       for x, y in IDENTITY_TYPE_CHOICES)[NID], required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['association_name'] = forms.CharField(
            label=capfirst(_(u'Association')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['enterprise_name'] = forms.CharField(
            label=capfirst(_(u'Enterprise')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['enterprise_tax_id'] = forms.CharField(
            label=capfirst(_(u'Tax id')), required=True,
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['enterprise_type_e'] = forms.ChoiceField(
            label=capfirst(_(u'Type')), required=True,
            # widget=forms.RadioSelect(),
            choices=(('', '----------'),) + TYPE_CHOICES,

            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['solution'] = forms.ModelChoiceField(
            label=capfirst(_(u'Solution')), required=True,
            queryset=Solution.objects.filter(is_active=True),
            help_text=u'<small class="help-error"></small> %s' % _(
                u' '),
        )
        self.fields['acept'] = forms.BooleanField(
            label=capfirst(_(u'I accept the Terms of Service and Privacy Policy.')), required=True,
            # widget=forms.CheckboxInput(),
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
        self.helper.form_class = 'js-validate form-vertical'
        self. helper.layout = Layout(

            TabHolder(
                Tab(
                    _('Account Info'),
                    Row(
                        Div(Field('username', autofocus=True, css_class='input-required'),
                    css_class='col-md-6'),
                        Div(Field('email', ),
                    css_class='col-md-6'),
                    ),
                    Row(
                        Div(Field('password1',),
                                    css_class='col-md-6'),
                        Div(Field('password2', ),
                                    css_class='col-md-6'),
                    ),

                    Row(
                        Div(Field('enterprise_name',),
                                    css_class='col-md-6'),
                        Div(Field('enterprise_tax_id', ),
                                    css_class='col-md-6'),
                    ),
                    Row(
                        Div(Field('association_name',),
                                    css_class='col-md-6'),
                        Div(Field('enterprise_type_e', ),
                                    css_class='col-md-6'),
                    ),
                    Row(
                        Div(Field('solution',),
                                    css_class='col-md-6'),
                    ),


                ),
                Tab(
                    _('Personal Info'),
                    Row(
                        Div(Field('first_name',),
                    css_class='col-md-6'),
                        Div(Field('last_name', ),
                    css_class='col-md-6'),
                    ),
                    Row(
                        Div(Field('identity_num',),
                                    css_class='col-md-6'),
                    ),
                ),
                Tab(_('Image'),
                    Field('photo', css_class="")
                    ),
            ),
            Row(
                Div(Field('acept',),
                    css_class='col-md-12'),
            ),

            FormActions(
                Submit('submit', _('Sign up'),
                       css_class='btn-success pull-right'),
            ),
        )
