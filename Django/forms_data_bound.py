import datetime
from django import forms
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoAdmin.settings")
django.setup()


class MyForm(forms.Form):
    name = forms.CharField(max_length=100, initial='Your Name')
    date = forms.DateField()

    def clean(self):
        super().clean()
        print('My form clean')


data = {'name': 'shoaib', 'date': datetime.date.today()}

form1 = MyForm(data)  # bound

for key in form1.data:
    print(key, form1.data.get(key))  # it returns output

form2 = MyForm(initial={'name': 'tasrif',
                        'date': datetime.date(2016, 1, 1)})  # not bound

print('sec0')
print(form1, form1.is_bound)  # cleaned by clean(),
# before cleaning the cleaned_data dict not even been created
# by cleaning data, cleaned_data dict gets filled into from data dict
print('sec1')
print(form2, form2.is_bound)  # not cleaned as it is not bound

for key in form1.data:
    print(key, form1.data.get(key))  # it returns output

for key in form2.data:
    print(key, form2.data.get(key))  # it returns nothing as unbound

print('sec2')
for key in form1.cleaned_data:
    print(key, form1.cleaned_data.get(key))


'''
class ContactForm(forms.Form):
    # Everything as before.
    

    def clean(self):
        cleaned_data = super().clean()
        cc_myself = cleaned_data.get("cc_myself")
        subject = cleaned_data.get("subject")

        if cc_myself and subject:
            # Only do something if both fields are valid so far.
            if "help" not in subject:
                raise forms.ValidationError(
                    "Did not send for 'help' in the subject despite "
                    "CC'ing yourself."
                )

references:
https://docs.djangoproject.com/en/2.2/ref/forms/validation/


'''
