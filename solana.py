import os
import base58
import ed25519

def createPrivateKey():
    keypair_seed = os.urandom(32)
    keypair_private = ed25519.SigningKey(keypair_seed)
    keypair_public = keypair_private.get_verifying_key().to_bytes()
    public_key = base58.b58encode(keypair_public).decode()
    private_key = base58.b58encode(keypair_private.to_bytes()).decode()
    return public_key+'|'+private_key

def signMessage(private_key,message) -> str:
    private_keyObj = ed25519.SigningKey(base58.b58decode(private_key))
    if type(message) == str:
        message = message.encode()    
    signature = private_keyObj.sign(message)
    return signature.hex()


count = int(input('nhập số lượng : '))
for i in range(count):
    wallet = createPrivateKey()
    print(wallet)
    with open('wallet_sol.txt', 'a+') as save:
        save.write(wallet+'\n')
