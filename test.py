import hashlib
print("Choose hash option: MD5 (1), SHA1 (2)")
with open('inp', 'rb') as file:
f = file.read()
print((hashlib.md5(f)
if
hashlib.sha1(f)).hexdigest())