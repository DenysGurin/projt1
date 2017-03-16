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
    def post(self, request):
    	if request.POST.get('test'):
	    	if request.user.is_authenticated():
	    		# polls = Poll.objects
	    		# context = {"polls" : polls}
	    		return redirect('test/%s' % request.POST.get('test'), poll_id = request.POST.get('test'))
	    	else:
    			return redirect('/')

    	#return HttpResponse(polls)

class Test(View):

	# @login_required()
    def get(self, request, poll_id):
    	if request.user.is_authenticated():
    		test = Poll.objects.get(id=poll_id)
    		context = {"test" : test}
    		return render(request, 'test.html', context)
    		# return HttpResponse(Poll.objects.get(id=poll_id))
    	else:
    		return redirect('/')
    