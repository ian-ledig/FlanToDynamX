[French translation](https://github.com/Pacito2)

# FlanToDynamX

This pack contains two programs allowing to pass toolbox .java models intended for Flan's mod on the Dynamx mod.

## Getting Started

Do not hesitate to report any errors.
It is not complicated to use these programs. Take care to read each step carefully.

## Prerequisites

Java			(https://www.java.com/fr/download/)
Toolbox			(https://www.minecraft-smp.de/index.php/toolbox-2-0)
Blender >2.8	(https://www.blender.org/)

## Instructions

### Editing .java models

Add your .java models to the "./import" folder.
Open the program "JavaVehicleExtractor.jar".
Wait for it to alert you when its execution is finished.

### Switching from .java to .obj models

Open Toolbox.
For each models in 
	./export/body, 
	./export/steering,
	./export/wheel. 
	Do this:
	
	-	Import > Model From Java > *Select the model*.
	-	Import > Texture from File > *Select the model texture*.
	(For wheel, for example, check that the model contains only the left wheel. If not, remove the disturbing objects).
	-	Export > As .Obj Model (All Parts in 1 Mesh) (the last option) > *Select the same directory as the .java (./export/...)*.

### Adding vehicles to DynamX

Open "DynamXVehicle.blend" with Blender.
Go to the "Scripting" tab (towards the center at the top).
Click on "Run Script" (arrow icon).
Go to the first tab "Layout" (on top).
Press "N".
Go to the "Dynamx Editor" tab (on the side, to the right of the appeared window):
	
	a. To generate an empty DynamX pack (If you don't already have one):
		-	Enter a pack name in "Pack name".
		-	Select a path in "Pack path" (example: .minecraft/DynamX).
		-	Click on "Generate pack".
		
	b. To import vehicles:
		-	In "Import .obj path", select the "export" folder previously generated.
		-	Fill in the field "Export .obj path" (example: .minecraft/DynamX/*packName*/assets/dynamxmod/models/obj).
		-	Fill in the field "Export .dynx path" (example: .minecraft/DynamX/*packName*/vehicles).
		-	Enter a pack name in "Pack name".
		-	Click on "Next vehicle" (A vehicle should appear).
		-	You can reposition the wheels and seats if they are not properly configured (Don't touch the steering wheel!).
		-	Replace and adjust the size of the two collision boxes.
		-	Click on "Next vehicle" to generate the vehicle configuration and process the next one.
		You can launch your game and drive your vehicle =)

## Authors

* **Pacito2** - *Initial work* - [Pacito2](https://github.com/Pacito2)
* **Bravesonny** - *Modeling seated Steve model*

