from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Poll


class Polls(View):

	# @login_required()
    def get(self, request):
    	if request.user.is_authenticated():
    		polls = Poll.objects
    		context = {"polls" : polls}
    		return render(request, 'polls.html', context)
    		# return HttpResponse([poll for poll in polls.all()])
    	else:
    		return redirect('/')
    def post():
    	polls = Poll.objects[:8]
    	context = {"polls" : polls}
    	return render(request, "polls", context)
    	#return HttpResponse(polls)