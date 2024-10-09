def prime_checker(p):
    if p < 2:
        return -1
    if p == 2:
        return 1
    for i in range(2, int(p**0.5) + 1):
        if p % i == 0:
            return -1
    return 1

def primitive_check(g, p, L):
    L.clear()  
    for i in range(1, p):
        L.append(pow(g, i, p))
    for i in range(1, p):
        if L.count(i) > 1:
            return -1
    return 1

l = []
while True:
    p = int(input("Enter p: "))
    if prime_checker(p) == -1:
        print("Number is not prime, please enter again!")
        continue
    break

while True:
    G = int(input(f"Enter the primitive root of {p}: "))
    if primitive_check(G, p, l) == -1:
        print(f"Number is not a primitive root of {p}, please try again!")
        continue
    break

while True:
    x1 = int(input("Enter the private key of user 1: "))
    x2 = int(input("Enter the private key of user 2: "))
    if x1 >= p or x2 >= p:  
        print(f"Private key for both users should be less than {p}!")
        continue
    break

y1, y2 = pow(G, x1, p), pow(G, x2, p)
k1, k2 = pow(y2, x1, p), pow(y1, x2, p)

print(f"\nSecret key for user 1 is {k1}\nSecret key for user 2 is {k2}\n")
if k1 == k2:
    print("Keys have been exchanged successfully.")
else:
    print("Keys have not been exchanged successfully.")
