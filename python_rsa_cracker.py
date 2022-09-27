from Crypto.PublicKey import RSA
import requests

###The cryptodome library is really doing some heavy lifting here

pub_file = input("Filename of public key: ")
with open(pub_file) as temp:
    pub_key = temp.read()
pub = RSA.importKey(pub_key)
n = int(pub.n)
e = int(pub.e)
factors = requests.get("http://factordb.com/api", params={"query": str(n)}).json()
y=0
for x in range(1, len(factors["factors"])):
    q=int(factors["factors"][y][0])
    p=int(factors["factors"][x][0])
    if q * p == n:
        break
    if q * p != n and x == ((len(factors["factors"])) - 1):
        y+=1
        x=y+1

phi_of_n = ((p-1)*(q-1))

###The encryption exponent d is the multiplicative inverse of emod(phi(n)) so we can use the extended euclidean algorithm to find the value of d and the compile the private key
###Other libraries already have this algorithm available as a pre-baked method but I wanted to understand mathematically what was going on under the hood so I taught myself some basics of the EEA and then codified it programmatically here.
a = phi_of_n
b = e
t1 = 0
t2 = 1
while b > 0:
    q = a // b
    r = a % b
    t = t1 - t2 * q
    t1 = t2
    t2 = t
    a = b
    b = r
###I'm planning on rewriting this program so that it will compile the private key from scratch rather than use the cryptodome library. I want to understand RSA more

private_key = RSA.construct((n,e,t1))

print(private_key.export_key().decode())
