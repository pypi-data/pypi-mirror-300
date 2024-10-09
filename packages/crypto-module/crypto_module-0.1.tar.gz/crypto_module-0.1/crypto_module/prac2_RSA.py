import math

# Initialize p and q
p = 3
q = 7

# Compute n
n = p * q
print("n =", n)

# Compute φ(n)
phi = (p - 1) * (q - 1)

# Find an appropriate e
e = 2
while e < phi:
    if math.gcd(e, phi) == 1:
        break
    e += 1
print("e =", e)

# Compute d
k = 2
d = ((k * phi) + 1) / e
print("d =", d)

# Display public and private keys
print("Public Key:", e, n)
print("Private Key:", int(d), n)

# Encrypt a message
msg = 11
C = pow(msg, e, n)
print("original msg:", msg)
print("encrypted msg:", C)

# Decrypt the message
M = pow(C, int(d), n)
print("decrypted msg:", M)
