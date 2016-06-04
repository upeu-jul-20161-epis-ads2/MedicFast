# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     utils

Descripcion: Personaliza formularios como botones

"""

from django.utils.translation import ugettext

from django.conf import settings
from django.template import Template
from django.template.loader import render_to_string

from crispy_forms.compatibility import text_type
from crispy_forms.utils import flatatt

TEMPLATE_PACK = getattr(settings, 'CRISPY_TEMPLATE_PACK', 'bootstrap')


def empty(request, parm, default):
    return default if not request.GET.get(parm) else request.GET.get(parm)


class BaseButton(object):

    """
    A base class to reduce the amount of code in the Button classes.
    """
    template = "%s/layout/basebuttonc.html"

    def __init__(self, name, value, **kwargs):
        self.name = name
        self.value = value
        self.id = kwargs.pop('css_id', '')
        self.attrs = {}

        if 'css_class' in kwargs:
            self.field_classes += ' %s' % kwargs.pop('css_class')

        self.template = kwargs.pop('template', self.template)
        self.flat_attrs = flatatt(kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        """
        Renders an `<button></button>` if container is used as a Layout object.
        Button value can be a variable in context.
        """
        self.value = Template(text_type(self.value)).render(context)
        template = self.template % template_pack
        return render_to_string(template, {'input': self}, context)


class Submit(BaseButton):

    """
    Used to create a Submit button descriptor for the {% crispy %} template tag::

        submit = Submit('Search the Site', 'search this site')

    .. note:: The first argument is also slugified and turned into the id for the submit button.
    """
    input_type = 'submit'
    field_classes = 'submit submitButton' if TEMPLATE_PACK == 'uni_form' else 'btn btn-primary'


class Button(BaseButton):

    """
    Used to create a Submit input descriptor for the {% crispy %} template tag::

        button = Button('Button 1', 'Press Me!')

    .. note:: The first argument is also slugified and turned into the id for the button.
    """
    input_type = 'button'
    field_classes = 'button' if TEMPLATE_PACK == 'uni_form' else 'btn'


class Reset(BaseButton):

    """
    Used to create a Reset button input descriptor for the {% crispy %} template tag::

        reset = Reset('Reset This Form', 'Revert Me!')

    .. note:: The first argument is also slugified and turned into the id for the reset.
    """
    input_type = 'reset'
    field_classes = 'reset resetButton' if TEMPLATE_PACK == 'uni_form' else 'btn'


            # HTML(
            #    """{% if form.test_image.value %}<img class="img-responsive"
            # src="{{ MEDIA_URL }}{{ form.test_image.value }}">{% endif %}""",
            # ),

def smtSave():
    return Submit(
        'submit',
        '<i class="btn-icon-onlyx fa fa-save"></i> <span class="hidden-xsx"> %s</span>' %
        ugettext('Save'),
        css_class='text-bold',  title='%s' % ugettext('Save'))


def btnCancel():
    return Button(
        'cancel',
        '<i class="btn-icon-onlyx fa fa-ban"></i> <span class="hidden-xs"> %s</span>' %
        ugettext('Cancel'),
        css_class='btn btn-danger btn-back text-bold', title='%s' % ugettext('Cancel'))


def btnReset():
    return Reset(
        'reset',
        '<i class="btn-icon-onlyx fa fa-undo"></i> <span class="hidden-xs"> %s</span>' %
        ugettext('Reset'),
        css_class='btn btn-default text-bold', title='%s' % ugettext('Reset'))
