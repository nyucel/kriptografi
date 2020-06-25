import random

from datetime import datetime

time1 = float(datetime.now().minute)


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
  p = random.getrandbits(n//2)
  q = random.getrandbits(n//2)
  while (1):
    p = random.getrandbits(n//2+1)
    if (fermat(p)==1) and (len(bin(p)[2:])==(n//2+1)):
      break
  while (1):
    q = random.getrandbits(n//2)
    if (fermat(q)==1) and (len(bin(q)[2:])==(n//2)):
      break
      
  n1 = p * q 
  if (len(bin(n1)[2:])==(n-1)):
    n1 = n1<<1
  
  seed = random.randint(1,n1)
  
  xi = 0
  while(len(bin(xi)[2:])!=n):
    xi = pow(seed,seed,n1) 
    seed = random.randint(1,n1)
    while (gcd(n,seed)!=1):
      seed = random.randint(1,n+1)
    
  return xi



def final(str):
  checksum = 0
  a = 1
  b = 0
  c_mod = (2**16)-1
  with open(str,'rb') as f:
    data = f.read()
    for i in range(0,len(data)):
      a = (a+data[i])*a % c_mod
      b = (b+a) % c_mod
  
  checksum =2**((a+b) % 32) ^ (b<<16) | a ^ 2**((a*b)% 32)
  if len(bin(checksum)[2:]) < 32:
    return checksum << (32-len(bin(checksum)[2:]))
  return checksum


#print(final("001.txt"))

h_sum = open('HASHSUM.txt','w') 
liste =[]
for i in range(2,101):
  time2=float(datetime.now().minute)
  if (time2-time1 < 10):  
    file_no = (3-len("{0}".format(i)))*'0' + "{0}".format(i) + '.txt'
    first_file = (3-len("{0}".format(i-1)))*'0' + "{0}".format(i-1) + '.txt'
    f_c = final(first_file)
    rand = bbs(32)
    
    checksum_ = ((rand | f_c) ^ (rand^f_c)) >>8
    h_sum.writelines("{0}. blok için üretilen rastgele değer:{1}\t\t{0}. bloğun özeti:00000000{2}\n".format(i,bin(rand)[2:],bin(checksum_)[2:]))
    
    with open(file_no,'w+') as f1:
      f1.write("{0}".format(hex(checksum_)))
    #with open('HASHSUM.txt','w+') as h_sum:
  else:
    break
h_sum.close()


