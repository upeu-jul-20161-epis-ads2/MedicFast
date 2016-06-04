# -*- coding: utf-8 -*-
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     utils

Descripcion: Tag o interfáz para mostrar a los usuarios los mensajes generados
por el sistema
"""
from django import template
#from apps.utils.messages import Message
from django.contrib import messages
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def get_notify(request):
    """
    Muestra los mensajes de error, advertencias o de información en
    los templates.
    Estos mensajes son recepcionados con el mod messages de django.contrib

    messages.DEBUG: 'debug', # no muestra en pantalla

    Setting messages in view::

        from django.contrib import messages

        messages.debug(request, 'QL statements were executed.') # no muestra
        messages.info(request, 'Three credits remain in your account.')
        messages.success(request, 'Profile details updated.')
        messages.warning(request, 'Your account expires in three days.')
        messages.error(request, 'Document deleted.')

        messages.add_message(request, messages.DEBUG, 'No muestra')
        messages.add_message(request, messages.INFO, 'info')
        messages.add_message(request, messages.SUCCESS, 'success')
        messages.add_message(request, messages.WARNING, 'warning')
        messages.add_message(request, messages.ERROR, 'error')

    Usage::

            {% get_notify request %}

    Examples::

            {% get_notify request %}
    """
    d = None
    try:
        d = messages.get_messages(request)
    except KeyError:
        pass
    o = ''
    if d:
        for i in d:
            # print i
            ox = (u''
                  u'<div class="alert alert-%s " role="alert">'
                  u'<button type="button" class="close" data-dismiss="alert">'
                  u'<span aria-hidden="true">&times;</span><span class="sr-only">Close</span>'
                  u'</button>%s</div>'
                  u'' % (i.tags, i)
                  )
            o += ox
    a = (u'<div id="flash-message" class="flash-message">'
         )

    c = (u'		</div>'
         )

    path = request.path  # get_full_path()
    script = (u'<script type="text/javascript">'
              u'//DwUpdateUrl("%s");'
              u'</script>'
              u'' % (path))
    if request.is_ajax():
        return mark_safe('%s%s%s %s' % (a, o, c, script))
    else:
        return mark_safe('%s%s%s' % (a, o, c))
