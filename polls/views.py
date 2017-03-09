from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View

class Polls(View):
    def get(self, request):
    	return render(request, 'polls.html', {})