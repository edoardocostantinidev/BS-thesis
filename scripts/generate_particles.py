import bpy
import bmesh
import csv
import os.path
from os import path
import time
import sys

start_time = time.time()
INPUT_PATH = '/home/edoardo/Downloads/output/'

def delete_all(name):
    for o in bpy.context.scene.objects:
        if o.name.startswith(name):
            o.select_set(True)
    bpy.ops.object.delete()

def getParticleFileName():
    frame = bpy.context.scene.frame_current
    prefix = INPUT_PATH + 'particles'
    fileName = getParticleFileName(prefix,frame)
    print('Frame: ' + str(frame) + '\nReading file: ' +fileName)
    s = str(frame)
    while(len(s) < 5):
        s = '0'+s
    return prefix+s+'.csv'



def main():
    delete_all('particle')
    fileName = getParticleFileName()
    print(fileName)
    
if __name__ == "__main__":
  main()