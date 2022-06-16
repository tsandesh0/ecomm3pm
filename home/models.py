from django.db import models

# Create your models here.
# category
# subcategory
# ads
# slider
# product
# brand

class Category(models.Model):
	name = models.CharField(max_length = 300)
	slug = models.TextField()
	status = models.CharField(max_length = 50,blank = True ,choices = (('active','Active'),('','Default')))

	def __str__(self):
		return self.name


class SubCategory(models.Model):
	name = models.CharField(max_length = 300)
	category = models.ForeignKey(Category, on_delete = models.CASCADE,default = 1)
	slug = models.TextField()

	def __str__(self):
		return self.name

class Ad(models.Model):
	name = models.CharField(max_length = 300)
	image = models.ImageField(upload_to = 'media')
	link = models.URLField(max_length=500 ,blank =True)
	rank = models.IntegerField()

	def __str__(self):
		return self.name

class Slider(models.Model):
	name = models.CharField(max_length = 400)
	image = models.ImageField(upload_to = 'media')
	rank = models.IntegerField()
	status = models.CharField(max_length = 300 ,blank = True ,choices = (('active','Active'),('','Default')))

	def __str__(self):
		return self.name

LABELS = (('offer','offer'),('new','new'),('hot','hot'),('','default'))
class Product(models.Model):
	name = models.CharField(max_length = 500)
	image = models.ImageField(upload_to = 'media')
	price = models.IntegerField()
	discounted_price = models.IntegerField(default = 0)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)
	subcategory = models.ForeignKey(SubCategory, on_delete = models.CASCADE)
	discription = models.TextField(blank = True)
	status = models.CharField(max_length = 50 , choices = (('active','Active'),('','Default')))
	labels = models.CharField(max_length = 500 , choices = LABELS,blank = True)
	slug = models.TextField()

	def __str__(self):
		return self.name


class Cart(models.Model):
	username = models.CharField(max_length = 400)
	slug = models.CharField(max_length = 500)
	items = models.ForeignKey(Product, on_delete = models.CASCADE)
	quantity = models.IntegerField(default = 1)
	checkout = models.BooleanField(default = False)
	total = models.IntegerField(default = 1)

	def __str__(self):
		return self.username




