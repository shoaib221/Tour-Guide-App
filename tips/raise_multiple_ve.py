from django.urls import path
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
import sys
from django import forms
from django.db import models
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoAdmin.settings")
sys.path += ['c:\\Users\\SHOAIB\\Desktop\\Projects\\DjangoAdmin']
django.setup()
# print(sys.path)


class MyForm(forms.Form):
    name = forms.CharField(max_length=10)
    address = forms.CharField(max_length=10)

    def clean(self):
        raise forms.ValidationError({
            'name': [
                forms.ValidationError(_('name error 1')),
                forms.ValidationError(_('name error 2')),
            ],
            'address': [
                forms.ValidationError(_('address error 1')),
                forms.ValidationError(_('address error 2')),
            ],
            '__all__': [
                forms.ValidationError(_('non fields error 1')),
                forms.ValidationError(_('non fields error 2')),
            ]
        })


def View1(request):
    data = {'name': 'shoaib', 'address': 'Lakecity'}
    form = MyForm(data)
    if form.is_valid():
        pass
    else:
        print(form.as_table())
        return render(request, 'form.html', {'form': form})


urlpatterns = [
    path('v1/', View1)
]
