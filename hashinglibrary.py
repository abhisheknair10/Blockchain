import hashlib
from typing import *

class HashingLibrary:
    
    def doubleSHA256(arg: bytes) -> str:
        return hashlib.sha256(
            hashlib.sha256(
                arg
            ).hexdigest().encode()
        ).hexdigest()