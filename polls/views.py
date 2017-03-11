from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required



class Polls(View):

	# @login_required()
    def get(self, request):
    	if request.user.is_authenticated():
    		return render(request, 'polls.html', {})
    	else:
    		return redirect('/')