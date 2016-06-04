# _*_ coding: utf-8 _*_
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

# models
from .models import Person

class PersonAdmin(admin.ModelAdmin):

    search_fields = ('first_name', 'last_name',)
    list_display = (
        'first_name', 'last_name', 'identity_type', 'identity_num',)

admin.site.register(Person, PersonAdmin)
