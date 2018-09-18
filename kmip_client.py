import ssl
from kmip.pie.client import ProxyKmipClient
from kmip import enums
from base64 import b64encode
from binascii import hexlify
from client_config import client


# Generate a symmetric key
with client:
  key_id = client.create(
            enums.CryptographicAlgorithm.AES,
            256,
            operation_policy_name = 'default',
            name = 'AES256_symm_key_001',
        )

# Before using the key we need to activate it
with client:
  client.activate(uid=key_id)
  
# Some info about that key
with client:
   sk = client.get(uid=key_id)
   print('Info about key ID {0}:'.format(key_id))
   print('Algorithm:      {0}'.format(sk.cryptographic_algorithm))
   print('Length:         {0}'.format(sk.cryptographic_length))
   print('Initial date:   {0}'.format(sk.initial_date))
   print('Object type:    {0}'.format(sk.object_type))
   # With PyKMIP 0.8.0, state still shows PRE_ACTIVE even after activating
   print('Key state:      {0}'.format(sk.state))
   print('Value type:     {0}'.format(type(sk.value)))
   print('Value (base64): {0}'.format(b64encode(sk.value)))
   print('Value (hex):    {0}'.format(hexlify(sk.value)))
   print('{:*^80}'.format(''))


# Encrypt a string - KMIP server will generate an IV if we don't want to provide one
cleartext = b'Hello world'
iv_hex = 'bf65f66454b521191fdf30c6b53ffd00'
iv = bytes(bytearray.fromhex(iv_hex))

with client:
    cr = client.encrypt(cleartext, uid=key_id,
                                cryptographic_parameters={'cryptographic_algorithm':enums.CryptographicAlgorithm.AES,
                                'block_cipher_mode': enums.BlockCipherMode.CBC,
                                'padding_method': enums.PaddingMethod.PKCS5}
                                #, iv_counter_nonce = iv
                       )

ciphertext = cr[0]
noncense = cr[1]

if noncense == None:
    # the IV bytes part of the response will be None if we specified an IV of our own
    noncense = iv

print('Ciphertext: {0}'.format(hexlify(ciphertext)))
print('IV:         {0}'.format(hexlify(noncense)))


