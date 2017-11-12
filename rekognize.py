import boto3

s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
    print(bucket.name)

##name of the source file	
sourceFile='sample.jpg'

data = open(sourceFile, 'rb')
s3.Bucket('securecheckin').put_object(Key=sourceFile, Body=data)


bucket='securecheckin'
##targetFile='maxbase.jpg'

targetFiles = ['maxbase.jpg', 'peterbase.jpg', 'muntaserbase.jpg', 'skylarbase.jpg']

client=boto3.client('rekognition')

found = 0
for target in targetFiles:

    response=client.compare_faces(SimilarityThreshold=70, SourceImage={'S3Object':{'Bucket':bucket,'Name':sourceFile}}, TargetImage={'S3Object':{'Bucket':bucket,'Name':target}})

    for faceMatch in response['FaceMatches']:
            position = faceMatch['Face']['BoundingBox']
            confidence = str(faceMatch['Face']['Confidence'])
            print('The face at ' +
                       str(position['Left']) + ' ' +
                       str(position['Top']) +
                       ' matches with ' + confidence + '% confidence')
            print('\n recognized file is ' + target)
            found = 1
            break
    if found==1:
        break


if found==0:
    print('none')
  
		   

		   
obj = s3.Object("securecheckin", sourceFile)
obj.delete()
