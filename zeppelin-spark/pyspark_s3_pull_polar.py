
file_list = [key.key for key in s3.Bucket('polar-fulldump').objects.all()]
first_file = file_list[0]
s3.Object('mybucket', first_file)

# .put(Body=open('/tmp/hello.txt', 'rb'))