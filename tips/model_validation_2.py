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


class Booki(models.Model):

    name = models.CharField(max_length=10)
    address = models.CharField(max_length=10)

    class Meta:
        pass

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
            # in case of error it will continue from except block
            super().clean_fields(exclude=exclude)
        except ValidationError as ve1:
            print('ve1', ve1.message_dict)

        if self.name == 'shoaib':
            # whether the field in exclude(modelform) or not
            try:
                if exclude and 'name' in exclude:
                    raise ValidationError(
                        _('Draft entries may not have a publication date.')
                    )
                else:
                    raise ValidationError({
                        'name': _(
                            'Set status to draft if there is not a '
                            'publication date.'
                        ),
                    })
                    # print('hi')
            except ValidationError as ve:
                print(ve.message_dict)
                # {'name': ['Set status to draft if there is not a publication date.']}

            if 1 == 1:
                if self.address == 'Lakecity':
                    raise ValidationError([
                        _('model ve2')
                    ])

    def clean(self):
        # this method is executed regardless of whether the previous one(clean_fields) raise ve or not
        # for custom validation
        # need not to call super().clean() if inherits models.Model
        # can call super().clean() if inherited parent's clean() does functionality
        # can’t raise ValidationError in Model.clean() for fields that don’t appear in a modelform
        print('model clean')
        if len(self.name) > 4:
            raise ValidationError(_('name too long'), code='long')
        else:
            raise ValidationError({
                'name': _('name gte 4')
            })


class BookiForm(forms.ModelForm):
    class Meta:
        model = Booki
        fields = '__all__'

    def clean_name(self):
        print('modelform clean_name')
        return self.cleaned_data['name']  # always return a data

    def clean(self):
        print('modelform clean')
        super().clean()


class View1(views.View):
    def get(self, request):
        book = Booka(name='saib')
        try:
            book.full_clean()
        except ValidationError as ve:
            print(ve.message_dict)
            return HttpResponse('hi')
            # return HttpResponse(['%s \n %s' % (shoaib, ve.message_dict.get(shoaib, None)) for shoaib in ve.message_dict])

        return HttpResponse('hi')


class View2(views.View):
    def get(self, request):
        data = {'name': 'shoaib', 'address': 'Lakecity'}
        form = BookiForm(data)
        # print(form.data)
        if form.is_valid():
            print(form.as_table())
            return HttpResponse('hi')
        else:
            print(form.as_table())
            return HttpResponse('hi else')


urlpatterns = [
    path('v1/', View1.as_view()),
    path('v2/', View2.as_view()),
]


'''
Note that if you provide an exclude argument to validate_unique(), any unique_together constraint
involving one of the fields you provided will not be checked.

-if more than one errors are raised for same field in two different places they will be appended
-errors raised in model validation will be appende to modelform errors

modelform clean field
modelform clean
- model gets the data from modelform cleaned_data dict
model clean_fields
model clean
'''
