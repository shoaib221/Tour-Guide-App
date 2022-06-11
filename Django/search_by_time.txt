from homepage.base import *

class DateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        year_choice = [("", "------------")]
        for i in range(dt.today().year, dt.today().year+5):
            year_choice += [(str(i), str(i))]
        self.fields['year'] = forms.ChoiceField(choices=year_choice)
        self.fields['month'] = forms.ChoiceField(
            choices=[("", "------------")])
        self.fields['day'] = forms.ChoiceField(choices=[("", "------------")])
        self.fields['to_year'] = forms.ChoiceField(
            choices=[("", "------------")], label='Year')
        self.fields['to_month'] = forms.ChoiceField(
            choices=[("", "------------")], label='Month')
        self.fields['to_day'] = forms.ChoiceField(
            choices=[("", "------------")], label='Day')


class View1(views.View):
    template_name = 'search_by_time.html'

    def get(self, request):
        form = DateForm()
        print(form)
        return render(request, self.template_name, {'form': form})


urlpatterns = [
    path('', View1.as_view())
]


-> search_by_time.html
{% extends 'base.html' %}


{% block content_1 %}
<title>sbt</title>
{% endblock content_1 %}

<div id="test">hi</div>
<button id="b1">Click Me</button>

{% block content_2 %}
<div id="test"></div>

<form method="POST" enctype="multipart/form-data" novalidate>
    {% csrf_token %}
    <table>
        {{form.as_table}}
        <tr>
            <td></td>
            <td>
                <input type="submit" value="ENter">
            </td>
        </tr>
    </table>
</form>

<script id="date_ajax" load_to_year="/residence/ajax/load_to_year/" load_to_month="/residence/ajax/load_to_month/"
    load_to_day="/residence/ajax/load_to_day/" load_from_month="/residence/ajax/load_from_month/"
    load_from_day="/residence/ajax/load_from_day/">

        $("#b1").click(function () { $("#test").show(); });
        $("#b1").dblclick(function () { $("#test").hide(); });


        $("#id_from_year").change(function () {
            // $("#test").html('changed');
            var year = $(this).val();
            var url = $("#date_ajax").attr("load_from_month");
            // $("#test").html(url);

            $.ajax({
                url: url,
                data: { 'year': year },
                success: function (shoaib) { $("#id_from_month").html(shoaib); }
            });

            $.ajax({
                url: $("#date_ajax").attr("load_to_year"),
                data: { 'year': year },
                success: function (redata) { $("#id_to_year").html(redata) }
            });
        });

        $("#id_from_month").change(function () {
            var year = $("#id_from_year").val();
            var month = $("#id_from_month").val();
            var url = $("#date_ajax").attr("load_from_day");
            // $("#test").html('ok');
            $.ajax({
                url: url,
                data: { 'year': year, 'month': month },
                success: function (tasrif) { $("#id_from_day").html(tasrif); }
            });

            $.ajax({
                url: $("#date_ajax").attr("load_to_month"),
                data: { 'from_year': $("#id_from_year").val(), 'to_year': $("#id_to_year").val(), 'from_month': $("#id_from_month").val() },
                success: function (redata) { $("#id_to_month").html(redata); }
            });
        });

        $("#id_to_year").change(function () {
            // $("#test").html('ok');
            $.ajax({
                url: $("#date_ajax").attr("load_to_month"),
                data: { 'from_year': $("#id_from_year").val(), 'to_year': $("#id_to_year").val(), 'from_month': $("#id_from_month").val() },
                success: function (redata) { $("#id_to_month").html(redata); }
            });
        });

        $("#id_to_month").change(function () {
            $.ajax({
                url: $("#date_ajax").attr("load_to_day"),
                data: {
                    'from_year': $("#id_from_year").val(),
                    'from_month': $("#id_from_month").val(),
                    'from_day': $("#id_from_day").val(),
                    'to_year': $("#id_to_year").val(),
                    'to_month': $("#id_to_month").val(),
                },
                success: function (redata) { $("#id_to_day").html(redata); }
            });
        });

        $("#id_from_day").change(function () {
            $.ajax({
                url: $("#date_ajax").attr("load_to_day"),
                data: {
                    'from_year': $("#id_from_year").val(),
                    'from_month': $("#id_from_month").val(),
                    'from_day': $("#id_from_day").val(),
                    'to_year': $("#id_to_year").val(),
                    'to_month': $("#id_to_month").val(),
                },
                success: function (redata) { $("#id_to_day").html(redata); }
            });
        });


    </script>

{% endblock content_2 %}



month_array = ['', 'January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'Octobor', 'November', 'December']


def load_month(request):
    #    print(type(request.GET)) <class 'django.http.request.QueryDict'>
    year = request.GET.get('year', None)
    month = []
    if year:
        year = int(year)
        today_ = datetime.today()
        this_month = today_.month
        this_year = today_.year

        if year == this_year:
            month = [(str(i), month_array[i]) for i in range(this_month, 13)]
        else:
            month = [(str(i), month_array[i]) for i in range(1, 13)]
        # print(month)
        # for m, n in month:
        #    print(m, n)
    return render(request, 'load_month.html', {'month': month})


def load_day(request):
    # print('load_day')
    year = request.GET.get('year', None)
    month = request.GET.get('month', None)
    lb = 0
    ub = 0
    if year and month:
        year = int(year)
        month = int(month)
        td = datetime.today()

        if month in [1, 3, 5, 7, 8, 10, 12]:
            ub = 31
        elif month in [4, 6, 9, 11]:
            ub = 30
        else:
            if year % 400 == 0 or (year % 100 != 0 and year % 4 == 0):
                ub = 29
            else:
                ub = 28
        if year == td.year and month == td.month:
            lb = td.day
        else:
            lb = 1

    day_arr = [(str(i), str(i)) for i in range(lb, ub+1)]

    return render(request, 'load_day.html', {'day_arr': day_arr})


def load_to_year(request):
    from_year = request.GET.get('year', None)
    year_choice = []
    if from_year:
        from_year = int(from_year)
        for i in range(from_year, from_year+5):
            year_choice += [(str(i), str(i))]

    return render(request, 'load_to_year.html', {'years': year_choice})


def load_to_month(request):
    from_year = request.GET.get('from_year', None)
    to_year = request.GET.get('to_year', None)
    from_month = request.GET.get('from_month', None)

    lb = 0
    ub = -1
    if from_year and to_year and from_month:
        from_year = int(from_year)
        to_year = int(to_year)
        from_month = int(from_month)

        if from_year == to_year:
            lb = from_month
        else:
            lb = 1
        ub = 12

    month_choice = []
    for i in range(lb, ub+1):
        month_choice += [(str(i), month_array[i])]

    return render(request, 'load_to_month.html', {'months': month_choice})


def load_to_day(request):
    from_year = request.GET.get('from_year', None)
    to_year = request.GET.get('to_year', None)
    from_month = request.GET.get('from_month', None)
    to_month = request.GET.get('to_month', None)
    from_day = request.GET.get('from_day', None)

    days = []

    if from_month and from_year and from_day and to_year and to_month:
        from_day = int(from_day)
        from_month = int(from_month)
        from_year = int(from_year)
        to_year = int(to_year)
        to_month = int(to_month)
        lb = 0
        ub = 0

        if from_year == to_year and from_month == to_month:
            lb = from_day
        else:
            lb = 1

        if to_month in [1, 3, 5, 7, 8, 10, 12]:
            ub = 31
        elif to_month in [4, 6, 9, 11]:
            ub = 30
        else:
            if to_year % 400 == 0 or (to_year % 100 != 0 and to_year % 4 == 0):
                ub = 29
            else:
                ub = 28

        for i in range(lb, ub+1):
            days += [(str(i), str(i))]

    return render(request, 'load_to_day.html', {'days': days})


urlpatterns = [
    path('load_month/', load_month),
    path('load_day/', load_day),
    path('load_to_year/', load_to_year),
    path('load_to_month/', load_to_month),
    path('load_to_day/', load_to_day),
]

'''
-> load_month.html
<option value="" selected>------------</option>
{% for m,n in month %}
<option value="{{m}}">{{n}}</option>
{% endfor %}

'''
