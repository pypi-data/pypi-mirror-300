# Overview
The implementation of secure random generator based on SHA256.
# Build
```
python setup.py sdist bdist_wheel
pip install dist/sha256sr*.whl
```
# Use Guide
```
sk_seed = "y5adsgpfojktyg90gerwyhrbdsyh4ou2"
encryptor = AdcpeEncryptor(sk_seed=sk_seed)
plain = [1 for _ in range(100)]
cipher = encryptor.encrypt(plain)
decryptor = AdcpeDecryptor(sk_seed=sk_seed)
dec_plain = decryptor.decrypt(cipher_de)
```