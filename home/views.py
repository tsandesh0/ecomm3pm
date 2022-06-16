from django.shortcuts import render,redirect
from django.views.generic import View
from .models import *

# Create your views here.
class BaseView(View):
	views = {}
	views['categories'] = Category.objects.all()
	views['subcategories'] = SubCategory.objects.all()
	views['sliders'] = Slider.objects.all()
	views['ads'] = Ad.objects.all()


class HomeView(BaseView):
	def get(self,request):
		self.views
		self.views['products'] = Product.objects.all()
		self.views['offers'] = Product.objects.filter(labels = 'offer')
		self.views['new'] = Product.objects.filter(labels = 'new')
		self.views['hots'] = Product.objects.filter(labels = 'hot')

		return render(request,'index.html',self.views)

class SubcategoryView(BaseView):
	def get(self,request,slug):
		subcatid = SubCategory.objects.get(slug = slug).id
		self.views['subcat_product'] = Product.objects.filter(subcategory_id = subcatid)

		return render(request,'kitchen.html',self.views)

class DetailView(BaseView):
	def get(self,request,slug):
		self.views['detail_product'] = Product.objects.filter(slug = slug)

		return render(request,'single.html',self.views)

class SearchView(BaseView):
	def get(self,request):
		if request.method == 'GET':
			query = request.GET['search']
			if query != '':
				self.views['search_product']= Product.objects.filter(name__icontains = query)
			else:
				return redirect('/')

		return render(request,'search.html',self.views)

from django.contrib import messages,auth
from django.contrib.auth.models import User
def signup(request):
	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		cpassword = request.POST['cpassword']

		if password == cpassword:
			if User.objects.filter(username = username).exists():
				messages.error(request,'USERNAME ALREADY EXISTS')
				return redirect('/register')
			elif User.objects.filter(email = email).exists():
				messages.error(request,'EMAIL ALREADY EXISTS')
				return redirect('/register')
			else:
				user = User.objects.create_user(
					username = username,
					email = email,
					password = password
					)
				user.save()
				return redirect('/')
		else:
			messages.error(request,'PASSWORD DOES NOT MATCH')
			return redirect('/register')


	return render(request,'register.html')

from django.contrib.auth import login,logout

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username = username, password = password)
		if user is not None:
			auth.login(request,user)
			return redirect('/')

		else:
			messages.error(request,'Username and Password Does Not Match')
			return redirect('/login')

	return render(request,'login.html')

def logout(request):
	auth.logout(request)
	return redirect('/')

def cal_cart(slug,username):
	if Cart.objects.filter(username = username ,slug = slug , checkout = False).exists():
		quantity = Cart.objects.get(username = username, slug = slug , checkout = False).quantity
	else:
		quantity = 1
	price = Product.objects.get(slug = slug).price
	discounted_price = Product.objects.get(slug = slug).discounted_price
	if discounted_price > 0 :
		original_price = discounted_price
	else:
		original_price = price

	return original_price,quantity

def cart(request,slug):
	username = request.user.username
	if Cart.objects.filter(username = username, slug = slug , checkout = False).exists():
		original_price,quantity = cal_cart(slug,username)
		quantity = quantity+1
		total = original_price * quantity
		Cart.objects.filter(username = username, slug = slug , checkout = False).update(quantity = quantity , total = total)
		return redirect('/my_cart/')

	else:
		username = request.user.username
		original_price,quantity = cal_cart(slug,username)
		data = Cart.objects.create(
			username = username,
			slug = slug,
			items = Product.objects.filter(slug = slug)[0],
			total = original_price
			)
		data.save()

		return redirect('/my_cart/')


def delete_cart(request,slug):
	username = request.user.username
	if Cart.objects.filter(username = username, slug = slug , checkout = False).exists():
		Cart.objects.filter(username = username ,slug = slug ,checkout = False).delete()
		return redirect('/my_cart/')

def reduce_cart(request,slug):
	username = request.user.username
	if Cart.objects.filter(username = username, slug = slug , checkout = False).exists():
		original_price,quantity = cal_cart(slug,username)
		quantity = quantity-1
		total = original_price * quantity
		Cart.objects.filter(username = username, slug = slug , checkout = False).update(quantity = quantity , total = total)
		return redirect('/my_cart/')

class CartView(BaseView):
	def get(self,request):
		username = request.user.username
		self.views['cart_product'] = Cart.objects.filter(username = username , checkout = False)

		return render(request,'wishlist.html',self.views)


#--------------API-----------------------

from rest_framework import serializers, viewsets
from .serializers import *

# ViewSets define the view behavior.
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ItemSerializer



import django_filters.rest_framework
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter

class ItemFilterViewSet(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter,SearchFilter]
    filter_filelds = ['id','category','subcategory','labels','status']
    ordering_fields = ['price','id','name']
    search_fields = ['name','description']


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class CRUDItemViewSet(APIView):
	def get_object(self,pk):
		#try 
		return Product.objects.get(pk = pk)
		#except:
			#print("The id does not exists. ")

	
	def get(self,request,pk,format = None):
		product_data = self.get_object(pk)
		serializer = ItemSerializer(product_data)
		return Response(serializer.data)

	def post(self,request,pk,format = None):
		serializer = ItemSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({'status':'The value is posted'})


	def put(self,request,pk,format = None):
		product_data = self.get_object(pk)
		serializer = ItemSerializer(product_data ,data = request.data , partial = True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)

		return Response({'status ':"The value is updated"})


	def delete(self,request,pk):
		try:
			Product.objects.filter(id = pk).delete()
			return Response({'status':"The object is deleted"})
		except:
			return Response({'status':"The object is already deleted"})

