[Traduction anglaise](https://github.com/Pacito2/FlanToDynamX/blob/master/README.md)

# FlanToDynamX

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](ian.ledigfr@gmail.com)

Ce pack contient deux programmes permettant de passer un modèle .java conçu pour Flan's mod sur DynamX.

## Informations

N'hésitez pas à reporter vos erreurs.  
Il n'est pas compliqué d'utiliser ces programmes. Prenez le temps de bien lire chaque instruction.

## Prerequisites

Java			(https://www.java.com/fr/download/)  
Toolbox			(https://www.minecraft-smp.de/index.php/toolbox-2-0)  
Blender >2.8	(https://www.blender.org/)

## Instructions

### Edition des modèles .java

Déposez vos modèles .java dans le dossier "./import".  
Ouvrez le programme "JavaVehicleExtractor.jar".  
Patientez jusqu'à qu'une fenêtre vous avertissant de la fin se son exécution apparaisse.

### Passage des modèles .java en .obj

Ouvrez Toolbox.  
Pour tous les modèles dans  
	./export/body,   
	./export/steering,  
	./export/wheel.   
	Faites ceci:  
	
	-	Import > Model From Java > *Sélectionnez un modèle*.
	-	Import > Texture from File > *Sélectionnez la texture du modèle*.
	(Pour la roue, par exemple, vérifiez que le modèle ne contient que la roue de gauche. Si non, supprimez les parties en trop).
	-	Export > As .Obj Model (All Parts in 1 Mesh) (la dernière option) > *Sélectionnez le même répertoire que le .java (./export/...)*. 
	(Vous pouvez sauvegarder le fichier .blend (File > Save) pour enregistrer les chemins.

### Ajout des véhicules sur DynamX

Ouvrez "DynamXVehicle.blend" avec Blender.  
Allez sur le tab "Scripting" (en haut, vers le centre).  
Cliquez sur "Run Script" (icône de flèche).  
Allez sur le tab "Layout" (en haut).  
Appuyez sur "N".  
Allez sur le tap "DynamX Editor" (à l'envers, sur le côté de la nouvelle fenêtre apparue) :

	a. Pour générer un pack DynamX vide (si vous n'en avez pas déjà un) :
		-	Notez un nom de pack dans "Pack name".
		-	Sélectionnez un chemin dans "Pack path" (exemple : .minecraft/DynamX).
		-	Cliquez sur "Generate pack".
		
	b. Pour importer des véhicules :
		-	Dans "Import .obj path", sélectionnez le dossier "export" précédemment généré.
		-	Sélectionnez un chemin dans "Export .obj path" (exemple : .minecraft/DynamX/*nomDuPack*/assets/dynamxmod/models/obj).
		-	Sélectionnez un chemin dans "Export .dynx path" (exemple : .minecraft/DynamX/*nomDuPack*/vehicles).
		-	Notez un nom de pack dans "Pack name".
		-	Cliquez sur "Next vehicle" (un véhicule devrait apparaitre).
		-	Vous pouvez repositionner les roues et les sièges s'ils ne sont pas bien positionnés (ne touchez pas au volant !).
		-	Positionnez et redimensionnez la taille des boîtes de collision.
		-	Cliquez sur "Next vehicle" pour générer la configuration du véhicule et passer au prochain.
		Vous pouvez lancer votre jeu et conduire votre véhicule =)

## Auteurs

* **Pacito2** - *Travail initial* - [Pacito2](https://github.com/Pacito2)
* **Bravesonny** - *Modèle du Steve assis*
* **Équipe de DrawLife** - *Testeurs*