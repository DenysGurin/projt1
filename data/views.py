from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import View

class Data(View):
	def get(self, request):
		return HttpResponse("data")
	    #return render(request, 'data.html', {})
    