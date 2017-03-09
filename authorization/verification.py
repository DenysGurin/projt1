import re


USERNAME_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

USERNAME_ERROR = "That's not a valid username."
PASSWORD_ERROR = "That wasn't a valid password."
V_PASSWORD_ERROR = "Your passwords didn't match."
EMAIL_ERROR = "That's not a valid email."
EXISTS_ERROR = "That user already exists"
LOGIN_ERROR = "Invalid login"


def chek_username(username):
    return username and USERNAME_RE.match(username)
    
def chek_password(password):
    return password and PASSWORD_RE.match(password)

def chek_email(email):
    return not email or EMAIL_RE.match(email)
                                 
# if not chek_username('111'):
# 	print "ne"
# if not chek_password('111'):
# 	print 'pa'
# elif '111' != '111':
# 	print 'con'

# if not chek_email(''):
# 	print 'em'
# if USERNAME_RE.match('11'):
# 	print "re"