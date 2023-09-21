

from ctypes import sizeof
from datetime import date
import datetime
from pyexpat.errors import messages
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django import views
from .models import House, Room
from .forms import HouseForm, RoomForm
from accounts.models import UserDetail


##########################################      House     #####################################################


class MyHouse(views.View):
	template_name = 'my_house.html'
	
	def get(self, request):
		if request.user.is_authenticated:
			qs = House.objects.filter( user_detail__username=request.user.username )
			context = { 'qs': qs }
			return render(request, self.template_name, context)
		else:
			messages.info(request, 'Log in First')
			return redirect('/accounts/')


class AddHouse(views.View):
	form_class = HouseForm
	template_name = 'add_house.html'
	
	def get(self, request):
		if request.user.is_authenticated:
			form = self.form_class()
			return render(request, self.template_name, {'form': form})
		else:
			return redirect("/accounts/login/")
	
	def post(self, request):
		if request.user.is_authenticated:
			form = self.form_class(request.POST, request.FILES)
			if form.is_valid():
				ob = form.save(commit=False)
				ob.user_detail = UserDetail.objects.get(username=request.user.username)
				ob.country = ob.city.country
				try:
					ob.save()
					return redirect( "/residence/my_house/" )
				except ValidationError as e:
					for kk in e.message_dict:
						form.add_error(kk, e.message_dict[kk])
					return render(request, self.template_name, {'form': form})
			else:
				return render(request, self.template_name, {'form': form})
		else:
			return redirect("/accounts/")


class HouseDetail(views.View):
	template_name = 'house_detail.html'
	
	def get(self, request, id):
		house = House.objects.get(id=id)
		rooms = Room.objects.filter(house_id=id)
		orders = Booking.objects.none()
		if request.user.is_authenticated and house.user_detail.username == request.user.username:
			orders = Booking.objects.filter(house_id=house)
		print(id)
		print(house.address)
		context = {'house': house, 'rooms': rooms, 'orders': orders }
		return render(request, self.template_name, context  )


##################################       Rooms       ##############################################################


class AddRoom(views.View):
	template_name = 'add_room.html'
	form_class = RoomForm
	
	def get(self, request, id):
		if request.user.is_authenticated:
			house = House.objects.get(id=id)
			if house.user_detail.username == request.user.username:
				form = self.form_class()
				return render(request, self.template_name, {'form': form})
			else:
				messages.info(request, 'Permission denied')
				redirect('/accounts/')
		else:
			messages.info(request, 'Log in First')
			return redirect('/accounts/')
	
	def post(self, request, id):
		if request.user.is_authenticated:
			house = House.objects.get(id=id)
			if house.user_detail.username == request.user.username:
				form = self.form_class(request.POST, request.FILES)
				if form.is_valid():
					ob = form.save(commit=False)
					ob.house = house
					try:
						ob.full_clean()
						ob.save()
						return redirect('/residence/house/{}/'.format(house.id))
					except ValidationError as ve:
						for kk in ve.message_dict:
							form.add_error(kk, ve.message_dict[kk])
						return render(request, self.template_name, {'form': form})
				else:
					messages.info('Invalid Credentials')
					return render(request, self.template_name, {'form': form})
			else:
				messages.info(request, 'Permission denied')
				return redirect('/accounts/')
		else:
			messages.info(request, 'Log in First')
			return redirect('/accounts/')


class RoomDetail(views.View):
	template_name = 'room_detail.html'
	
	def get(self, request, id):

		if request.user.is_authenticated:
			print("room_detail")
			room = Room.objects.get(id=id)
			unavail = RoomUnavailable.objects.filter(room=room, booked=False).order_by("from_day")
			bookings =  RoomBooking.objects.filter(room_id=id)
			qs = []
			for x in bookings:
				qs.append(x.booking)

			print( len( bookings ) )

			context = {'room': room, 'unavails': unavail, 'bookings': qs }
			return render(request, self.template_name, context )
		else:
			request.message.info('Log in First')
			return redirect('/accounts/')

		
############################################    Availability        ################################################
from . import forms
from . import pre_view

class CreateUnavailability(views.View):

	template_name = "create_availability.html"
	form_class = forms.CreateUnavaiabilityForm
	
	def get(self, request, room_id):
		
		if request.user.is_authenticated:
			room = Room.objects.get(id=room_id)
			if room.house.user_detail.username == request.user.username:
				form = self.form_class()
				return render(request, self.template_name, {'form': form, "space": room })
			else:
				return redirect("/accounts/")
		else:
			return redirect('/accounts/')
	

	def post(self, request, room_id):
		
		if request.user.is_authenticated:
			room = Room.objects.get(id=room_id)
			if room.house.user_detail.username == request.user.username:
				form = self.form_class(request.POST or None)
				if form.is_valid():
					from_date, to_date = pre_view.load_date_from_DateForm(form)
					new_unavail = RoomUnavailable( room=room, from_day=from_date, to_day=to_date, house=room.house, booked=False )  
					try:
						new_unavail.full_clean()
						new_unavail.save()
						print("created unavail successfully")
						return redirect("/residence/room/{}/".format(room.id))
					except ValidationError as e :
						for kk in e.message_dict:
							form.add_error(kk, e.message_dict[kk])
						return render(request, self.template_name, {'form': form, "space": room })
				else:
					return render(request, self.template_name, {'form': form, "space": room })
			else:
				messages.info(request, 'Permission denied')
				return redirect("/accounts/")
		else:
			messages.info(request, 'Log in First')
			return redirect('/accounts/')

from .models import RoomUnavailable


class DeleteUnavailability(views.View):
	
	
	def get(self, request, id):
		if request.user.is_authenticated:
			unavail = RoomUnavailable.objects.get(id=id)
			if unavail.house.user_detail.username == request.user.username:
				unavail.delete()
				return redirect("/residence/room/{}/".format(unavail.room.id))
			else:
				messages.info(request, 'Permission denied')
				return redirect('/accounts/')
		else:
			messages.info(request, 'Log in First')
			return redirect('/accounts/')
		



###########################################   Search #######################################

from .forms import RoomSearchForm
from accounts.models import Country, City

class SearchRoom(views.View):

	form_class = forms.RoomSearchForm

	def get(self, request):
		if request.user.is_authenticated:
			context = {
				'form': self.form_class(),
			}
			return render(request, 'search_room.html', context  )
		else:
			messages.info(request, 'You must log in first')
			return redirect('/accounts/')
		
	def post( self, request ):

		if request.user.is_authenticated:
			form = self.form_class(request.POST)

			if form.is_valid():
				from_date, to_date = pre_view.load_date_from_DateForm(form)
				city_id = form.cleaned_data['city']


				qs = RoomUnavailable.objects.all()
				qs = qs.filter(house__city_id=city_id)
				qs = qs.filter(from_day__lte=to_date, to_day__gte=from_date)

				unavail = set()
				for x in qs:
					unavail.add(x.room.id)
				
				ase = Room.objects.all()
				ase = ase.filter(house__city_id=city_id)

				ans = []

				for x in ase:
					if x.id not in unavail:
						ans.append( x )
				
				return render(request, 'search_room.html', {'form': form, 'qs': ans})
			else:
				return render(request, 'search_room.html', {'form': form})
		else:
			messages.info(request, 'You must log in first')
			return redirect('/accounts/')
		
from .models import Cart


class AddToCart(views.View):

	def get(self, request, room_id):
		if request.user.is_authenticated:
			room = Room.objects.get(id=room_id)		
			user_detail = UserDetail.objects.get(username=request.user.username)
			start_date = request.GET.get('start_date')
			end_date = request.GET.get('end_date')
			cart = Cart()

			cart = Cart()
			cart.user_detail = user_detail
			cart.room = room
			cart.house = room.house
			cart.book_from = start_date
			cart.book_to = end_date
			number_of_days = (cart.book_to - cart.book_from).days
			cart.price_per_day = room.price * number_of_days
			try:
				cart.full_clean()
				cart.save()
				print("added to cart")
				return render(request, 'message.html', {'message': 'Added to cart'} )
			except ValidationError as ve:
				context = {
					'message': 'Failed to add to cart',
					'errors': ve.message_dict
				}
				return render(request, 'message.html', context )
		else:
			messages.info(request, 'You must log in first')
			return redirect('/accounts/')


class MyCart(views.View):

	template_name = "cart.html"
	
	def get(self, request):
		if request.user.is_authenticated:
			qs= Cart.objects.filter(user_detail__username=request.user.username)
			return render(request, self.template_name, {'qs': qs}	 )
		else:
			messages.info(request, 'You must log in first')
			return redirect('/accounts/')


######################################   RoomBookings    ####################################


from .models import Booking, House, RoomBooking



class BookRooms(views.View):

	def get(self, request):
		if request.user.is_authenticated:
			rows = Cart.objects.filter(user_detail__username=request.user.username)
			rooms=[]
			for x in rows:
				rooms.append(x.room.id)
			guest=UserDetail.objects.get(username=request.user.username)

			if( len(rooms)<1 ) :
				return render(request, 'message.html', {'message': 'failed'} )

			house=House.objects.get(id=rows[0].house.id)

			house_id = set()

			for x in rows:
				house_id.add(x.house.id)

			if( len(house_id)>1 ):
				return render(request, 'message.html', {'message': 'failed'} )
			
			total_price=0
			for x in rows:
				total_price += x.price
			
			now_time=datetime.datetime.now()
			booking = Booking( guest=guest, house=house, total_price=total_price, booking_time=now_time )

			try:
				booking.full_clean()
				booking.save()
				temp = []
				for x in rows:
					room_booking = RoomBooking( booking=booking, room=x.room, price=x.price, start_date=x.book_from, end_date=x.book_to )
					try:
						room_booking.full_clean()
						room_booking.save()
						temp.append(room_booking)
					except ValidationError as e:
						for t in temp:
							t.delete()
						return render(request, 'message.html', {'message': 'failed'} )
				
				for x in rows:
					new_unavail = RoomUnavailable( room=x.room, from_day=x.book_from, to_day=x.book_to, house=x.room.house, booked=True  ) 
					new_unavail.save()
				
				cart_elements = Cart.objects.filter(user_detail__username=request.user.username)
				for x in cart_elements:
					x.delete()
				return redirect("/residence/my_booking/")
			
			except ValidationError as e:
				return render(request, 'message.html', {'message': 'failed'} )
			
		else:
			messages.info(request, 'You must log in first')
			return redirect('/accounts/')
		
		

class MyBookings(views.View):
	template_name = "my_booking.html"
	
	def get(self, request):
		if request.user.is_authenticated:
			bookings = Booking.objects.filter(guest__username=request.user.username).order_by("-booking_time")
			return render(request, self.template_name, {"orders": bookings})
		else:
			messages.info(request, 'You must log in first')
			return redirect("/accounts/")



class BookingDetail(views.View):

	template_name = "booking_detail.html"

	def get(self, request, id):
		if request.user.is_authenticated:
			booking = Booking.objects.get(id=id)
			if booking.guest.username == request.user.username or booking.house.user_detail.username == request.user.username :
				qs = RoomBooking.objects.filter(booking_id=id)
				rooms = []
				for x in qs:
					rooms.append(x.room)
				return render(request, self.template_name, { "booking": booking, "rooms": rooms })
			else:
				return redirect("/accounts/")
		else:
			return redirect("/login_required/")