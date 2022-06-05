from django.shortcuts import render
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