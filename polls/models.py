from django.db import models
import os

class Poll(models.Model):
	
	name = models.CharField(max_length=30, null=True)
	description = models.CharField(max_length=300, null=True)
	category = models.CharField(max_length=60, null=True)
	# puth = 'media/polls/static/'
	code = models.TextField(null=True)
	pub_date = models.DateTimeField(auto_now_add=True)
	image = models.FileField(upload_to='polls/static', null=True)
	picture = models.CharField(max_length=60, default= 'static/', help_text="input filename.type")