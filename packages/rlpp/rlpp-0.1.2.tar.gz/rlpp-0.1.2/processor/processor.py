import pygame 
import os 
import json 
from os.path import join as jn
"""Read a config.json file and map it into a pygame.py file"""

def map_json(path):
    def read_json_file(file_path):
        # Open the JSON file and load its contents
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        return data

    object_lists = read_json_file(path)
    text_for_template = ""
    tab = "    "
    list_collection = [] #at the end, all lists will be nested within a main list_of_game_objects
    # each key represents a list
    for key in object_lists.keys():
        _str = f"{tab}{tab}self.{key}=[]\n"
        list_collection.append(f"self.{key}") #add this list name to the collection
        for idx,go in enumerate(object_lists[key]):
            _str += f"{tab}{tab}go_{key}_{idx} = GameObject({go['position']},{go['angle']},\"{go['object_type']}\",r\"{go['img_path']}\");self.{key}.append(go_{key}_{idx})\n"
        text_for_template += _str
    text_for_template += f'{tab}{tab}self.all_game_objects = ({",".join(list_collection)})\n'
    with open("./template.txt",'r') as file:
        file = file.read()
    
    with open(jn(os.path.split(path)[0],"output.py"),"w") as py_file:
        file = file.replace("<<embed_game_objects>>",text_for_template)
        py_file.write(file)
    
map_json(r"C:\Users\Uriel\Desktop\test.json")