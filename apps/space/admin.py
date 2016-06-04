# _*_ coding: utf-8 _*_
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

# models
from .models import Solution


class SolutionAdmin(admin.ModelAdmin):

    """docstring for SolutionAdmin"""
    # formfield_overrides = {
    #    models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    #}

    list_display = ('name', 'description', 'is_active',)
    search_fields = ('name', 'is_active',)
    list_per_page = 2

admin.site.register(Solution, SolutionAdmin)
