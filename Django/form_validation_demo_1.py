from django import forms, views
from django.shortcuts import render, HttpResponse
from django.urls import path, include


class MyForm(forms.Form):
    name = forms.CharField(max_length=100)
    title = forms.CharField(max_length=100)

    def clean_name(self):
        name = self.cleaned_data.get('name', None)

        if name:
            if len(name) < 8:
                raise forms.ValidationError([
                    forms.ValidationError("at least 8 chars"),
                ])

        print('myform clean name')
        return name  # always return a value even if not been changed to replace the value n cleaned data
        '''
        name <ul class="errorlist"><li>at least 8 chars</li></ul>
        '''

    def clean(self):
        print('hi')
        name = self.cleaned_data.get('name', None)
        title = self.cleaned_data.get('title', None)

        if name and title:
            if len(name) < len(title):

                # name <ul class="errorlist"><li>make it large</li></ul>
                self.add_error('name', 'make it large')
                raise forms.ValidationError([
                    # __all__ <ul class="errorlist nonfield"><li>name to be gte title</li></ul>
                    forms.ValidationError('name lte title'),
                ])


class MyView(views.View):

    def get(self, request):
        form = MyForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = MyForm(request.POST or None)

        if form.is_valid():
            print(form.as_table())
            return HttpResponse('yes')
        else:
            # print(type(form.errors)) # <class 'django.forms.utils.ErrorDict'>
            # print(form.as_table())
            for key in form.errors:
                print(key)
                print(form.errors.get(key, None))

            return render(request, 'form.html', {'form': form})


urlpatterns = [
    path('', MyView.as_view(), name='fvd1')
]


'''
-> form.html

{% extends 'base.html' %}

{% block content_1 %}
<title>Form</title>
{% endblock %}

{% block content_2 %}

<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    <table>
        <tr>
            <td></td>
            <td>{{ form.non_field_errors }}</td>
        </tr>
        <tr>
            <td> {{ form.name.label_tag }} </td>
            <td> {{ form.name }} </td>

        </tr>
        <tr>
            <td></td>
            <td>{{ form.name.errors }}</td>
        </tr>
        <tr>
            <td> {{ form.title.label_tag }} </td>
            <td> {{ form.title }} </td>

        </tr>
        <tr>
            <td></td>
            <td>{{ form.title.errors }}</td>
        </tr>

        <tr>
            <td></td>
            <td><input type="submit" value="Enter"></td>
        </tr>
    </table>
</form>
{% endblock %}


'''
