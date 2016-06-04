# -*- coding: utf-8 -*-
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     utils

Descripcion: Genera el pie de paginación
"""

from django import template
from django.utils.html import escapejs, format_html
from django.contrib.admin.views.main import (ALL_VAR, 
                                             ORDER_VAR, PAGE_VAR, SEARCH_VAR)
from django.utils.safestring import mark_safe

register = template.Library()

DOT = '.'


@register.simple_tag
def paginator_number(page_obj, i, f, q, o):
    """
    Generates an individual page index link in a paginated list.
    """
    # i=i+1
    #print '%s\n' % i
    if i == DOT:
        return mark_safe('<li class="dot"><a>...</a></li>')
    elif i == page_obj.number:
        return format_html('<li class="active"><a href="#">{0}<span class="sr-only">(current)</span></a></li> ', i)
    else:
        return format_html('<li><a href="{0}"{1}>{2}</a> </li>',
                           '?page=%s&f=%s&q=%s&o=%s' % (i, f, q, o),
                           mark_safe(
                               ' class="end"' if i == page_obj.paginator.num_pages else ''),
                           i)


def paginator(context, adjacent_pages=3):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.

    """

    page_numbers = [n for n in
                    range(context['page_obj'].number - adjacent_pages, context[
                          'page_obj'].number + adjacent_pages + 1)
                    if n > 0 and n <= context['paginator'].num_pages]

    paginator, page_num = context[
        'page_obj'].paginator, context['page_obj'].number
    page_range = []
    ON_EACH_SIDE = adjacent_pages
    ON_ENDS = 2  # 2

        # If there are 10 or fewer pages, display links to every page.
    # Otherwise, do some fancy
    if paginator.num_pages <= 4:  # 10
        page_range = range(1,paginator.num_pages+1)
    else:
        # Insert "smart" pagination links, so that there are always ON_ENDS
        # links at either end of the list of pages, and there are always
        # ON_EACH_SIDE links at either end of the "current page" link.
        page_range = []
        if page_num > (ON_EACH_SIDE + ON_ENDS + 1):
            page_range.extend(range(1, ON_ENDS + 1))
            page_range.append(DOT)
            page_range.extend(
                range(page_num - ON_EACH_SIDE, page_num + 0))
        else:
            page_range.extend(range(1, page_num + 0))
        if page_num < (paginator.num_pages - ON_EACH_SIDE - ON_ENDS - 0):
            page_range.extend(
                range(page_num + 0, page_num + ON_EACH_SIDE + 1 + 0))
            page_range.append(DOT)
            page_range.extend(
                range(paginator.num_pages - ON_ENDS + 1, paginator.num_pages + 1))
        else:
            page_range.extend(range(page_num + 0, paginator.num_pages + 1))

    return {
        'page_obj': context['page_obj'],
        'paginator': context['paginator'],

        'page': context['page_obj'].number,
        'pages': context['paginator'].num_pages,
        'page_numbers': page_range,
        'next': context['page_obj'].next_page_number,
        'previous': context['page_obj'].previous_page_number,
        'has_next': context['page_obj'].has_next(),
        'has_previous': context['page_obj'].has_previous(),
        'show_first': 1 not in page_range,
        'show_last': context['paginator'].num_pages not in page_range,

        'o': context['o'],
        'f': context['f'],
        'q': context['q'],

        'opts': context['opts'],
        'show_all_url': True,


    }

register.inclusion_tag('utils/paginator.html', takes_context=True)(paginator)


def paginator_original(context, adjacent_pages=2):
    current_page = context['page_obj'].number
    number_of_pages = context['paginator'].num_pages
    page_obj = context['page_obj']
    paginator = context['paginator']
    startPage = max(current_page - adjacent_pages, 1)
    endPage = current_page + adjacent_pages + 1
    if endPage > number_of_pages:
        endPage = number_of_pages + 1
    page_numbers = [n for n in range(startPage, endPage)
                    if 0 < n <= number_of_pages]

    return {
        'page_obj': page_obj,
        'paginator': paginator,
        'page': current_page,
        'pages': number_of_pages,
        'page_numbers': page_numbers,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'show_first': 1 != current_page,
        'show_last': number_of_pages != current_page,
    }

#register.inclusion_tag('utils/paginator_o.html', takes_context=True)(paginator)
