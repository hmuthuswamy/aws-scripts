#!/usr/bin/python
import boto.ec2
from datetime import datetime, timedelta

# Remember to install boto before running this script
# After checking out from github 
   # 1.  add the access and secret key
   # 2.  specify region
   # 3.  specify snapshotdays_limit , currently set to 15
   # 4.  specify volumes_list , these are the volumes for which snapshots will be managed
   # 5.  specify exception_list,  these are the snapshots which will be excluded from deletion
class ec2snapshots:
   access_key = ''
   secret_key = ''
   # Specify region   eg.   regions = ['us-west-2']
   regions = ['']
   snapshotdays_limit = 15     # number of days to keep snapshots 
   # Volume list for creating snapshots     eg. volume_list = ['vol-xxxxxxxx','vol-yyyyyyyy']
   volume_list = ['','']
   # Snapshots that you dont want to delete    eg. exception_list = ['Snapshot:snap-xxxxxxxx','Snapshot:snap-yyyyyyyy' ]
   exception_list = ['','' ]

   def __init__(self):
      print "Initiating Snapshot Maintenance"

   def connect_region(self,region):
      self.region = region
      ec2_conn = boto.ec2.connect_to_region(region, aws_access_key_id = ec2snapshots.access_key, aws_secret_access_key = ec2snapshots.secret_key)      
      return ec2_conn

   def create_snapshot(self,volume_id,ec2_conn):
      self.volume_id = volume_id
      self.ec2_conn  = ec2_conn
      snapshot = self.ec2_conn.create_snapshot(volume_id,'db snapshot')
      print 'snapshot taken'
      return snapshot

   def get_snapshotlist(self,volume_id,ec2_conn):
      self.volume_id = volume_id
      self.ec2_conn = ec2_conn
      sp = self.ec2_conn.get_all_snapshots(filters={'volume_id':self.volume_id})
      return sp

   def get_deletion_time(self,days):
      self.days = days
      deletion_time = datetime.utcnow() - timedelta(days=days)
      return deletion_time

   def delete_snapshot(self,snapshot):
      self.snapshot = snapshot
      print "Deleting Snapshot : " + str(self.snapshot)  
      self.snapshot.delete() 

aws_ec2 = ec2snapshots()
deletion_time = aws_ec2.get_deletion_time(ec2snapshots.snapshotdays_limit)
print "deletion time " + str(deletion_time)
for region in aws_ec2.regions:
   ec2_conn = aws_ec2.connect_region(region)
   for volume in ec2snapshots.volume_list:
      snp = aws_ec2.create_snapshot(volume,ec2_conn)
      snaps = aws_ec2.get_snapshotlist(volume,ec2_conn)
      print "count of snaps =  " ,len(snaps)
      for snap in snaps:
         start_time = datetime.strptime(snap.start_time,'%Y-%m-%dT%H:%M:%S.000Z')
         if start_time < deletion_time :
            print str(snap) + " " + snap.start_time
            if str(snap) not in aws_ec2.exception_list :
               aws_ec2.delete_snapshot(snap)
      
