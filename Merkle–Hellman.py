import random
import secrets
import math
import functions
import sympy
import os

# Ahmet Orbay 100401053
# Merkle Hellman

def keygen(n):
  w=[];wtotal=0;rcontrol=0;controlPrime=0
  y=secrets.randbits(32)
  w.append(y)
  while len(w)!=8:
    total=0
    total=sum(w)
    w.append(total+1)
  wtotal=sum(w)
  while controlPrime==0:
    qNumber= random.randint(wtotal,wtotal+1000)
    primeNumber=functions.isprime(qNumber)
    if(primeNumber==0):
      controlPrime=0
    else:
      controlPrime=1
  while rcontrol==0:
    rNumber= random.randint(1,1000)
    gcd_q_r=math.gcd(qNumber,rNumber)
    if(gcd_q_r==1):
      rcontrol=1
    else:
      rcontrol=0
  BArray=[]
  for i in w:
    b=(rNumber*i)%qNumber
    BArray.append(b)
  with open("publickey.txt","w") as public:
    for i in BArray:
      public.write(str(i)+" ")
  private_key=(w,qNumber,rNumber)
  with open("privatekey.txt","w") as private:
    for i in w:
      private.write(str(i)+" ")
    private.write("-"+str(qNumber))
    private.write("-"+str(rNumber))


def encrypt(plaintext, publickeytxt):
  if(os.path.isfile(publickeytxt)!=False):
      BArray=[]
      public=open(publickeytxt,"r")
      publicRead=public.read()
      for i in publicRead.split(" "):
        BArray.append(i)
      plain=open(plaintext)
      plainRead=plain.read()
      chipper=open("ciphertext.txt","w")
      chipper.write("")
      chipper.close()
      for letter in plainRead:
        encryptedText=0
        ors=(ord(letter))
        l=bin(ors).replace("0b","")
        if(len(l)<7):
          l="0"+l
        for i in range(len(l)):
          encryptedText=encryptedText+(int(l[i])*int(BArray[i]))
        chipper=open("ciphertext.txt","a")
        chipper.write(" "+str(encryptedText))
        chipper.close()
      plain.close()
      public.close()
  else:
    print("key files could not be found. Please run the keygen function!")

def decrypt(ciphertext, privatekeytxt):
  if(os.path.isfile(privatekeytxt)!=False):

      outputText="";w=[];wCopy=[]
      chipper=open(ciphertext,"r")
      encryptedTextRead=chipper.read()
      encryptedTexts=encryptedTextRead.split(" ")
      privates=open(privatekeytxt,"r")
      private=privates.read()
      result=private.split('-')
      wRead=result[0]
      wSplit=wRead.split(" ")
      for c in wSplit:
        if(c==""):
          break
        w.append(int(c))
        wCopy.append(int(c))
      qNumber=int(result[1])
      rNumber=int(result[2])
      for encryptedText in encryptedTexts:
        arrayBits=[];w=[];count=0
        w=w+wCopy
        if(encryptedText!=""):
          modular_inverse = sympy.mod_inverse(rNumber, qNumber)
          messageReverse=(int(encryptedText)*modular_inverse)%qNumber
          for i in range(len(w)-1):
            arrayBits.append(0)
          while count!=(len(w)):
            count+=1
            for i in range((len(w)-1),-1,-1):
                  if(messageReverse>=w[i]):
                    arrayBits[i]=1
                    messageReverse=messageReverse-w[i]
                    w.remove(w[i])
                    break
            if(messageReverse>0):
              if(w[0]==messageReverse):
                index=w.index(messageReverse)
                arrayBits[index]=1
          letter=""
          for i in arrayBits:
            letter=letter+str(i)
          outputText=outputText+chr(int(letter,2))
      planeDecrypt=open("plaintext2.txt","w")
      planeDecrypt.write(str(outputText))
      planeDecrypt.close()
      filequals("plaintext2.txt","plaintext.txt")
  else:
    print("key files could not be found. Please run the keygen function!")

def filequals(plaintext,plaintext2):
  f1=open(plaintext,"r")
  f2=open(plaintext2,"r")
  file1=f1.read()
  file2=f2.read()
  if(file1==file2):
    print("Files equal")
  else:
    print("files not equal")
  f1.close()
  f2.close()