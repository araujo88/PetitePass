import hashlib

# print(hashlib.algorithms_available)
# print(hashlib.algorithms_guaranteed)

string = "hello world"

digest_md5 = hashlib.md5(string.encode()).hexdigest()
digest_sha224 = hashlib.sha224(string.encode()).hexdigest()
digest_sha256 = hashlib.sha256(string.encode()).hexdigest()
digest_sha386 = hashlib.sha384(string.encode()).hexdigest()
digest_sha512 = hashlib.sha512(string.encode()).hexdigest()

print(f"MD5: {digest_md5}")
print(f"SHA-224: {digest_sha224}")
print(f"SHA-256: {digest_sha256}")
print(f"SHA-386: {digest_sha386}")
print(f"SHA-512: {digest_sha512}")
