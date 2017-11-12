import RPi.GPIO as GPIO
import time
import os
import requests
import json
import sys
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto import Random
import boto3


# Padding for the input string --not
# related to encryption itself.
BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class AESCipher:
    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3 and PyCrypto 2.6.1.
    """


    def __init__(self, key):
        #self.key = md5(key.encode('utf8')).hexdigest()
	##self.key = md5(key).hexdigest()
	##hacky solution
	self.key = "hackathongsu2017"


    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:])).decode('utf8')







##START CODE









GPIO.setmode(GPIO.BCM)

TRIG = 23 
ECHO = 24

count = 0

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)

flag = 0

while count <3 :
  print "Distance Measurement In Progress"

  print "Waiting For Sensor To Settle"
  time.sleep(2)

  GPIO.output(TRIG, True)
  time.sleep(0.00001)
  GPIO.output(TRIG, False)

  while GPIO.input(ECHO)==0:
    pulse_start = time.time()

  while GPIO.input(ECHO)==1:
    pulse_end = time.time()

  pulse_duration = pulse_end - pulse_start

  distance = pulse_duration * 17150

  distance = round(distance, 2)

  print "Distance:",distance,"cm"

  #GPIO.cleanup()

  time.sleep(5)
  
  ##do stuff here if user found

  if distance<100 :
    if flag == 1:
      continue
    
    flag = 1
    print ('\n user detected!!\n')
    print ('\n taking photo of user \n')

    ##uncomment to activate
    ##os.system("raspistill -o sample.jpg")

    time.sleep(5)
    print ('\n photo captured, now calling server for rekognition \n')
    ##s3 = boto3.resource('s3')
    boto3.setup_default_session(region_name='us-east-1')
    s3 = boto3.resource('s3', aws_access_key_id='AKIAJHOPDASKMDTOMDAQ', aws_secret_access_key='m/659qzxZeGxecnT0ENBq8EJzDED9b4mojLROj7l', region_name='us-east-1')

    for bucket in s3.buckets.all():
        print(bucket.name)

    sourceFile='sample.jpg'

    data = open(sourceFile, 'rb')
    s3.Bucket('securecheckin').put_object(Key=sourceFile, Body=data)

    bucket='securecheckin'

    mybucket = s3.Bucket(bucket)

    for object in mybucket.objects.all():
        print(object.key)

    list1 = mybucket.objects.all()
    

    ##targetFiles = ['maxbase.jpg', 'peterbase.jpg', 'muntaserbase.jpg', 'skylarbase.jpg']

    client=boto3.client('rekognition', aws_access_key_id='AKIAJHOPDASKMDTOMDAQ', aws_secret_access_key='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', region_name='us-east-1')
    
    foundperson=''
    found = 0
    for target in list1:
        
        if target.key=='sample.jpg' :
            continue
        response=client.compare_faces(SimilarityThreshold=70, SourceImage={'S3Object':{'Bucket':bucket,'Name':sourceFile}}, TargetImage={'S3Object':{'Bucket':bucket,'Name':target.key}})

        for faceMatch in response['FaceMatches']:
                position = faceMatch['Face']['BoundingBox']
                confidence = str(faceMatch['Face']['Confidence'])
                print('The face at ' +
                           str(position['Left']) + ' ' +
                           str(position['Top']) +
                           ' matches with ' + confidence + '% confidence')
                print('\n recognized file is ' + target.key)
                print('\n proceed to fingerprint verification\n')
                foundperson = target.key
                found = 1
                break
        if found==1:
            break


    if found==0:
        print('none')
      
                       


    ##reset image database
    
    obj = s3.Object("securecheckin", sourceFile)
    obj.delete()
    obj = s3.Object("securecheckin", 'newuser.jpg')
    obj.delete()


   
  else:
      flag = 0
  
  count +=1

GPIO.cleanup()
print ('\n end of program reached!!\n')
