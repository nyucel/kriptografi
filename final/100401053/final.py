import random
import os,sys
from datetime import datetime


def final(dosyaName):
    with open(dosyaName, 'r') as dosya:
        data=dosya.read()
    data=bin(int(data,16))[2::].zfill(64)
    dataKey='11011100001100101110100010101010010111000011001'
    result=''
    result=data
    for i in range(0,16):
        firstBit=result[0:31]
        secondBit=result[32:64]
        secondBit=int(secondBit)^int(dataKey,2)
        secondBit=bin(int(secondBit))[2::].zfill(32)
        secondBit=int(firstBit,16) ^ int(secondBit,2)
        result=str(secondBit) + firstBit
    result=hex(int(result))
    lenResult=len(result)
    result=result[(lenResult-8):lenResult]
    return (bin(int(result, 16))[2:].zfill(32))



i=1
startTime=float(datetime.now().minute)
while i<100:
    Idouble=str(i)
    while len(Idouble)<3:
        Idouble='0'+Idouble
    firstBlok=final(Idouble+".txt")
    rasgele=str(bin(random.getrandbits(32))[2:].zfill(32))
    createBlok=str(bin(int(firstBlok,2) + int(rasgele,2))[2:].zfill(32))[0:32]
    a=0
    hashsum=open("HASHSUM.txt", 'a+')
    hashsumValue=hashsum.read()
    with open('control.txt','w') as dosya:
        dosya.write(str(hex(int(createBlok,2)))[2::])
    finaltime=float(datetime.now().minute)
    if((finaltime-startTime)<10.0):
    
        secondBlok=final("control.txt")
        dosya.close()
        if(hashsumValue.find(secondBlok)<0):
            if(int(secondBlok[0:8])==0):
                randomNumber=rasgele+" - "+secondBlok+"\n"
                
                hashsum.write(randomNumber)
                hashsum.close()
                i+=1
                dosyaName=str(i)
                while len(dosyaName)<3:
                    dosyaName="0"+dosyaName
                with open(dosyaName+".txt", 'a') as hashFile:
                    hashFile.write(str(hex(int(createBlok,2)))[2::])
        else:
            os.remove("control.txt")
    else:
        sys.exit()

os.remove("control.txt")
