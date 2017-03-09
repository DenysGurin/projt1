from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import View
from . import verification, protection


class Welcome(View):
    def get(self, request):
	    return render(request, 'welcome.html', {})
    def post(self, request):
        a = False
        verifyed = False
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')
        email = request.POST.get('email')
        kwargs = {'username': username,
                    'email': email}
        # if self.exists(username, "username", "User"):
        #    verifyed = True
        #    kwargs["un_error"] = EXISTS_ERROR
        if not verification.chek_username(username):
            verifyed = True
            kwargs['n_error'] = verification.USERNAME_ERROR

        if not verification.chek_password(password):
            verifyed = True
            kwargs['p_error'] = verification.PASSWORD_ERROR
        elif password != confirm:
            verifyed = True
            kwargs['vp_error'] = verification.V_PASSWORD_ERROR

        if not verification.chek_email(email):
            verifyed = True
            kwargs['e_error'] = verification.EMAIL_ERROR 
        
        if verifyed:
            return render(request, 'welcome.html', kwargs)
        else:
            # user_instance = User(username=username, password=Protection.make_pw_hash(username, password), email=email)
            # user_instance.put()
            # self.add_cookie("username", Protection.make_secure_val(str(username)))
            return redirect('/polls')
# class Singin(View):
# 	def get(self, request):
# 		return render(request, 'singin.html', {})
# 	def post(self, request):
# 		verifyed = False	
# 		username = request.POST.get('username')
# 		password = request.POST.get('password')
# 		verify = request.POST.get('verify')
# 		email = request.POST.get('email')
# 		kwargs = {'username': username,
# 		            'email': email}
# 		# if self.exists(username, "username", "User"):
# 		#    verifyed = True
# 		#    kwargs["un_error"] = EXISTS_ERROR
# 		if not verification.chek_username(username):
# 		    verifyed = True
# 		    kwargs['n_error'] = verification.USERNAME_ERROR

# 		if not verification.chek_password(password):
# 		    verifyed = True
# 		    kwargs['p_error'] = verification.PASSWORD_ERROR
# 		elif password != verify:
# 		    verifyed = True
# 		    kwargs['vp_error'] = verification.V_PASSWORD_ERROR

# 		if not verification.chek_email(email):
# 		    verifyed = True
# 		    kwargs['e_error'] = verification.EMAIL_ERROR 
		    

# 		if verifyed:
# 		    return render(request, 'singin.html', kwargs)
# 		else:
# 		    # user_instance = User(username=username, password=Protection.make_pw_hash(username, password), email=email)
# 		    # user_instance.put()
# 		    # self.add_cookie("username", Protection.make_secure_val(str(username)))
# 		    return redirect('/main')

# class Login(View):
# 	def get(self, request):
# 		return render(request, 'login.html', {})
# 		