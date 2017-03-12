from django.db import models

class Polls(models.Model):
	name = models.CharField(max_length=30)
	picture = models.CharField(max_length=60)
	pub_date = models.DateTimeField('date published')