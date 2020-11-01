import bpy
import bmesh
import csv
import os.path
from os import path
import time
start_time = time.time()

def add_sphere(name, x, y, z, u_segments, v_segments,diameter):
    # Create an empty mesh and the object.
    mesh = bpy.data.meshes.new(name)
    basic_sphere = bpy.data.objects.new(name, mesh)
    basic_sphere.location.x = x
    basic_sphere.location.y = y
    basic_sphere.location.z = z
    # Add the object into the scene.
    bpy.context.collection.objects.link(basic_sphere)
    

    # Select the newly created object
    bpy.context.view_layer.objects.active = basic_sphere
    basic_sphere.select_set(True)

    # Construct the bmesh sphere and assign it to the blender mesh.
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=u_segments, v_segments=v_segments, diameter=diameter)
    bm.to_mesh(mesh)
    bm.free()

    #bpy.ops.object.modifier_add(type='SUBSURF')
    #bpy.ops.object.shade_smooth()
    
    return basic_sphere

def add_icosphere(name, x, y, z, subdivisions, diameter):
    # Create an empty mesh and the object.
    mesh = bpy.data.meshes.new(name)
    basic_sphere = bpy.data.objects.new(name, mesh)
    basic_sphere.location.x = x
    basic_sphere.location.y = y
    basic_sphere.location.z = z
    # Add the object into the scene.
    bpy.context.collection.objects.link(basic_sphere)
    

    # Select the newly created object
    bpy.context.view_layer.objects.active = basic_sphere
    basic_sphere.select_set(True)

    # Construct the bmesh sphere and assign it to the blender mesh.
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm,subdivisions=subdivisions,diameter=diameter)
    bm.to_mesh(mesh)
    bm.free()

    #bpy.ops.object.modifier_add(type='SUBSURF')
    #bpy.ops.object.shade_smooth()
    
    return basic_sphere

def delete_all(name):
    for o in bpy.context.scene.objects:
        if o.name.startswith(name):
            o.select_set(True)
    bpy.ops.object.delete()

def getParticleFileName(prefix,frame):
    s = str(frame)
    while(len(s) < 5):
        s = '0'+s
    return prefix+s+'.csv'

def joinObjects(objects):
    ctx = bpy.context.copy()
    # one of the objects to join
    ctx['active_object'] = objects[0]
    ctx['selected_objects'] = objects
    bpy.ops.object.join(ctx)
    return objects[0]

def main():
    delete_all('particle')
    frame = bpy.context.scene.frame_current
    prefix = '/home/edoardo/Downloads/output/particles'
    fileName = getParticleFileName(prefix,frame)
    print('Frame: ' + str(frame) + '\nReading file: ' +fileName)
    last = None
    objects=[]
    count = 1
    if path.exists(fileName):
        with open(fileName, 'r') as file:
            reader = csv.reader(file)
            firstline = True
            for row in reader:
                count = count+1
                if firstline:
                    firstline = False
                    continue
                #current = add_sphere('particle',float(row[0]),float(row[1]),float(row[2]),8,4,0.00025)
                current = add_icosphere('particle',float(row[0]),float(row[1]),float(row[2]),2,0.00025)
                if last is None:
                    last = current
                    objects.append(current)
                else:
                    objects.append(current)
                    if count%42==0: #42 magic number that actually reduce time to insert in scene
                        last = joinObjects(objects)
                        objects.clear()
                        objects.append(last)
    joinObjects(objects) #join remainders
    bpy.ops.transform.resize(value=(100, 100, 100))
    print('Generated '+str(count)+' particles')               
    timeInSeconds = (time.time() - start_time)
    print("--- %s seconds ---" % timeInSeconds)
    print('For a total of ' + str(count/timeInSeconds) + ' particles/second')
if __name__ == "__main__":
  main()
