
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from residence.models import *
from .serializers import *
from accounts.models import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, authenticate, logout

class Test(APIView):

    def get(self, request):
        return Response( { 'message': 'Hello Get test' } , status=status.HTTP_200_OK )
    
    def post(self, request):
        return Response( { 'message': 'Hello Post test' } , status=status.HTTP_200_OK )
    
    def put(self, request):
        return Response( { 'message': 'Hello Put test' } , status=status.HTTP_200_OK )


###########################################  accounts  ###########################################



class MyRegister(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            context = {
                'message': 'Already Registered'
            }
            return Response( context , status=status.HTTP_200_OK)
        else:
            serializer = UserDetailSerializer()
            qs = Country.objects.all()
            country_serializer = CountrySerializer(qs, many=True)
            context = {
                'user_detail': serializer.data,
                'country': country_serializer.data
            }
            return Response(context , status=status.HTTP_200_OK )

    def post(self, request):

        if request.user.is_authenticated:
            context = {
                'message': 'Already Registered'
            }
            return Response( context , status=status.HTTP_200_OK)
        
        else:

            serializer = UserDetailSerializer(data=request.data)
            #print(request.data)
            #print(serializer.data)

            if serializer.is_valid():
                user_detail = UserDetail()
                user_detail.username = serializer.validated_data['mail']
                user_detail.country = serializer.validated_data['country']
                user_detail.nid = serializer.validated_data['nid']
                user_detail.mobile = serializer.validated_data['mobile']
                user_detail.mail = serializer.validated_data['mail']
                user_detail.password = make_password( serializer.validated_data['password'] )

                #print(serializer.validated_data)
                #print(serializer.data)
                #print(user_detail.password)

                try:
                    user_detail.full_clean()
                    user_detail.save()
                    context = {
                        'message': 'successfully registered',
                        'serializer': serializer.data
                    }
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except ValidationError as ve:
                    context = {
                        'errors': ve.message_dict,
                        'serializer': serializer.data
                    }
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)
                
            else:
                context={
                    'errors': serializer.errors,
                    'serializer': serializer.data
                }
                return Response(context , status=status.HTTP_400_BAD_REQUEST)
            

class MyLogin(APIView):

    template_name = "login.html"
    form_class = LoginSerializer

    def post(self, request):
        
        if request.user.is_authenticated:
            context = {
                'message': 'Already logged in'
            }
            return Response( context , status=status.HTTP_200_OK)
        
        else:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                mail = serializer.validated_data['mail']
                password = serializer.validated_data['password']
                user = UserDetail.objects.get(mail=mail)
                if user is None:
                    
                    context = {
                        'message': 'No such user, Regester',
                        'serializer': serializer.data
                    }
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)
                
                elif check_password(password, user.password):
                    login(request, user)
                    context = {
                        'message': 'Successfully logged in',
                    }
                    return Response(context, status=status.HTTP_200_OK)

                else:
                    context = {
                        'message': 'Incorrect Password',
                        'serializer': serializer.data
                    }
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)
            else:
                context = {
                    'errors': serializer.errors,
                    'serializer': serializer.data
                }
                return Response( context , status=status.HTTP_200_OK)
            

    def get(self, request):
        if request.user.is_authenticated:
            context = {
                'message': 'Already logged in'
            }
            return Response( context , status=status.HTTP_200_OK)
        else:
            #print(request.data)
            #print(request.user)
            serializer = LoginSerializer()
            return Response(serializer.data, status=status.HTTP_200_OK)


class MyLogout(APIView):
        
        def get(self, request):

            if request.user.is_authenticated:
                logout(request)
                context = {
                    'message': 'Successfully logged out'
                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {
                    'message': 'Already logged out'
                }
                return Response(context, status=status.HTTP_200_OK)
            

class MyProfile(APIView):

    def get( self, request ):
        if request.user.is_authenticated:
            user_detail = UserDetail.objects.get(username=request.user.username)
            serializer = MyProfileSerializer(user_detail)
            context = {'user_detail': serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                'message': 'Log in first'
            }
            return Response(context, status=status.HTTP_200_OK)
        

class ShowProfileDetail(APIView):

    def get(self, request, user_id):

        if request.user.is_authenticated:
            user_detail = UserDetail.objects.get(id=user_id)
            if user_detail is None:
                return Response( { "message": "No such user" } ,status=status.HTTP_400_BAD_REQUEST)
            serializer = MyProfileSerializer(user_detail)
            context = {'user_detail': serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                'message': 'Log in first'
            }
            return Response(context, status=status.HTTP_200_OK)



#######################################  house  #############################################

class MyHouse(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            qs = House.objects.filter( user_detail__username=request.user.username )
            serializer = HouseSerializer(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            context = {
                'message': 'Log in first'
            }
            return Response(context, status=status.HTTP_200_OK)
        

        
class AddHouse(APIView) :

    def get(self, request):
        if request.user.is_authenticated:
            serializer = HouseSerializer()

            user_detail = UserDetail.objects.get(username=request.user.username)
            cities = City.objects.filter( country = user_detail.country )
            cs = CitySerializer(cities, many=True)
            context = {
                'serializer': serializer.data,
                'cities': cs.data
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                'message': 'Log in first'
            }
            return Response(context, status=status.HTTP_200_OK)
    
    def post(self, request):
        if request.user.is_authenticated:
            serializer = HouseSerializer(data=request.data)

            if serializer.is_valid():
                
                user_detail = UserDetail.objects.get(username=request.user.username)

                house = House()
                house.user_detail = user_detail
                house.name = serializer.validated_data['name']
                house.address = serializer.validated_data['address']
                house.city = serializer.validated_data['city']
                house.country = serializer.validated_data['country']
                house.description = serializer.validated_data['description']


                try:
                    house.full_clean()
                    house.save()
                    context = {
                        'message': 'successfully created',
                        'serializer': serializer.data
                    }
                    return Response(context , status=status.HTTP_201_CREATED)
                except ValidationError as e:
                    context = {
                        'errors': e.message_dict,
                        'serializer': serializer.data
                    }
                    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
                
            else:
                context = {
                    'errors': serializer.errors,
                    'serializer': serializer.data
                }
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        else:
            context = {
                'message': 'Log in first'
            }
            return Response(context, status=status.HTTP_200_OK)



#########################  Room          #########################################
'''

class AllHouse(APIView):
    def get(self, request):
        all_house = House.objects.all()
        serializer = HouseSerializer(all_house, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HouseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)
    
class HouseDetail(APIView):
    def get(self, request, house_id):
        house = House.objects.get(id=house_id)
        serializer = HouseSerializer(house)
        return Response(serializer.data)

    def put(self, request, house_id):
        house = House.objects.get(id=house_id)
        serializer = HouseSerializer(house, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data)

    def delete(self, request, house_id):
        house = House.objects.get(id=house_id)
        house.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


from django import views
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, auth
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django import views
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from .serializers import CreateUserForm, LoginForm, PasswordChangeForm
from .models import UserDetail, City, Country
from django.contrib.auth.hashers import make_password, check_password



class MyHome(views.View):
    template_name = "home.html"

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        else:
            return redirect('/accounts/login/')
    


class MyProfile(views.View):
    template_name = 'profile.html'

    def get(self, request):
        if request.user.is_authenticated:
            user_detail = UserDetail.objects.get( username=request.user.username )
            context = {'user_detail': user_detail}
            return render(request, self.template_name, context)
        else:
            messages.info(request, 'Log in first')
            return redirect('/accounts/')
        
    def post(self, request):
        if request.user.is_authenticated:
            user_detail = UserDetail.objects.get( username=request.user.username )
            context = {'user_detail': user_detail}
            return render(request, self.template_name, context)
        else:
            messages.info(request, 'Log in first')
            return redirect('/accounts/')


        
class ForgotPassword(views.View):
    
    def get(self, request):
        return render(request, 'forgot_password.html')
    
    def post(self, request):
        aha=0


class ShowProfileDetail(views.View):
    def get(self, request, user_id):
        user_detail = UserDetail.objects.get(pk=user_id)
        return render(request, "profile.html", { 'user_detail': user_detail})


############################ update profile ############################

from .serializers import UpdateMobileForm, UpdateMailForm, UpdateNameForm


class ChangePassword(views.View):
    template_name = 'change_password.html'
    form_class = PasswordChangeForm

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        else:
            messages.info(request, 'You must log in first')
            return redirect('/accounts/')

    def post(self, request):

        if request.user.is_authenticated:
            user = request.user
            form = self.form_class(request.POST or None)

            if form.is_valid():
                username = user.username
                password = form.cleaned_data['current_password']
                new_pass = form.cleaned_data['new_password']
                confirm_pass = form.cleaned_data['confirm_password']
                auth_user = authenticate(
                    request, username=username, password=password)
                if auth_user is not None:
                    if new_pass == confirm_pass:
                        auth_user.set_password(new_pass)
                        print('cppost')
                        auth_user.save()
                        login(request, auth_user)
                        return redirect('/home/')
                    else:
                        messages.info(request, 'Passwords not matching')
                        return redirect('/change_password/')
                else:
                    messages.info(request, 'Permission denied')
                    return redirect('/underground/')
            else:
                return render(request, self.template_name, {'form': form})
        else:
            messages.info(request, 'You must log in first')
            return redirect('/')


from .serializers import UpdateNameForm

class UpdateName(views.View):
    

    def get(self, request):
        if request.user.is_authenticated:
            form = UpdateNameForm()
            return render(request, 'update_name.html', {'form': form})
        else:
            messages.info(request, 'You must log in first')
            return redirect('/accounts/')
    
    def post(self, request):

        if request.user.is_authenticated:
            form = UpdateNameForm(request.POST or None)
            
            if form.is_valid():
                name = form.cleaned_data['name']
                user_detail = UserDetail.objects.get(username=request.user.username)
                user_detail.name = name
                user_detail.save()
                return redirect( "/accounts/my_profile/" )
            else:
                return render(request, 'update_name.html', {'form': form})
            
        else:
            messages.info(request, 'You must log in first')
            return redirect('/accounts/')
        
from .serializers import UpdateMailForm

class UpdateEmail(views.View):
    

    def get(self, request):
        if request.user.is_authenticated:
            form = UpdateMailForm()
            return render(request, 'update_mail.html', {'form': form})
        else:
            messages.info(request, 'You must log in first')
            return redirect('/accounts/')
    
    def post(self, request):

        if request.user.is_authenticated:
            form = UpdateNameForm(request.POST or None)
            
            if form.is_valid():
                mail = form.cleaned_data['mail']
                user_detail = UserDetail.objects.get(username=request.user.username)
                user_detail.mail = mail
                try:
                    user_detail.save()
                    return redirect( "/accounts/my_profile/" )
                except:
                    form.add_error('mail', 'Email Address Taken')
                    return render(request, 'update_mail.html', {'form': form})
            else:
                return render(request, 'update_name.html', {'form': form})
            
        else:
            messages.info(request, 'You must log in first')
            return redirect('/accounts/')

from .serializers import UpdateMobileForm



class UpdateMobile(views.View):
    
    def get(self, request):
        if request.user.is_authenticated:
            form = UpdateMobileForm()
            return render(request, 'update_mobile.html', {'form': form})
        else:
            messages.info(request, 'You must log in first')
            return redirect('/accounts/')
    
    def post(self, request):

        if request.user.is_authenticated:
            form = UpdateMobileForm(request.POST or None)
            
            if form.is_valid():
                mobile = form.cleaned_data['mobile']
                user_detail = UserDetail.objects.get(username=request.user.username)
                user_detail.mobile = mobile
                try:
                    user_detail.save()
                    return redirect( "/accounts/my_profile/" )
                except:
                    form.add_error('mobile', 'Mobile Number Taken')
                    return render(request, 'update_mobile.html', {'form': form})
            else:
                return render(request, 'update_mobile.html', {'form': form})
            
        else:
            messages.info(request, 'You must log in first')
            return redirect('/accounts/')




###################################### Orders ######################################




from datetime import date
import datetime
from pyexpat.errors import messages
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django import views
from .models import House, Room
from .serializers import HouseForm, RoomForm
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
	template_name = 'add_space.html'
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
			unavail = RoomUnavailable.objects.filter(room=room)
			return render(request, self.template_name, {'room': room, 'unavails': unavail })
		else:
			messages.info(request, 'Log in First')
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
					new_unavail = RoomUnavailable( room=room, from_day=from_date, to_day=to_date, house=room.house )  
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

from .serializers import RoomSearchForm
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
			obj = Cart( user_detail=user_detail, room=room, house=room.house, book_from=start_date, book_to=end_date, price=room.price )
			try:
				obj.full_clean()
				obj.save()
				print("added to cart")
				return render(request, 'message.html', {'message': 'Added to cart'} )
			except ValidationError as e:
				return render(request, 'message.html', {'message': 'failed'} )
		else:
			messages.info(request, 'You must log in first')
			return redirect('/accounts/')
		
from residence.models import Cart



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
			house=House.objects.get(id=rows[0].house.id)
			start_date = rows[0].book_from
			end_date = rows[0].book_to
			total_price=0
			for x in rows:
				total_price += x.price
			now_time=datetime.datetime.now()
			booking = Booking( guest=guest, house=house, book_from=start_date, book_to=end_date, total_price=total_price, booking_time=now_time )

			try:
				booking.full_clean()
				booking.save()
				for x in rows:
					room_booking = RoomBooking( booking=booking, room=x.room, price=x.price )
					try:
						room_booking.full_clean()
						room_booking.save()
					except ValidationError as e:
						return render(request, 'message.html', {'message': 'failed'} )
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
			orders = Booking.objects.filter(guest__username=request.user.username).order_by("-booking_time")
			return render(request, self.template_name, {"orders": orders})
		else:
			messages.info(request, 'You must log in first')
			return redirect("/accounts/")



class OrderDetail(views.View):
	template_name = "order_detail.html"
	
	def get(self, request, id):
		if request.user.is_authenticated:
			order = Booking.objects.get(id=id)
			if order.guest.username == request.user.username :
				return render(request, self.template_name, {"order": order})
			else:
				return redirect("/accounts/")
		else:
			return redirect("/login_required/")


            
'''