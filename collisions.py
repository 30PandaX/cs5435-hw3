import siphash
import datetime

s = 2**16

test = ['17076', '134875', '368425', '406782', '543665', '553314', '705066', '740085', '754095', '841465', '861736', '1011710', '1062521', '1149426', '1255305', '1287787', '1315436', '1329654', '1376308', '1428996', '1544521', '1734559', '1744179', '1806490', '1880423', '1889961', '1905592', '1910789', '1923096', '1926487', '1934351', '2010604', '2019179', '2021647', '2023677', '2200669', '2319584', '2338894', '2467123', '2471912', '2501319', '2718479', '2736240', '2757677', '2901633', '2907587', '3039984', '3094301', '3114610', '3173779']

# ht_hash(key, str(17076).encode("utf-8"), s)

def callhash(hashkey, inval):
    return siphash.SipHash_2_4(hashkey, inval).hash()


def ht_hash(hashkey, inval, htsize):
    return callhash(hashkey, inval) % htsize

#Put your collision-finding code here.
#Your function should output the colliding strings in a list.
def find_collisions(key):
    colls = []
    i = 0
    while (len(colls) < 1000):
        hash_res = ht_hash(key, str(i).encode("utf-8"), s)
        if hash_res == 0:
            colls.append(str(i))
            if len(colls) % 50 == 0:
                print(f"{datetime.datetime.now()}: {len(colls)}")
        i += 1
    return colls

#Implement this function, which takes the list of
#collisions and verifies they all have the same
#SipHash output under the given key.
def check_collisions(key, colls):
    cnt = 0
    for col in colls:
        val = ht_hash(key, col.encode("utf-8"), s)
        if val != 0:
            print("{col} wrong {val}")
            cnt += 1
    print(f"{(len(colls) - cnt)} are right")


if __name__=='__main__':
    #Look in the source code of the app to
    #find the key used for hashing.
    key = b'\x01'*16
    colls = find_collisions(key)
    check_collisions(key, colls)
    with open("./res.txt", "w") as f:
        f.write(str(colls))
