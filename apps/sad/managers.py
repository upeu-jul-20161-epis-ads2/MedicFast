# _*_ coding: utf-8 _*_
"""
@copyright   Copyright (c) 2014 Submit Consulting
@author      Angel Sullon (@asullom)
@package     sad

Descripcion: Implementacion de los managers de la app sad
"""

from django.db import models
#from django.db.models.query import QuerySet
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import UserManager


class UserQuerySet(models.query.QuerySet):

    """ """

    def with_status(self):
        return self.extra(
            select={
                'status': '''SELECT
                status FROM (
                SELECT * FROM sad_user_status  ORDER BY id %(desc)s 
                ) AS estado
                WHERE  estado.user_id = auth_user.id
                GROUP BY estado.user_id
                ''' % {'desc': settings.DESC}  # MySQL es DESC
            },
        )

# http://agiliq.com/books/djangodesignpatterns/models.html


class UserManager(UserManager):  # models.Manager

    """ """

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def with_status(self):
        return self.get_queryset().with_status()

    def get_by_natural_key(self, username):
        return self.get(username=username)
