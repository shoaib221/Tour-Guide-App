from django.shortcuts import HttpResponse
from django import views
from django.urls import path, include
import django
import os
from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import sys
sys.path += ['c:\\Users\\SHOAIB\\Desktop\\Projects\\DjangoAdmin']
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoAdmin.settings")
django.setup()


class Book1(models.Model):
    """Model definition for Book."""

    name = models.CharField(max_length=10)
    address = models.CharField(max_length=10)

    class Meta:
        """Meta definition for Book."""

        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return '%s  %s' % (self.name, self.address)

    def clean_fields(self, exclude=None):
        # must call super().clean_fields(), it wiil validate all the fields individually
        # to raise ValidationError for fields excluded in modelform
        # raising error is like 'return'
        # if exception is not caught it will directly redirect to error page

        print('model clean_fields')
        super().clean_fields(exclude=exclude)  # in case of error will return from here
        try:
            raise ValidationError(_('model clean_fields error'))
        except:
            pass

        raise ValidationError(_('model clean_fields error 22'))

    # this method is executed regardless of whether the previous one(clean_fields) raise ve or not

    def clean(self):
        # for custom validation
        # need not to call super().clean() if inherits models.Model
        # can call super().clean() if inherited parent's clean() does functionality
        # can’t raise ValidationError in Model.clean() for fields that don’t appear in a modelform
        print('model clean')

        raise ValidationError(_('model clean error'))


class Book1Form(forms.ModelForm):
    class Meta:
        model = Book1
        fields = '__all__'

    def clean_name(self):
        print('modelform clean_name')
        raise ValidationError(_('modelform clean_fieldname error'))
        return self.cleaned_data['name']  # always return a data

    def clean(self):
        print('modelform clean')
        raise ValidationError(_('modelform clean error'))
        super().clean()


class View2(views.View):
    def get(self, request):
        data = {'name': 'shoaib', 'address': 'Lakecity'}
        form = Book1Form(data)
        # print(form.data)
        if form.is_valid():
            print(form.as_table())
            return HttpResponse('hi')
        else:
            print(form.as_table())
            return HttpResponse('hi else')


urlpatterns = [

    path('v2/', View2.as_view()),
]

'''
you can raise multiple ve within a cleaning method by cathing one by one
'''
