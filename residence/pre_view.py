       

from datetime import date, timedelta
import datetime
from .models import House, Room, RoomUnavailable, RoomBooking, Booking



month_array = ['', 'January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'Octobor', 'November', 'December']


def load_date_from_DateForm(form):
    
    year = int(form.cleaned_data['from_year'])
    month = int(form.cleaned_data['from_month'])
    day = int(form.cleaned_data['from_day'])
    from_date = date(year, month, day)
    year = int(form.cleaned_data['to_year'])
    month = int(form.cleaned_data['to_month'])
    day = int(form.cleaned_data['to_day'])
    to_date = date(year, month, day)
    return from_date, to_date


    
