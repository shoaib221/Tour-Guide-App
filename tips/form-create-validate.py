from django import forms, views
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bravo1.settings")
django.setup()


class MyClass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'name'], name='unique class')]


class MyForm(forms.ModelForm):
    class Meta:
        model = MyClass
        exclude = ['user']


class MyView(views.View):
    form_class = MyForm
    template_name = 'form.html'

    def get(self, request):
        form = self.form_class()
        # self.form_class({'user': request.user}) will bind the data and therefore invoke validation
        # the upper process will just set the placeholder
        # if not selected or displayed explicitly the data wont be bound on the template during submission
        # print(form.is_bound)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            ob = form.save(commit=False)
            ob.user = request.user
            try:
                ob.full_clean()
                ob.save()
                return render(request, self.template_name)
            except ValidationError as ve:
                msg = ve.message_dict[NON_FIELD_ERRORS]
                return render(request, self.template_name, {'msg': msg, 'form': form})
            except Exception as e:
                return render(request, self.template_name, {'form': form, 'msg': e})
        else:
            return render(request, self.template_name, {'form': form})


# form.html
'''
{% extends 'base.html' %}

{% block content_1 %}
    <title>Form</title>
{% endblock %}

{% block content_2 %}
    hi
    <form method="post" enctype="multipart/form-data">
    {% csrf_token %}
        <ul>
            {% for message in msg %}
                <li>{{ message }}</li>
            {% endfor %}
        </ul>
    <table>
    {{ form.as_table }}
    <tr><td></td><td><input type="submit" value="Save"></td></tr>
    </table>
    </form>
{% endblock %}
'''

# NB
'''
Form validation steps:
- forms.full_clean(),is_valid(),errors
    - field.clean()
        - to_python()
        - validate()             -> override for custom validation of this field everywhere
        - run_validators()
    - forms.clean_<field_name>() -> override for custom validation of this field only in this form
    - forms.clean()              -> more than one field validation, invoked after the all fields individual validation,
                                 -> should be overriden in case of form validation

Model Validation steps:
- Model.clean_fields() -> individual field validation
- Model.clean() -> whole model instance validation, should be overriden for custom validation
- Model.validate_unique()
'''
