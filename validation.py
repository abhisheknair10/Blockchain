

def leading_zeros(block_hash):
    if(list(block_hash)[0] == "0" and list(block_hash)[1] == "0" and 
        list(block_hash)[2] == "0" and list(block_hash)[3] == "0" and list(block_hash)[4] == "0"):
        return True
    return False