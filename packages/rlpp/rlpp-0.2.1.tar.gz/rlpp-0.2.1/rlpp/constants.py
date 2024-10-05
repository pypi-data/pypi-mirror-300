import pygame 
import numpy as np 
from PyQt5.QtGui import QImage
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget, QFileDialog,QMessageBox,QShortcut
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap, QKeySequence
import os
from os.path import join as jn
import cv2
import sys
import json 

RES = 32 #resolution of reference from the resouces folder
dir_location = os.path.dirname(__file__)
RESOURCES_PATH = jn(dir_location,f"resources/res_{RES}")
SCREEN = (640,480)
pygame_surface = pygame.Surface(SCREEN)  # Pygame rendering surface)

# cursor settings
cursor_settings = {"POS":(0,0),"MODE":"", "INDISPLAY":False}


# DD. GAME_OBJECT
# gameObject = GameObject()
# interp. a game object in the editor with:
# - position x and y in the screen, where coordinate is the center of the object
# - image loaded in pygame
# - object_type: agent, wall, enemy, food
class GameObject():
    def __init__(self,object_type, img_path):
        self.placed = False #stops following cursor once it's placed
        self.object_type = object_type
        self.image_path = img_path
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()
        self.angle = 0

        
    def draw(self):
        pygame_surface.blit(self.image, self.rect)
        if self == objectManager.current_go:
            pygame.draw.rect(pygame_surface,"green",self.rect,1)
        
    def update_pos(self):
        if not self.placed:
            self.rect.center = cursor_settings["POS"]

    def turnClockwise(self, degrees=90):
        # Preserve the current center position of the rectangle
        self.angle = (self.angle + degrees)%360
        previous_center = tuple(self.rect.center)
        # Rotate the image
        self.image = pygame.transform.rotate(self.image, -degrees)  # Use -self.angle for clockwise rotation
        self.rect = self.image.get_rect(center=previous_center)  # Reassign the rect with the updated center
    
    def to_dict(self):
        d = {"position":self.rect.center,
             "angle":self.angle,
             "img_path":self.image_path,
             "object_type":self.object_type
             }
        return d
        
# Objects display manager allows mainUI and main to access the collection of objects that are being placed within the screen
# DD. DesignerObjectManager()
# gm = DesignerObjectManager()
# interp. an object to track the parameters and objects placed in the designer by the player
class DesignerObjectManager():
    def __init__(self):
        self.walls = []
        self.agents = []
        self.foods = []
        self.enemies = []
        self.list_names = ["walls","agents","foods","enemies"]
        self.gameObjects = [self.walls ,self.agents ,self.foods ,self.enemies]
        self.current_go = None
        
    def updateGameObjects(self):
        for logo in self.gameObjects:
            for go in logo:
                go.draw()
    
    
    def update_pygame(self, qlabel):
        # Render Pygame content (for example, a red circle moving across the screen)
        pygame_surface.fill((30, 30, 30))  # Clear screen
        # UPDATE THE GAMEOBJECTS IN THE MANAGER
        self.updateGameObjects()
        if self.current_go is not None:
            self.current_go.update_pos()
            self.current_go.draw()
        
        # pygame.draw.circle(pygame_surface, (255, 0, 0), cursor_settings["POS"], 50)
        # Convert Pygame surface to an image that PyQt can display
        self.display_pygame_on_qt(qlabel)

    def display_pygame_on_qt(self, qlabel):
        # Get the Pygame surface as a 3D array (RGB format)
        raw_image = pygame.surfarray.array3d(pygame_surface)
        # Convert from (width, height, color) to (height, width, color)
        raw_image = np.transpose(raw_image, (1, 0, 2))

        # Convert the image to a format suitable for PyQt5 (QImage)
        height, width, channel = raw_image.shape
        bytes_per_line = 3 * width
        qt_image = QImage(raw_image.tobytes(), width, height, bytes_per_line, QImage.Format_RGB888)

        # Set the QPixmap to the QLabel to display it
        qlabel.setPixmap(QPixmap.fromImage(qt_image))
    
    def create_new_gameObject(self,img_path,object_type, reset_mode=False):
        cursor_settings["MODE"] = "" if reset_mode else cursor_settings["MODE"]
        if object_type == "agent":
            gameObject = GameObject("agent",img_path)
            self.current_go = gameObject
            # self.agents.append(gameObject)
        elif object_type == "wall":
            gameObject = GameObject("wall",img_path)
            self.current_go = gameObject
            # self.walls.append(gameObject)
        elif object_type == "enemy":
            gameObject = GameObject("enemy",img_path)
            self.current_go = gameObject
            # self.enemies.append(gameObject)
        elif object_type == "food":
            gameObject = GameObject("food",img_path)
            self.current_go = gameObject
            # self.foods.append(gameObject)
            
    def processCurrentObject(self):
        if self.current_go.object_type == "agent":
            self.agents.append(self.current_go)
        elif self.current_go.object_type == "wall":
            self.walls.append(self.current_go)
        elif self.current_go.object_type == "enemy":
            self.enemies.append(self.current_go)
        elif self.current_go.object_type == "food":
            self.foods.append(self.current_go)
        self.current_go.placed = True
        
        # Control the behavior of the STAMP tool
        if not cursor_settings["MODE"] == "STAMP":
            self.current_go = None
        else:
            angle_reference = self.current_go.angle
            self.create_new_gameObject(self.current_go.image_path,self.current_go.object_type)
            self.current_go.turnClockwise(angle_reference)
        
    def getObjectClicked(self):
        '''Iterate over all the elements in the game to find that which overlaps the cursor '''
        for logo in self.gameObjects:
            for go in logo:
                if go.rect.collidepoint(cursor_settings["POS"]):
                    self.current_go = go 
                    break
            
    def remove_current_gameObject(self):
        for logo in self.gameObjects:
            for go in logo:
                if go == self.current_go:
                    self.current_go = None
                    cursor_settings["MODE"] = "SELECT"
                    logo.remove(go)
                    return 
    
    def export_JSON(self):
        config = {list_name:[go.to_dict() for go in self.gameObjects[idx]] for idx, list_name in enumerate(self.list_names)}
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(None, "Save File", "", "JSON Files (*.json);;All Files (*)", options=options)
                
        if fileName:
            if not fileName.endswith('.json'):
                fileName += '.json'
            with open(f"{fileName}","w") as jsonfile:
                json.dump(config, jsonfile, indent=4)  # Use json.dump to write the dictionary to the file
            QMessageBox.information(None, "File Selected", f"File will be saved as: {fileName}")

objectManager = DesignerObjectManager()