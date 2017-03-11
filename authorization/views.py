from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import View

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

#from .models import AuthUser
from . import verification, protection


class Welcome(View):
    def get(self, request):
	    return render(request, 'welcome.html', {})
    def post(self, request):
        if request.POST.get('submit') == 'registration':
            verifyed = False
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm = request.POST.get('confirm')
            email = request.POST.get('email')
            kwargs = {'username': username,
                        'email': email}

            if username in [user.username for user in User.objects.all()]:#User.objects.get(username=username).username:
               verifyed = True
               kwargs["un_error"] = verification.EXISTS_ERROR
            elif not verification.chek_username(username):
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
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                # user_instance = User(username=username, password=Protection.make_pw_hash(username, password), email=email)
                # user_instance.put()
                # self.add_cookie("username", Protection.make_secure_val(str(username)))
                return redirect('/polls')

        elif request.POST.get('submit') == 'login':
    
            username = request.POST.get('username')
            password = request.POST.get('password')
            kwargs = {}
            ###first method
            #user_db = User.gql("WHERE username = '%s'" % username)
            #self.response.out.write(user_db.get().username)
            
            ###second method
            #user_db = User.all()#.
            #self.response.out.write(user_db.filter("username =", username).get().username)
            # user_db = User.gql("WHERE username = '%s'" % username).get()
            # if user_db and protection.valid_pw(username, password, user_db.password):
            #     self.add_cookie("username", Protection.make_secure_val(str(username)))
            #     return render(request, 'welcome.html', kwargs)

            # if username in [user.username for user in User.objects.all()]:
            #     return redirect('/polls')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/polls')
            else:
                kwargs["login_er"] = verification.LOGIN_ERROR
                return render(request, 'welcome.html', {})

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/')

class Print(View):
    def get(self, request):
        return HttpResponse([user.username for user in User.objects.all()])

class Login(View):
    def get(self, request):
        return render(request, 'login.html', {})
    def post(self, request):
        return HttpResponse(request.POST)
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