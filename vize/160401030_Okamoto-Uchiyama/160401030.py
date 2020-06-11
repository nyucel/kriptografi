import random
import math
import hashlib



def gcd(a,b):
  while (b):
    a , b = b , a%b
  return a

def fermat(p):
  test = 5
  for i in range(test):
    try:
      a = random.randint(1,p)
    except:
      return 0 
    if pow(a,p-1,p) != 1:
      return 0 
  return 1


def bbs(n): #n bit random sayı üretir
  test = 5
 

  p = random.getrandbits(n//2)
  q = random.getrandbits(n//2)
  while (fermat(p)!=1):
    p = random.getrandbits(n//2)
   
  while (fermat(q)!=1):
    q = random.getrandbits(n//2)
    
  n = p * q 
  seed = random.randint(1,n)
  
  while (gcd(n,seed)!=1):
    seed = random.randint(1,n)
    
  xi = pow(seed,seed,n) 
  for i in range(test):
    xi = xi % n
  return xi
  

def m_r(n):

  s = 0
  d = n-1
  while (1):
    q,r = divmod(d,2)
    if r == 1:
      break
    s+=1
    d = q

  def composite(a):
      if pow(a, d, n) == 1:
        return False
      for i in range(s):
        if pow(a, 2**i * d, n) == n-1:
          return False
      return True 
    
 

  for i in range(5):
    a = random.randrange(2, n)
    if composite(a):
      return False

  return True 

  


def miller_rabin(exp):
  while(1): 
    rand = random.getrandbits(exp)
    if (m_r(rand)==True):
      
      break 
    else:
      rand = random.getrandbits(exp)
  return rand







def keygen(n):
  #tim = time.time()
  p = miller_rabin(n)
  q = miller_rabin(n)
  n = p*p*q
  len_n = len(bin(n))-2
  g = bbs(random.randint(2,len_n//2))
  while (pow(g,p-1,p*p)==1):
    g = bbs(len_n-1)
  h = pow(g,n,n)
  with open("publickey.txt", "w+") as f:
    f.write("{0}\n".format(g))
    f.write("{0}\n".format(n))
    f.write("{0}".format(h))
  
  with open("privatekey.txt", "w+") as f1:
    f1.write("{0}\n".format(p))
    f1.write("{0}\n".format(q))
    f1.write("{0}".format(g))
  
 


def encrypt(plaintext,publickey):
  #n,g,h
  with open(publickey,"r") as f:
    g = int(f.readline())
    n = int(f.readline())
    h = int(f.readline())
  p_text = ""
  with open(plaintext,"r") as f1:
    p_text = f1.readline()

  m = ""
  for i in p_text:
    m += "{0}".format(ord(i)+100)
    
  
  m = int(m)
  
  n_len = len(bin(n))-2
  r = bbs(random.randint(2,n_len))
  c = (pow(g,m,n)*pow(h,r,n))%n
  
  f = open("ciphertext.txt","w+")
  f.write("{0}".format(c))
  f.close()






def L(x, p):
    return (x-1)//p



def decrypt(ciphertext,privatekey):
  #p,q,g
  try:
    with open(privatekey,"r") as f:
      p = int(f.readline())
      q = int(f.readline())
      g = int(f.readline())

   
    
    with open(ciphertext, "r") as f2:
      c = int(f2.readline())

    
    a = pow(c, p-1, p**2)
    b = pow(g, p-1, p**2)
    x = L(a,p)
    y = L(b,p)
    try:
      m = (x * pow(y,-1,p)) % p
    except:
      m = (x*pow(y,p-2,p))%p
    
    m_str = "{0}".format(m)
    m_len = len(m_str) //3
    str_ = ""
    str_int = 0

    for i in range(0,m_len):
      str_int = int(m_str[i*3:(i*3)+3])
      str_int = str_int - 100
      
      str_ = str_ + chr(str_int)
    
    with open("plaintext2.txt","w+") as f3:
      f3.write(str_)

    BUF_SIZE = 65536  

   
    sha1 = hashlib.sha1()
    sha1_ = hashlib.sha1()

    with open("plaintext.txt", 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            
            sha1.update(data)
   
    _sha1 = "{0}".format(sha1.hexdigest())
    
    with open("plaintext2.txt", 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
           
            sha1_.update(data)
    
    
    __sha1 = "{0}".format(sha1.hexdigest())

    if (__sha1 in _sha1):
      print("Dosyalar Aynı!")
    
      
  except:
    print("Dosyalar Farklı")



  


keygen(512)
encrypt("plaintext.txt","publickey.txt")
decrypt("ciphertext.txt", "privatekey.txt")
