import hashlib

#
def double_sha256(arg):
    return hashlib.sha256(hashlib.sha256(arg.encode()).hexdigest().encode()).hexdigest()

#
"""
def tx_encrypt(txlist):
    txlist_hashed = []
    for i in range(len(txlist)):
        txlist_hashed.append(double_sha256(txlist[i]))
    return txlist_hashed
"""

#
def findMerkleRoot(txlist):
    while(len(txlist) != 1):
        txlen = len(txlist)
        txlist = layerXMerkle(txlist, txlen)
    return txlist[0]

#
def layerXMerkle(txlist, txlen):
    inter_list = []
    for i in range(0, txlen, 2):
        if(txlen%2 == 0):
            inter_list.append(double_sha256(txlist[i] + txlist[i+1]))
        else:
            if(i == txlen-1):
                inter_list.append(double_sha256(txlist[i] + txlist[i]))
            else:
                inter_list.append(double_sha256(txlist[i] + txlist[i+1]))
    return inter_list