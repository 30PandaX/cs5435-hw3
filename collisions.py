import siphash
import datetime

s = 2**16
key = b'\x01'*16


def callhash(hashkey, inval):
    return siphash.SipHash_2_4(hashkey, inval).hash()

def ht_hash(hashkey, inval, htsize):
    return callhash(hashkey, inval) % htsize

#Put your collision-finding code here.
#Your function should output the colliding strings in a list.
def find_collisions(key, num_collisions):
    hash_map = {}
    i = 0 # used for construct random string
    max_bucket_len = 0
    res_bucket_id = 0
    # used for filter out unpromising candidates in a progressive way, cur_length < max_bucket_len - thresh[i]; 
    thresh = [32, 128, 64, 128, 64, 128, 64] # [16, 32, 64, 128, 64, 128, 64, 128, 64] # [16, 32, 128, 64, 32]
    # used for which threshold should we use for now
    idx = 0 
    print(f"{datetime.datetime.now()}: {max_bucket_len}, dict size: {len(hash_map)}")
    
    # when we find one bucket that has length == num_collisions, break loop
    
    while max_bucket_len < num_collisions:
        bucket_id = ht_hash(key, str(i).encode("utf-8"), s)
        if max_bucket_len < 8: # why use this hardcode 8? bc when maxCol==8, d would increase to 38243
            if bucket_id not in hash_map:
                hash_map[bucket_id] = []
            hash_map[bucket_id].append(str(i))
            # update max_bucket_len
            if len(hash_map[bucket_id]) > max_bucket_len:
                max_bucket_len = len(hash_map[bucket_id])
                res_bucket_id = bucket_id
        else:
            if bucket_id in hash_map:
                if max_bucket_len - thresh[idx] < len(hash_map[bucket_id]):
                    hash_map[bucket_id].append(str(i))
                    # update max_bucket_len
                    if len(hash_map[bucket_id]) > max_bucket_len:
                        max_bucket_len = len(hash_map[bucket_id])
                        res_bucket_id = bucket_id 
                        # track progress, only for debugging purpose 
                        # In fact, during this process, the number of candidates in the hash_map will be smaller and smaller             
                        if max_bucket_len % 50 == 0:
                            idx = min(idx + 1, len(thresh) - 1)
                            print(f"{datetime.datetime.now()}: {max_bucket_len}, dict size: {len(hash_map)}")
                else:
                    # abandon those unpromising candidates to save memory
                    hash_map.pop(bucket_id)

        i += 1
    check_collisions(key, hash_map[res_bucket_id])
    return hash_map[res_bucket_id]

#Implement this function, which takes the list of
#collisions and verifies they all have the same
#SipHash output under the given key.
def check_collisions(key, colls):
    cnt = 0
    ans = ht_hash(key, colls[0].encode("utf-8"), s)
    for col in colls:
        val = ht_hash(key, col.encode("utf-8"), s)
        if val != ans:
            print(f"{col} is wrong, its hash: {val} != {ans}")
            cnt += 1
    print(f"{(len(colls) - cnt)} are right")


if __name__=='__main__':
    #Look in the source code of the app to
    #find the key used for hashing.
    # key is defined at the beginning of this file
    colls = find_collisions(key, 1000)
    with open("./res.txt", "w") as f:
        f.write(str(colls))
