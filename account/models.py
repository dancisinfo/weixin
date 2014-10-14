from django.db import models

# Create your models here.
class account(models.Model):
	openid = models.CharField(max_length=50,unique=True)
	point = models.IntegerField()
	wxname = models.CharField(max_length=50)
	alipay= models.CharField(max_length=20,null=True,unique=False)
	name = models.CharField(max_length=20,null=True,unique=False)
	mobile = models.CharField(max_length=20,null=True,unique=False)
	
class mission(models.Model):
	user = models.ForeignKey(account)
	task = models.CharField(max_length=20)
	time = models.DateTimeField(auto_now_add=True)
	point = models.IntegerField()
	
class pay(models.Model):
	user = models.ForeignKey(account)
	point = models.IntegerField()
	apply_time = models.DateTimeField(auto_now_add=True)
	deal_time = models.DateTimeField()
	status = models.IntegerField()
	orderID = models.CharField(max_length=20)