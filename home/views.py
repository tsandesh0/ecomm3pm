from django.shortcuts import render
from django.views.generic import View
from .models import *

# Create your views here.
class BaseView(View):
	views = {}
	views['categories'] = Category.objects.all()
	views['subcategories'] = SubCategory.objects.all()



class HomeView(BaseView):
	def get(self,request):
		self.views['categories'] = Category.objects.all()
		self.views['subcategories'] = SubCategory.objects.all()
		self.views['products'] = Product.objects.all()
		self.views['offers'] = Product.objects.filter(labels = 'offer')
		self.views['new'] = Product.objects.filter(labels = 'new')
		self.views['hots'] = Product.objects.filter(labels = 'hot')
		self.views['sliders'] = Slider.objects.all()
		self.views['ads'] = Ad.objects.all()





		return render(request,'index.html',self.views)