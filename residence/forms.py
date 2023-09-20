


import datetime
from .models import  Room, RoomUnavailable
from accounts.models import Country, City
from .models import House
from django import forms

class HouseForm(forms.ModelForm):

    class Meta:
        model = House
        fields = ['name', 'address', 'description', 'city']
        

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if 'country' in self.data:
            country_id = int(self.data.get('country'))
            self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('city')
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('city')

        print("HouseForm")


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'beds', 'has_ac', 'price', 'description']

    def __init__(self, *args, **kwargs):
        # print("SpaceForm")
        super().__init__(*args, **kwargs)
        residence_id = None
        init_dict = {}
        # form for creating new space
        if kwargs.get('initial', None):
            init_dict = kwargs.get('initial', None)
            if init_dict.get('residence', None):
                residence_id = init_dict.get('residence', None)
        # print("44", self.data)

        if kwargs.get("instance", None):
            instance = kwargs.get("instance", None)
            residence_id = instance.id
            # print(instance, type(instance))
#        self.fields['space_type'].queryset = SpaceType.objects.filter( residence_id=residence_id)

    def clean(self):
        pass




class MyChoice:

    months = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'),
        (7, 'July'), (8, 'August'), (9, 'September'), (10, 'Octobor'), (11, 'November'), (12, 'December')
    ]

    dates = [
        (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'),
        (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'),
        (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'),
        (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'),
        (25, '25'), (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'),
    ]


class CreateUnavaiabilityForm(forms.Form):

    from_year = forms.ChoiceField(choices=[("", "------------")], label="From Year", required=True)
    from_month = forms.ChoiceField(choices=[("", "------------")], label="From Month" , required=True )
    from_day = forms.ChoiceField(choices=[("", "------------")], label="From Day", required=True)
    to_year = forms.ChoiceField(choices=[("", "------------")], label='To Year' , required=True )
    to_month = forms.ChoiceField(choices=[("", "------------")], label='To Month', required=True)
    to_day = forms.ChoiceField(choices=[("", "------------")], label='To Day' , required=True) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        year_choice = [("", "choose year")]
        for i in range( datetime.date.today().year , datetime.date.today().year +2):
            year_choice += [(i, str(i))]
        
        month_choice = [("", "choose month")]
        for i in range( len(MyChoice.months) ):
            month_choice += [(MyChoice.months[i][0], MyChoice.months[i][1])]

        date_choice = [("", "choose date")]
        for i in range( len(MyChoice.dates) ):
            date_choice += [(MyChoice.dates[i][0], MyChoice.dates[i][1])]
        
        
        self.fields['from_year'] = forms.ChoiceField(choices=year_choice, label="From Year")

        self.fields['from_month'] = forms.ChoiceField(choices=month_choice, label="From Month")
        
        self.fields['from_day'] = forms.ChoiceField(choices=date_choice, label="From Day")
        
        self.fields['to_year'] = forms.ChoiceField(choices=year_choice, label='To Year')

        self.fields['to_month'] = forms.ChoiceField(choices=month_choice, label='To Month')

        self.fields['to_day'] = forms.ChoiceField(choices=date_choice, label='To Day')

        '''
        if 'from_year' in self.data:
            from_month = int(self.data['from_month'])
            from_year = int(self.data['from_year'])
            from_day = int(self.data['from_day'])
            to_day = int(self.data['to_day'])
            to_month = int(self.data['to_month'])
            to_year = int(self.data['to_year'])

            self.fields['from_month'] = forms.ChoiceField(
                choices=load_flw_from_month(from_year))
            self.fields['from_day'] = forms.ChoiceField(
                choices=load_flw_from_day(from_year, from_month))
            self.fields['to_year'] = forms.ChoiceField(
                choices=load_flw_to_year(from_year))
            self.fields['to_month'] = forms.ChoiceField(
                choices=load_flw_to_month(from_year, to_year, from_month))
            self.fields['to_day'] = forms.ChoiceField(choices=load_flw_to_day(
                from_year, to_year, from_month, to_month, from_day))

        '''
        
from accounts.models import Country, City

class RoomSearchForm(forms.Form):
    
    from_year = forms.ChoiceField(choices=[("", "------------")], label="From Year", required=True)
    from_month = forms.ChoiceField(choices=[("", "------------")], label="From Month" , required=True )
    from_day = forms.ChoiceField(choices=[("", "------------")], label="From Day", required=True)
    to_year = forms.ChoiceField(choices=[("", "------------")], label='To Year' , required=True )
    to_month = forms.ChoiceField(choices=[("", "------------")], label='To Month', required=True)
    to_day = forms.ChoiceField(choices=[("", "------------")], label='To Day' , required=True) 
    city = forms.ChoiceField(choices=[("", "------------")], label='City' , required=True)
    country = forms.ChoiceField(choices=[("", "------------")], label='Country' , required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        year_choice = [("", "choose year")]
        for i in range( datetime.date.today().year , datetime.date.today().year +2):
            year_choice += [(i, str(i))]
        
        month_choice = [("", "choose month")]
        for i in range( len(MyChoice.months) ):
            month_choice += [(MyChoice.months[i][0], MyChoice.months[i][1])]

        date_choice = [("", "choose date")]
        for i in range( len(MyChoice.dates) ):
            date_choice += [(MyChoice.dates[i][0], MyChoice.dates[i][1])]
        
        
        self.fields['from_year'] = forms.ChoiceField(choices=year_choice, label="From Year")

        self.fields['from_month'] = forms.ChoiceField(choices=month_choice, label="From Month")
        
        self.fields['from_day'] = forms.ChoiceField(choices=date_choice, label="From Day")
        
        self.fields['to_year'] = forms.ChoiceField(choices=year_choice, label='To Year')

        self.fields['to_month'] = forms.ChoiceField(choices=month_choice, label='To Month')

        self.fields['to_day'] = forms.ChoiceField(choices=date_choice, label='To Day')


        country_choice = [("", "choose country")]
        for i in Country.objects.all():
            country_choice += [(i.id, i.name)]
        
        self.fields['country'] = forms.ChoiceField(choices=country_choice, label='id_country' , required=True)

        city_choice = [("", "choose city")]
        for i in City.objects.all():
            city_choice += [(i.id, i.name)]
        
        self.fields['city'] = forms.ChoiceField(choices=city_choice, label='id_city' , required=True)