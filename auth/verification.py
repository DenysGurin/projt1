import os
import re
import time
import random
import string
import hashlib
import hmac
import json
import datetime
import urllib2
from xml.dom import minidom
from google.appengine.ext import db



temp = os.path.join(os.path.dirname(__file__), "templates")
jin_env = jinja2.Environment(loader=jinja2.FileSystemLoader(temp), autoescape=True)

#verify_page =  open("verify_page.html", "r").read()
#welcome_page = open("welcome_page.html", "r").read()

USERNAME_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

USERNAME_ERROR = "That's not a valid username."
PASSWORD_ERROR = "That wasn't a valid password."
V_PASSWORD_ERROR = "Your passwords didn't match."
EMAIL_ERROR = "That's not a valid email."
EXISTS_ERROR = "That user already exists"
LOGIN_ERROR = "Invalid login"


def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)
    
#####################
#####DATABASE########
#####################  
  
class Story(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)
    author = db.StringProperty(required=True)
    coords = db.GeoPtProperty()
    gmaps_img = db.StringProperty()
    
class User(db.Model):
    username = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)


###################
####HASHING#######
###################

class Protection(object):
    
    SECRET = 'imsosecret'
    @staticmethod
    def hash_str(s, secret = SECRET):
        return hmac.new(secret, s).hexdigest()
    @staticmethod
    def make_secure_val(s):
        return "%s|%s" % (s, Protection.hash_str(s))
    @staticmethod
    def check_secure_val(h):
        val = h.split('|')[0]
        if h == Protection.make_secure_val(val):
            return val
    @staticmethod
    def make_salt():
        return ''.join(random.choice(string.letters) for x in xrange(5))
    @staticmethod
    def make_pw_hash(name, pw, salt=None):
        if not salt:
            salt = Protection.make_salt()
        h = hashlib.sha256(name + pw + salt).hexdigest()
        return '%s,%s' % (h, salt)
    @staticmethod
    def valid_pw(name, pw, h):
        hashed, salt = h.split(',')
        return hashlib.sha256(name + pw + salt).hexdigest() == hashed

########################
#####BASE_HANDLER#######
#######################

class Handler(webapp2.RequestHandler):
    
    def write(self, *ar, **kw):
        self.response.out.write(*ar, **kw)
        
    def render_str(self,temp, **pars):
        t = jin_env.get_template(temp)
        return t.render(**pars)
        
    def render(self, temp, **kwars):
        self.write(self.render_str(temp, **kwars))
        
    def req_get(self, name):
        return self.request.get(name)
        
    def remove_data(self, db_name):
        db_data = db.GqlQuery("SELECT * FROM %s" % db_name)
        for data in db_data:
            data.delete()
            
    def add_cookie(self, name, val):
        self.response.headers.add_header("Set-Cookie", '%s=%s; Path=/'%(name, val))
        
    def get_cookie(self, name):
        return self.request.cookies.get("%s"%name, "")
       
    def exists(self, name, parameter, db_name):
        return name in [getattr(user, parameter) for user in db.GqlQuery("SELECT * FROM %s" % db_name)]
        
class GeoLoc(object):
    
    def gmaps_img(self, points):
        image_url = GMAPS_URL
        for point in points:
            image_url+="markers={0},{1}&".format(point.lat, point.lon)
        return image_url[:-1]    
          
    def get_coords(self, ip):
        #ip = "173.18.89.13"
        url = IP_URL + ip
        try:
            content = urllib2.urlopen(url).read()
        except urllib2.URLError:
            return 
        if content:
            parse = minidom.parseString(content)
            lon = parse.getElementsByTagName("lon")
            lat = parse.getElementsByTagName("lat")
            if lat and lon:
                lon = lon[0].childNodes[0].nodeValue
                lat = lat[0].childNodes[0].nodeValue
                return db.GeoPt(lat, lon)

    #def get(self):
    #    self.response.out.write("2123")#self.get_coords(self.request.remote_addr))
                
      
####################
#####PAGES#########
###################             
                                                                         
class VerifyPage(Handler):
    
    def chek_username(self, username):
        return username and USERNAME_RE.match(username)
        
    def chek_password(self, password):
        return password and PASSWORD_RE.match(password)
    
    def chek_email(self, email):
        return not email or EMAIL_RE.match(email)
                                 
    def get(self):
        #self.remove_data()
        self.render("verify_page.html")
        self.get_cookie("username")
    
    def post(self):
        
        verifyed = False
        username = self.req_get("username")
        password = self.req_get("password")
        verify = self.req_get("verify")
        email = self.req_get("email")
        kwargs = {"username":username,
                    "email":email}
        
        if self.exists(username, "username", "User"):
            verifyed = True
            kwargs["un_error"] = EXISTS_ERROR
        elif not self.chek_username(username):
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
            self.render("verify_page.html", **kwargs)
        else:
            user_instance = User(username=username, password=Protection.make_pw_hash(username, password), email=email)
            user_instance.put()
            self.add_cookie("username", Protection.make_secure_val(str(username)))
            self.redirect("/blog")
                                
class WelcomePage(Handler):
    
    def get(self):
        #username = Protection.check_secure_val(self.get_cookie("username"))
        #if username:
        self.render("welcome_page.html")
        #    #time.sleep(1)
        #    self.redirect("/blog")
        #else:
        #    self.redirect("/singin")
            
class LoginPage(Handler):
    
    def get(self):
        self.render("login_page.html")
        self.get_cookie("username")
    def post(self):
        username = self.req_get("username")
        password = self.req_get("password")
        kwargs = {}
        ###first method
        #user_db = User.gql("WHERE username = '%s'" % username)
        #self.response.out.write(user_db.get().username)
        
        ###second method
        #user_db = User.all()#.
        #self.response.out.write(user_db.filter("username =", username).get().username)
        user_db = User.gql("WHERE username = '%s'" % username).get()
        if user_db and Protection.valid_pw(username, password, user_db.password):
            self.add_cookie("username", Protection.make_secure_val(str(username)))
            self.redirect("/blog")
        else:
            kwargs["login_er"] = LOGIN_ERROR
            self.render("login_page.html", **kwargs)
            
class LogoutPage(Handler):
    
    def get(self):
        if  self.get_cookie("username"):
            self.add_cookie("username", "")
        self.redirect("/singin")
        
        
class BlogMainP(Handler, GeoLoc):
    def render_front(self):
        #time.sleep(0.1)
        storage = db.GqlQuery("SELECT * FROM Story ORDER BY created DESC")
        storage = list(storage)
        points = filter(None, [p.coords for p in storage])
        img_url = None
        if points:
            img_url = self.gmaps_img(points)
            
        self.render("blog_main.html", storage=storage, img_url=img_url)
        
    def get(self):
        #self.remove_data()
        username = Protection.check_secure_val(self.get_cookie("username"))
        if username:
            self.render_front()
        else:
            self.redirect("/login")
            
    def post(self):
        new_post_button = self.req_get("new_post_button")
        if new_post_button:
            self.redirect("/blog/newpost")
            
class NewPostP(Handler, GeoLoc):
    
    def get(self):
        username = Protection.check_secure_val(self.get_cookie("username"))
        if username:
            self.render("new_post.html", subject="", content="", error="")
        else:
            self.redirect("/login")
            
    def post(self):
        subject = self.req_get("subject")
        content = self.req_get("content")
        author = Protection.check_secure_val(self.get_cookie("username"))
        
        if subject and content:
            story = Story(subject=subject, content=content, author=author)
            coords = self.get_coords(self.request.remote_addr)
            if coords:
                story.coords = coords
                story.gmaps_img = self.gmaps_img([coords])
            story.put()
            self.redirect('/blog/%s'%str(story.key().id()))
        else:
            error = "fill in both field"
            self.render("new_post.html", subject=subject, content=content, author=author, error=error)
        
class PostP(Handler,GeoLoc):
    def get(self, post_id):
        key = db.Key.from_path("Story", int(post_id))
        post = db.get(key)
        points = []
        
        if post.coords:
            points.append(post.coords)
        img_url = None
        if points:
            img_url = self.gmaps_img(points)
        self.render("post_page.html", post=post, img_url=img_url)
        #self.response.out.write(key)
        #self.response.out.write(post)
        
    def post(self, post_id):
        main_page_button = self.req_get("main_page_button")
        if main_page_button:
            self.redirect("/blog")
                        
class DBPage(Handler):
    
    def get(self):
        for cursore in DBQuery.get_entitys(User):
            self.write("%s<br>"%cursore)

################
###JSON_API##### 
################
class DBQuery(object):
    
    @staticmethod
    def get_entitys(DBType):
        return [cursore._entity for cursore in DBType.all()]
    
    @staticmethod
    def get_by_key(DBType, item_name):
        
        key = db.Key.from_path(DBType.__name__, int(item_name))
        post = db.get(key)
        return post._entity
        
        
class BlogMainJson(Handler):
    
    def get(self):
        entitys = DBQuery.get_entitys(Story)
        for entity in entitys:
            for key in entity.keys():
                if type(entity[key]) == datetime.datetime:
                    entity[key] = entity[key].ctime()
        json_format = json.dumps(entitys)
        self.write(json_format)
             
class PostJson(Handler):
    
    def get(self, post_id):
        cursor = DBQuery.get_by_key(Story, post_id)
        for key in cursor.keys():
            if type(cursor[key]) == datetime.datetime:
                cursor[key] = cursor[key].ctime()
        json_format = json.dumps(cursor)
        self.write(json_format)
        
class Debug(Handler, GeoLoc):
    
    def get(self):
        
        post = Story.all().order("-created").get()
        self.write(post.coords)
        self.write(self.get_coords(""))
        post.gmaps_img = self.gmaps_img([post.coords])
        self.write(post.gmaps_img)
        """
        if post.coords:
            points.append(post.coords)
        img_url = None
        if points:
            img_url = self.gmaps_img(post.coords)
        self.render("post_page.html", post=post, img_url=img_url)
        """                        
app = webapp2.WSGIApplication([('/singin', VerifyPage), 
                                ('/', WelcomePage), 
                                ("/login", LoginPage), 
                                ("/logout", LogoutPage), 
                                ("/database", DBPage), 
                                ('/blog', BlogMainP),
                                ("/blog/newpost", NewPostP),
                                ("/blog/([0-9]+)", PostP),
                                ('/blog.json', BlogMainJson),
                                ("/blog/([0-9]+).json", PostJson),
                                ("/debug", Debug)], debug = True)
        