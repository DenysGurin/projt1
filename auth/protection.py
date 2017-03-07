import re
import random
import string
import hashlib
import hmac


USERNAME_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

USERNAME_ERROR = "That's not a valid username."
PASSWORD_ERROR = "That wasn't a valid password."
V_PASSWORD_ERROR = "Your passwords didn't match."
EMAIL_ERROR = "That's not a valid email."
EXISTS_ERROR = "That user already exists"
LOGIN_ERROR = "Invalid login"

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

    @staticmethod
    def chek_username(self, username):
        return username and USERNAME_RE.match(username)

    @staticmethod   
    def chek_password(self, password):
        return password and PASSWORD_RE.match(password)
        
    @staticmethod
    def chek_email(self, email):
        return not email or EMAIL_RE.match(email)
                                 