#!/usr/bin/python
##  Script to clean up a directory 
##    
import argparse
import os
from os.path import join, getsize, splitext
from subprocess import check_call,call

def get_dir_size(folder):
    size_of_all_files = 0
    for item in os.walk(folder):
        for file in item[2]:
            try:
                size_of_all_files = size_of_all_files + getsize(join(item[0], file))
            except:
                print('error with file:  ' + join(item[0], file))
    return size_of_all_files

def remove_files(folder):
   for item in os.walk(folder): 
      for file in item[2]:
         print('Removing {}/{}'.format(folder,file))
         os.remove('{}/{}'.format(folder,file))


if (__name__ == '__main__'):
   parser = argparse.ArgumentParser()
   group = parser.add_mutually_exclusive_group()
   group.add_argument('-s','--size',help='Max size of Folder Allowed',action='store')
   group.add_argument('-r','--remove',help='Remove files from  folder ',action='store_true')
   parser.add_argument('folder_name', help='Folder to purge ', type=str)
   args = parser.parse_args()
   
   folder = args.folder_name
   if args.remove:
      print 'Removing files from {}'.format(folder)
      remove_files(folder)
   elif args.size:
      maxsize = int(args.size)
      size_of_folder = float(get_dir_size(folder)) / 1024 /1024 /1024
      print('Size of {} is {} GB before compression.'.format(folder,size_of_folder))
      if ( size_of_folder > maxsize ):
         print 'Freeing up space  by gziping files that have not yet been gzipped'
         for item in os.walk(folder):
            for file in item[2]:
               ext = os.path.splitext(file)[-1].lower()
               if ext !=  '.gz':
                  print('gzipping {}/{}'.format(folder,file))
                  retcode=call(['gzip','{}/{}'.format(folder,file)])
                  if ( retcode != 0 ):
                     print 'Could not gzip {}/{} . retcode : {}'.format(folder,file,retcode)
         size_post_compression = float(get_dir_size(folder)) / 1024 /1024 /1024
         print('Size of {} is {} GB after compression.'.format(folder,size_post_compression))
         print 'Run script with -r to remove all files in {}'.format(folder)
      else:
         print('Size of {} is {} GB. Nothing to clean up'.format(folder,size_of_folder))


