import bpy
from mathutils import Matrix, Vector
import os
import math

objects = bpy.context.scene.objects

class panel(bpy.types.Panel):
    bl_label = "DynamX Editor"
    bl_idname = "template"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "DynamX Editor"
   
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        paths = context.scene.paths
        
        col.prop(paths, "import_obj")
        col.prop(paths, "export_obj")
        col.prop(paths, "export_config")
        
        col.prop(paths, "pack_name")
        
        layout.operator("model.next")
        
        layout.prop(paths, "pack_path")
        layout.operator("create.pack")
        
class paths(bpy.types.PropertyGroup):
    import_obj: bpy.props.StringProperty(name="Import .obj path",
                                        description="Folder containing the 'body', 'steering' and 'wheel' folders",
                                        default="...\\export\\",
                                        maxlen=1024,
                                        subtype="FILE_PATH")
                                        
    export_obj: bpy.props.StringProperty(name="Export .obj path",
                                        description=".obj export folder",
                                        default="...\\.minecraft\\DynamX\\DrawLife\\assets\\dynamxmod\\models\\obj\\",
                                        maxlen=1024,
                                        subtype="FILE_PATH")
                                        
    export_config: bpy.props.StringProperty(name="Export .dynx path",
                                        description=".dynx export folder",
                                        default="...\\.minecraft\\DynamX\\DrawLife\\vehicles\\",
                                        maxlen=1024,
                                        subtype="FILE_PATH")
                                        
    pack_name: bpy.props.StringProperty(name="Pack name",
                                        description="Name used by the dynamx pack",
                                        default="DrawLife")
                                        
    pack_path: bpy.props.StringProperty(name="Pack path",
                                        description="The directory to create the pack",
                                        default="...\\.minecraft\\DynamX\\",
                                        maxlen=1024,
                                        subtype="FILE_PATH")
          
class create_pack(bpy.types.Operator):
    bl_label = "Generate pack"
    bl_idname = "create.pack"
    bl_description = "Setup a new DynamX pack"
    
    def directory_exist():
        self.report({'ERROR'}, "The directories already exist")
        print("The directories already exist")
    
    def invoke(self, context, event):
        paths = context.scene.paths
        pack1 = paths.pack_path + "\\" + paths.pack_name + "\\assets\\dynamxmod\\lang"
        pack2 = paths.pack_path + "\\" + paths.pack_name + "\\assets\\dynamxmod\\models\\item"
        pack3 = paths.pack_path + "\\" + paths.pack_name + "\\assets\\dynamxmod\\models\\obj"
        pack4 = paths.pack_path + "\\" + paths.pack_name + "\\vehicles"
        
        #Try to create directories
        try:
            os.makedirs(pack1)
        except:
            directory_exist()
            
        try:
            os.makedirs(pack2)
        except:
            directory_exist()
            
        try:
            os.makedirs(pack3)
        except:
            directory_exist()
            
        try:
            os.makedirs(pack4)
        except:
            directory_exist()
            
        self.report({'INFO'}, "The creation of the pack has been completed")
        print("The creation of the pack has been completed")
        
        return {'FINISHED'}
   
    def draw(self, context):
        layout = self.layout
       
    def execute(self, context):
        return {'FINISHED'}    
                                        
class next_model(bpy.types.Operator):
    bl_label = "Next vehicle"
    bl_idname = "model.next"
    bl_description = "Save the vehicle, load the next one and generate the configuration of the current vehicle"
    
    #Vehicle vars
    vehicle_name = ""
    vehicle_flwheel = list()
    vehicle_frwheel = list()
    vehicle_blwheel = list()
    vehicle_brwheel = list()
    vehicle_steering = list()
    vehicle_seat0 = list()
    vehicle_seat1 = list()
    vehicle_seat2 = list()
    vehicle_seat3 = list()
    vehicle_coll0 = list()
    vehicle_coll1 = list()
    model_index = 0
    
    #Clear objects
    def clear_scene():
        #Clearing scene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
    #Clear materials
    def delete_materials():
        for material in bpy.data.materials:
            bpy.data.materials.remove(material) 
            
    #Rename texture to lower
    def mtl_texture_lower(file, texture):
        try:
            mtl = open(file + ".mtl", "r")
            
            new_file = ""
            for line in mtl:
                new_line = line
                if("map_kd" in line.lower()):
                    new_line = line.lower()
                new_file += new_line
            mtl.close()
            
            mtl = open(file, "w")
            mtl.write(new_file)
            mtl.close()
        
            os.rename(texture, texture.lower())
        except:
            print("Unable to rename the texture")
        
    def fix_model_syntax(file):
        obj = open(file, "r")
        
        new_file = ""
        for line in obj:
            new_line = line
            if("#" in line.lower()):
                new_line = line.split("#", 1)[0] + "\n"
            new_file += new_line
        obj.close()
        
        obj = open(file, "w")
        obj.write(new_file)
        obj.close()
            
   
    def invoke(self, context, event):
        wm = context.window_manager
        
        paths = context.scene.paths
        
        vehicle_objects = ["wheel_front_left", "body", "wheel_front_right", "wheel_back_left", "wheel_back_right", "steering"]
        vehicle = list()
        
        #Save the configuration file and export the body model
        if(next_model.vehicle_name != ""):
            vehicle_name = next_model.vehicle_name
            
            #Updates the position, rotation and size of objects in the configuration
            for obj in objects:
                if("wheel_front_left" in obj.name):
                    next_model.vehicle_flwheel = [obj.location.x, obj.location.y, obj.location.z]
                if("wheel_front_right" in obj.name):
                    next_model.vehicle_frwheel = [obj.location.x, obj.location.y, obj.location.z]
                if("wheel_back_left" in obj.name):
                    next_model.vehicle_blwheel = [obj.location.x, obj.location.y, obj.location.z]
                if("wheel_back_right" in obj.name):
                    next_model.vehicle_brwheel = [obj.location.x, obj.location.y, obj.location.z]
                if("steering" in obj.name):
                    obj.name = "SteeringWheel"
                    obj.data.name = "SteeringWheel"
                if("seat0" in obj.name):
                    next_model.vehicle_seat0 = [obj.location.x, obj.location.y, obj.location.z]
                if("seat1" in obj.name):
                    next_model.vehicle_seat1 = [obj.location.x, obj.location.y, obj.location.z]
                if("seat2" in obj.name):
                    next_model.vehicle_seat2 = [obj.location.x, obj.location.y, obj.location.z]
                if("seat3" in obj.name):
                    next_model.vehicle_seat3 = [obj.location.x, obj.location.y, obj.location.z]
                if("coll0" in obj.name):
                    next_model.vehicle_coll0 = [obj.location.x, obj.location.y, obj.location.z, obj.scale.x, obj.scale.y, obj.scale.z]
                if("coll1" in obj.name):
                    next_model.vehicle_coll1 = [obj.location.x, obj.location.y, obj.location.z, obj.scale.x, obj.scale.y, obj.scale.z]
                    
                #Selects and removes unnecessary objects
                obj.select_set(False)
                if("body" in obj.name):
                    obj.name = "Chassis"
                    obj.data.name = "Chassis"
                elif(not "SteeringWheel" in obj.name):
                    obj.select_set(True)
            bpy.ops.object.delete()
            
            #Try to export the body model
            path = paths.export_obj + "\\" + vehicle_name + "\\"
            try:
                bpy.ops.export_scene.obj(filepath=path + vehicle_name + "_body.obj", path_mode='COPY')
            except:
                self.report({'ERROR'}, "Can't export model. The file may already exist")
                print("Can't export model. The file may already exist")
            
            #Try to create the vehicle directory
            path = paths.export_config + "\\" + vehicle_name + "\\"
            try:
                os.mkdir(path)
            except:
                self.report({'INFO'}, "directory '" + path + "' already exist")
                print("directory '" + path + "' already exist")
            
            #Write the vehicle config file
            vehicle_file = path + "vehicle_" + vehicle_name + ".dynx"
            with open(vehicle_file, 'w') as file:
                file.write("""Description: """ + vehicle_name + """
                
EmptyMass: 1191
DragCoefficient: 0.4
CenterOfGravityOffset: 0 0 0

DrawLifeAddon{
    Trunk: 20
    FuelInTank: 50
    Strength: 100
    Trunk_Position: -0.020345 2.64449 1.14081
    Trunk_Scale: 0.777124 0.365566 0.5
    Motor_Position: 0.005389 -1.33169 1.14081
    Motor_Scale: 0.777124 0.706801 0.223486
}

Model: obj/""" + vehicle_name + """/""" + vehicle_name + """_body.obj
ShapeYOffset: 0.2

DefaultEngine: """ + paths.pack_name + """.engine_""" + vehicle_name + """
DefaultSounds: """ + paths.pack_name + """.sounds_""" + vehicle_name + """

SteeringWheel{
    PartName: SteeringWheel
    BaseRotation: 1 """ + str(next_model.vehicle_steering[3]) + """ """ + str(next_model.vehicle_steering[4]) + """ """ + str(next_model.vehicle_steering[5]) + """
    RotationPoint: """ + str(next_model.vehicle_steering[0]) + """ """ + str(next_model.vehicle_steering[1]) + """ """ + str(next_model.vehicle_steering[2]) + """
}

Shape_Core{
    ShapeScale: """ + str(next_model.vehicle_coll0[3]) + """ """ + str(next_model.vehicle_coll0[4]) + """ """ + str(next_model.vehicle_coll0[5]) + """
    ShapePosition: """ + str(next_model.vehicle_coll0[0]) + """ """ + str(next_model.vehicle_coll0[1]) + """ """ + str(next_model.vehicle_coll0[2]) + """
}
Shape_Top{
    ShapeScale: """ + str(next_model.vehicle_coll1[3]) + """ """ + str(next_model.vehicle_coll1[4]) + """ """ + str(next_model.vehicle_coll1[5]) + """
    ShapePosition: """ + str(next_model.vehicle_coll1[0]) + """ """ + str(next_model.vehicle_coll1[1]) + """ """ + str(next_model.vehicle_coll1[2]) + """
}

WheelFrontLeft{
    AttachedWheel: """ + paths.pack_name + """.wheel_""" + vehicle_name + """
    isRight: false
    Position: """ + str(next_model.vehicle_flwheel[0]) + """ """ + str(next_model.vehicle_flwheel[1]) + """ """ + str(next_model.vehicle_flwheel[2]) + """
    IsSteerable: True
    MaxTurn: 0.7
    DrivingWheel: False
}
WheelFrontRight{
    AttachedWheel: """ + paths.pack_name + """.wheel_""" + vehicle_name + """
    isRight: true
    Position: """ + str(next_model.vehicle_frwheel[0]) + """ """ + str(next_model.vehicle_frwheel[1]) + """ """ + str(next_model.vehicle_frwheel[2]) + """
    IsSteerable: True
    MaxTurn: 0.7
    DrivingWheel: False
}

WheelBackLeft{
    AttachedWheel: """ + paths.pack_name + """.wheel_""" + vehicle_name + """
    isRight: false
    Position: """ + str(next_model.vehicle_blwheel[0]) + """ """ + str(next_model.vehicle_blwheel[1]) + """ """ + str(next_model.vehicle_blwheel[2]) + """
    IsSteerable: False
    MaxTurn: 0
    DrivingWheel: True
}

WheelBackRight{
    AttachedWheel: """ + paths.pack_name + """.wheel_""" + vehicle_name + """
    isRight: true
    Position: """ + str(next_model.vehicle_brwheel[0]) + """ """ + str(next_model.vehicle_brwheel[1]) + """ """ + str(next_model.vehicle_brwheel[2]) + """
    IsSteerable: False
    MaxTurn: 0
    DrivingWheel: True
}

DriverSeat{
    Position: """ + str(next_model.vehicle_seat0[0]) + """ """ + str(next_model.vehicle_seat0[1]) + """ """ + str(next_model.vehicle_seat0[2]) + """
    Driver: True
}
PassengerFrontSeat{
    Position: """ + str(next_model.vehicle_seat1[0]) + """ """ + str(next_model.vehicle_seat1[1]) + """ """ + str(next_model.vehicle_seat1[2]) + """
    Driver: false
}
PassengerBackLeftSeat{
    Position: """ + str(next_model.vehicle_seat2[0]) + """ """ + str(next_model.vehicle_seat2[1]) + """ """ + str(next_model.vehicle_seat2[2]) + """
    Driver: false
}
PassengerBackRightSeat{
    Position: """ + str(next_model.vehicle_seat3[0]) + """ """ + str(next_model.vehicle_seat3[1]) + """ """ + str(next_model.vehicle_seat3[2]) + """
    Driver: false
}
""")
            file.close()
                
            #Write the wheel config file
            wheel_file = path + "wheel_" + vehicle_name + ".dynx"
            with open(wheel_file, 'w') as file:
                file.write("""Model: obj/""" + vehicle_name + """/""" + vehicle_name + """_wheel.obj
Width: 0.226
WheelRadius: 0.551
RimRadius: 0.323
Friction: 1
BrakeForce: 70
RollInInfluence: 1
SuspensionRestLength: 0.05
SuspensionStiffness: 30
SuspensionMaxForce: 10000
WheelDampingRelaxation: 0.45
WheelsDampingCompression: 0.22
""")
            file.close()
                
            #Write the sounds config file
            sounds_file = path + "sounds_" + vehicle_name + ".dynx" 
            with open(sounds_file, 'w') as file:
                file.write("""Engine{
    Interior{
        Starting{
            Sound: tt_start
        }
        0-1500{
            Sound: tt_int_idle
            PitchRange: 0.5 2.0
        }
        1400-5000{
            Sound: tt_int_low
            PitchRange: 0.0 0.7
        }
        4900-9000{
            Sound: tt_int_high
            PitchRange: 0.0 0.65
        }
    }
    Exterior{
        Starting{
            Sound: tt_start
        }
        0-1500{
            Sound: tt_ex_idle
            PitchRange: 0.5 2.0
        }
        1400-5000{
            Sound: tt_ex_low
            PitchRange: 0.0 0.7
        }
        4900-9000{
            Sound: tt_ex_high
            PitchRange: 0.0 0.65
        }
    }
}
""")
            file.close()
                
            #Write the engine config file
            engine_file = path + "engine_" + vehicle_name + ".dynx"
            with open(engine_file, 'w') as file:
                file.write("""Power: 1683
MaxRPM: 5000
Braking: 15

Point_1{
    RPMPower: 0 0
}
Point_2{
    RPMPower: 900 0.55
}
Point_3{
    RPMPower: 1400 0.50
}
Point_4{
    RPMPower: 1900 0.60
}
Point_5{
    RPMPower: 2400 0.70
}
Point_6{
    RPMPower: 2900 0.80
}
Point_7{
    RPMPower: 3400 0.70
}
Point_8{
    RPMPower: 4000 0.45
}
Point_9{
    RPMPower: 5000 0.3
}

Gear_0{
    SpeedRange: 0 -30
    RPMRange: 800 5000
}
Gear_1{
    SpeedRange: -1000000 1000000
    RPMRange: 0 5000
}
Gear_2{
    SpeedRange: 0 10
    RPMRange: 800 2400
}
Gear_3{
    SpeedRange: 10 30
    RPMRange: 800 2400
}
Gear_3{
    SpeedRange: 30 50
    RPMRange: 850 2400
}
Gear_4{
    SpeedRange: 50 70
    RPMRange: 900 2400
}
Gear_5{
    SpeedRange: 70 85
    RPMRange: 900 2400
}
Gear_6{
    SpeedRange: 85 175
    RPMRange: 900 5000
}
""")
            file.close()
            next_model.vehicle_name = ""
            
        #Clear the scene and the materials
        next_model.clear_scene()
        next_model.delete_materials()
        
        #Opens all parts of the vehicle
        for object in vehicle_objects:
            dir = os.path.join(paths.import_obj + "\\" + object.replace("_front_left", "").replace("_front_right", "").replace("_back_left", "").replace("_back_right", ""))
            files = sorted(os.listdir(dir))
            objs = [item for item in files if item.endswith('.obj')]
            
            try:
                obj = objs[next_model.model_index]
            except:
                #Reset the model index
                next_model.model_index = 0
                self.report({'INFO'}, "No vehicle to load !")
                print("No vehicle to load !")
                return {'FINISHED'}
            
            #Export the vehicle wheel model
            if(next_model.vehicle_name == ""):
                next_model.vehicle_name = obj.replace(".obj", "").replace("_wheel", "").lower()
                if(next_model.vehicle_name.startswith("model")):
                    next_model.vehicle_name = next_model.vehicle_name[5:]
            
                #Fixing model syntax
                next_model.fix_model_syntax(dir + "\\" + obj)
                #Importing model
                model_path = os.path.join(dir, obj)
                bpy.ops.import_scene.obj(filepath = model_path)
                obj_wheel = objects[0]
                
                #Set geometry to origin
                bpy.context.view_layer.objects.active = obj_wheel
                bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
                
                #Set Z rotation
                obj_wheel.rotation_euler[2] = math.radians(-90)
                
                vehicle_name = next_model.vehicle_name
  
                #Try to create the vehicle directory
                path = paths.export_obj + "\\" + vehicle_name + "\\"
                try:
                    os.mkdir(path)
                except:
                    self.report({'ERROR'}, "directory '" + path + "' already exist")
                    print("directory '" + path + "' already exist")
                
                #Exporting obj
                objName = path + vehicle_name + "_wheel"
                try:
                    bpy.ops.export_scene.obj(filepath=objName + ".obj", path_mode='COPY')
                except:
                    self.report({'ERROR'}, "Can't export model. The file may already exist")
                    print("Can't export model. The file may already exist")
                    
                if(len(bpy.data.images) > 0):
                    next_model.mtl_texture_lower(objName, path + bpy.data.images[0].name)
                    
                #Clear the scene
                next_model.clear_scene()
            
            #Fixing model syntax
            next_model.fix_model_syntax(dir + "\\" + obj)
            #Importing model
            model_path = os.path.join(dir, obj)
            bpy.ops.import_scene.obj(filepath = model_path)
            
        for obj in objects:
            #Setting material for each objects
            obj.data.materials.clear()
            obj.data.materials.append(bpy.data.materials[2])
            
            #Set Z rotation
            obj.rotation_euler[2] = math.radians(-90)
            bpy.ops.object.select_all(action='SELECT')
              
        index = 0
        for obj in objects:
            #Setting up object names
            obj.name = next_model.vehicle_name + "_" + vehicle_objects[index]
            index+=1
            
            if("_steering" in obj.name):
                next_model.vehicle_steering = [obj.location.x, obj.location.y, obj.location.z, math.degrees(obj.rotation_euler[0]), math.degrees(obj.rotation_euler[1]), math.degrees(obj.rotation_euler[2])]
                obj.location = (0, 0, 0)
                obj.rotation_euler[1] -= math.radians(25)
            
            #Right wheel placement
            if("_front_right" in obj.name or "_back_right" in obj.name):
                obj.location.x = -obj.location.x
                
            #Rear wheels placement
            if("_back_" in obj.name):
                obj.location.y = -obj.location.y
                
            #Set origin to geometry
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
            
        #Adding seats
        for i in range(4):
            try:
                bpy.ops.import_scene.fbx(filepath = bpy.path.abspath("//content\\steve.fbx"))
            except:
                self.report({'ERROR'}, "Please use the \"DynamXVehicle.blend\" file to run the program. Steve (seat) has been replaced by a cube.")
                print("Please use the \"DynamXVehicle.blend\" file to run the program. Steve (seat) has been replaced by a cube.")
                bpy.ops.mesh.primitive_cube_add(size=0.1)
            
        index = 0
        for obj in objects:
            if("seat" in obj.name):
                obj.name = "seat" + str(index)
            
                if(index == 0):
                    obj.location=(0.65,-0.05,-0.02)
                elif(index == 1):
                    obj.location=location=(-0.65,-0.05,-0.02)
                elif(index == 2):
                    obj.location=location=(0.65,1.5,-0.02)
                else:
                    obj.location=location=(-0.65,1.5,-0.02)
                index+=1

        #Adding collision objects
        mat_col = bpy.data.materials.new(name="collision")
        mat_col.use_nodes = True
        mat_col.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.116892, 0.8, 0.0847513, 1)
        mat_col.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0.0666667
        mat_col.blend_method='BLEND'

        for i in range(2):
            bpy.ops.mesh.primitive_cube_add()
            obj = bpy.context.selected_objects[0]
            obj.name = "coll" + str(i)
            obj.data.materials.append(mat_col)
            
            if(i == 0):
                obj.location=(0,-0.15,0.2)
                bpy.ops.transform.resize(value=(1.4,3.5,0.7))
            else:
                obj.location=(0,0.7,1.27)
                bpy.ops.transform.resize(value=(1.4,2.1,0.38))
                
        #Increasing vehicle index
        next_model.model_index += 1
        
        return {'FINISHED'}
   
   
    def draw(self, context):
        layout = self.layout
       
   
    def execute(self, context):
        return {'FINISHED'}    

classes = [panel, paths, create_pack, next_model]
 
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.paths = bpy.props.PointerProperty(type=paths)
 
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.paths
    del(bpy.types.Scene.QueryProps)
 
if __name__ == "__main__":
    register()