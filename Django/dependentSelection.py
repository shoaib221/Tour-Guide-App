from django.db import models
from django.urls import path, include, reverse_lazy
from django import views
from django.views.generic import ListView, CreateView, UpdateView
from django import forms
from django.shortcuts import render

'''
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoAdmin.settings")
django.setup()
'''


class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=100)
    birthdate = models.DateField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'load_cities.html', {'cities': cities})


# in case of modelform
class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'birthdate', 'country', 'city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()
        '''
        print(type(self.data))
        for k1 in self.data:  # iterating dictionary
            print(k1, self.data.get(k1, None))

        # output
        <class 'django.http.request.QueryDict'>
        csrfmiddlewaretoken 8ifH6Xed7mhcxTKRazO7KKfEp4dhmfgFJLIrbdlBqf6B98GcgP9eoKyJ61BsEbxT
        name shoaib
        birthdate 2016-01-01
        country 2
        city 3
        '''

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(
                    country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by(
                'name')

'''
# in case of non-modelform

from django import forms
from homepage.models import MyChoice, Country, City


class SearchRestaurantForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'] = forms.ChoiceField(
            choices=[(o.id, str(o)) for o in Country.objects.all()], required=False)
        self.fields['city'] = forms.ChoiceField(
            choices=[(o.id, str(o)) for o in City.objects.none()], required=False)

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'] = forms.ChoiceField(
                    choices=[(o.id, str(o)) for o in City.objects.filter(country_id=country_id)], required=False)

            except (ValueError, TypeError):
                pass
'''

class PersonListView(ListView):
    model = Person
    template_name = 'person_list.html'
    context_object_name = 'people'


class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'person_create.html'
    success_url = reverse_lazy('person_changelist')


class PersonUpdateView(UpdateView):
    model = Person
    form_class = PersonForm
    template_name = 'person_create.html'
    success_url = reverse_lazy('person_changelist')


urlpatterns = [
    path('', PersonListView.as_view(), name='person_changelist'),
    path('add/', PersonCreateView.as_view(), name='person_add'),
    path('<int:pk>/', PersonUpdateView.as_view(), name='person_change'),
    path('ajax/load-cities/', load_cities, name='ajax_load_cities'),
]

'''
-> load_cities.html

<html>
<body>

    <option value="">---------</option>
    {% for city in cities %}
    <option value="{{ city.pk }}">{{ city.name }}</option>
    {% endfor %}
</body>
</html>


-> person_create.html

{% extends 'base.html' %}


{% block content_1 %}
<title>Create Person </title>
{% endblock content_1 %}


{% block content_2 %}
<h2>Person Form</h2>

<form method="post" id="personForm" data-cities-url="{% url 'ajax_load_cities' %}" novalidate>
    {% csrf_token %}
    <table>
        {{ form.as_table }}
    </table>
    <button type="submit">Save</button>
    <a href="{% url 'person_changelist' %}">Nevermind</a>
</form>

<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script>
    $("#id_country").change(function () {
        var url = $("#personForm").attr("data-cities-url");  // get the url of the `load_cities` view
        var countryId = $(this).val();  // get the selected country ID from the HTML input

        $.ajax({                       // initialize an AJAX request
            url: url,                   // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
            data: {
                'country': countryId       // add the country id to the GET parameters
            },
            success: function (shoaib) {   // `data` is the return of the `load_cities` view function
                $("#id_city").html(shoaib);  // replace the contents of the city input with the data that came from the server
            }
        });
    });
</script>
{% endblock content_2 %}

->person_list.html
{% extends 'base.html' %}


{% block content_1 %}
<title>Person List</title>

{% endblock content_1 %}


{% block content_2 %}

{% for p in people %}
<a href="{{p.id}}/">{{p.name}}</a>
{% endfor %}

<a href="add/"> Add New Person </a>

{% endblock content_2 %}


'''
