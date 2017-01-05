#!/usr/bin/python
import sys
import boto.ec2
import time

# Script to start up new  instance  in AWS EC2 
# After checking out from github,
#    1.  add the access and secret key 
#    2.  specify the ami-id  that you want to use
#    3.  specify the key that you created in AWS , this is the key to login to this instance
#    4.  specify the instance type ( eg. t2.micro ) 
#    5.  specify the security group(s)
#    6.  specify the subnet


class aws_ec2:
   access_key = ''
   secret_key = ''
   regions = ['']
   image_id = ''
   key_name = ''
   instance_type = ''
   security_group = ['']
   subnet=''

   def __init__(self,server_name):
      self.server_name = server_name
      print "Starting creation of " + server_name

   def create_instance(self,image_id,key_name,instance_type,security_group_ids, subnet_id,ec2_conn):
      self.image_id = image_id
      self.key_name = key_name
      self.instance_type = instance_type
      self.security_group_ids = security_group_ids
      self.subnet_id = subnet_id
      self.ec2_conn = ec2_conn
      reservations = ec2_conn.run_instances(self.image_id,key_name=self.key_name,instance_type=self.instance_type,security_group_ids=self.security_group_ids,subnet_id=self.subnet_id)
      
      print "Waiting for 2 minutes for the server to come up"
      time.sleep(120)
      i = reservations.instances[0]
      return reservations

   def connect_region(self,region):
      self.region = region
      ec2_conn = boto.ec2.connect_to_region(region,aws_access_key_id = aws_ec2.access_key,aws_secret_access_key = aws_ec2.secret_key)
      return ec2_conn

   def addtag(self,tag,value,instance,ec2_conn) :
      self.tag = tag
      self.value = value
      self.instance = instance
      self.ec2_conn = ec2_conn
      self.instance.add_tag(self.tag,self.value)

if ( len(sys.argv) < 2 ) :
    print "Usage :  aws_ec2.py <servername>  where servername is the tag for the new instance"
    sys.exit()
else :
   server_name = sys.argv[1]

awsinstance  = aws_ec2(server_name)
ec2_conn = awsinstance.connect_region(awsinstance.regions[0])
reservations = awsinstance.create_instance(awsinstance.image_id,awsinstance.key_name,awsinstance.instance_type,awsinstance.security_group,awsinstance.subnet,ec2_conn)
for instance in reservations.instances:
   awsinstance.addtag('Name',server_name,instance,ec2_conn)
   print " Private ip of  " + server_name + " is " + str(instance.private_ip_address)
