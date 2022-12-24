from django import forms
import os
import sys
import django
sys.path += ['c:\\Users\\SHOAIB\\Desktop\\Projects\\DjangoAdmin']
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoAdmin.settings')
django.setup()


class MyForm(forms.Form):
    name = forms.CharField(max_length=10)
    add = forms.CharField(max_length=10)

    def clean(self):

        error_dict = {}
        i1 = {'name': 'first error'}
        error_dict.update(i1)
        i2 = {'__all__': ['second error']}
        error_dict.update(i2)
        error_dict['__all__'] += ['third error']
        # error_dict['__all__'] = None

        raise forms.ValidationError(error_dict)


data = {'name': 'sh', 'add': 'lake'}
form = MyForm(data)

if form.is_valid():
    pass
else:
    print(form.as_table())
