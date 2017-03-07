from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import View
from . import verification, protection


class Welcome(View):
    def get(self, request):
	    return render(request, 'welcome.html', {})

class Singin(View):
	def get(self, request):
		return render(request, 'singin.html', {})
	def post(self, request):
		verifyed = False
		username = request.GET["username"]
		password = request.GET["password"]
		verify = request.GET["verify"]
		email = request.GET["email"]
		kwargs = {"username":username,
		            "email":email}

		#if self.exists(username, "username", "User"):
		#    verifyed = True
		#    kwargs["un_error"] = EXISTS_ERROR
		if not verification.chek_username(username):
		    verifyed = True
		    kwargs["un_error"] = USERNAME_ERROR

		if not self.chek_password(password):
		    verifyed = True
		    kwargs["p_error"] = PASSWORD_ERROR
		elif password != verify:
		    verifyed = True
		    kwargs["vp_error"] = V_PASSWORD_ERROR

		if not self.chek_email(email):
		    verifyed = True
		    kwargs["e_error"] = EMAIL_ERROR 
		    

		if verifyed:
		    self.render(request, "singin.html", **kwargs)
		else:
		    user_instance = User(username=username, password=Protection.make_pw_hash(username, password), email=email)
		    user_instance.put()
		    self.add_cookie("username", Protection.make_secure_val(str(username)))
		    self.redirect("/main")

class Login(View):
	def get(self, request):
		return render(request, 'login.html', {})
		