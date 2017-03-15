from django.db import models

class Poll(models.Model):
	name = models.CharField(max_length=30, null=True)
	description = models.CharField(max_length=300, null=True)
	category = models.CharField(max_length=60, null=True)
	picture = models.CharField(max_length=60, null=True)
	code = models.TextField(null=True)
	pub_date = models.DateTimeField('date published')
