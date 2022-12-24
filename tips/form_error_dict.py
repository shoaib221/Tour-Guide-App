from django import forms
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
import django
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoAdmin.settings")
sys.path += ['c:\\Users\\SHOAIB\\Desktop\\Projects\\DjangoAdmin']
django.setup()


class MyForm(forms.Form):
    name = forms.CharField(max_length=10)
    address = forms.CharField(max_length=10)

    def clean_name(self):
        name = self.cleaned_data.get('name', None)

        if name == 'shoaib':
            raise ValidationError("clean_name")

        return name

    def clean(self):
        address = self.cleaned_data.get('address', None)
        # print(address)
        if address == 'lake':
            raise ValidationError("clean")


data = {'name': 'shoaib', 'address': 'lake'}
form = MyForm(data)

if form.is_valid():
    pass  # print(form.as_table())
else:
    # form.errors <class 'django.forms.utils.ErrorDict'>
    # <ul class="errorlist">
    #   <li>name
    #   <ul class="errorlist">
    #       <li>clean_name</li>
    #       </ul>
    #   </li>
    #   <li>__all__
    #   <ul class="errorlist nonfield">
    #       <li>clean</li>
    #   </ul>
    #   </li>
    # </ul>

    # form.errors['name'] <class 'django.forms.utils.ErrorList'>
    # <ul class="errorlist">
    #   <li>clean_name</li>
    # </ul>

    form.add_error('name', 'new name error')
    form.add_error('__all__', ['new all error 1', 'new all error 2'])
    print(form.as_table())

'''
output
<tr><td colspan="2"><ul class="errorlist nonfield"><li>clean</li><li>new all error</li></ul></td></tr>
<tr><th><label for="id_name">Name:</label></th><td><ul class="errorlist"><li>clean_name</li><li>new name error</li></ul><input type="text" name="name" value="shoaib" maxlength="10" required id="id_name"></td></tr>
<tr><th><label for="id_address">Address:</label></th><td><input type="text" name="address" value="lake" maxlength="10" required id="id_address"></td></tr>
'''


def post(self, request, space_id):
    space = Space.objects.get(pk=space_id)
    if request.user.is_authenticated and space.residence.user_detail.user == request.user:
        form = self.form_class(request.POST or None)
        if form.is_valid():
            space_available = form.save(commit=False)
            space_available.space = space
            try:
                space_available.full_clean()
                space_available.save()
                return redirect('/residence/space/{}/'.format(space.id))
            except ValidationError as ve:
                # print(ve.message_dict)
                for k in ve.message_dict:
                    # form error filled by ve
                    form.add_error(k, ve.message_dict.get(k, None))
                # print(form.as_table())
                return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})
    else:
        return redirect('/permission_denied/')


'''
{'__all__': ['This space is already available within a part of this time span']}
<tr><td colspan="2"><ul class="errorlist nonfield"><li>This space is already available within a part of this time span</li></ul></td></tr>
<tr><th><label for="id_number_of_space">Number of space:</label></th><td><input type="number" name="number_of_space" value="1" required id="id_number_of_space"></td></tr>
<tr><th><label for="id_avail_from">Avail from:</label></th><td><input type="text" name="avail_from" value="2020-1-3" required id="id_avail_from"></td></tr>
'''
