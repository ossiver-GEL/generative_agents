"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: spatial_memory.py
Description: Defines the MemoryTree class that serves as the agents' spatial
memory that aids in grounding their behavior in the game world. 
"""
import json
import sys

from utils import *
from global_methods import *

class MemoryTree: 
  def __init__(self, f_saved): 
    self.tree = {}
    if check_if_file_exists(f_saved): 
      self.tree = json.load(open(f_saved))


  def print_tree(self): 
    def _print_tree(tree, depth):
      dash = " >" * depth
      if type(tree) == type(list()): 
        if tree:
          print (dash, tree)
        return 

      for key, val in tree.items(): 
        if key: 
          print (dash, key)
        _print_tree(val, depth+1)
    
    _print_tree(self.tree, 0)
    

  def save(self, out_json):
    with open(out_json, "w") as outfile:
      json.dump(self.tree, outfile) 



  def get_str_accessible_sectors(self, curr_world): 
    """
    Returns a summary string of all the arenas that the persona can access 
    within the current sector. 

    Note that there are places a given persona cannot enter. This information
    is provided in the persona sheet. We account for this in this function. 

    INPUT
      None
    OUTPUT 
      A summary string of all the arenas that the persona can access. 
    EXAMPLE STR OUTPUT
      "bedroom, kitchen, dining room, office, bathroom"
    """
    x = ", ".join(list(self.tree[curr_world].keys()))
    return x


  def get_str_accessible_sector_arenas(self, sector): 
    """
    Returns a summary string of all the arenas that the persona can access 
    within the current sector. 

    Note that there are places a given persona cannot enter. This information
    is provided in the persona sheet. We account for this in this function. 

    INPUT
      None
    OUTPUT 
      A summary string of all the arenas that the persona can access. 
    EXAMPLE STR OUTPUT
      "bedroom, kitchen, dining room, office, bathroom"
    """
    curr_parts = sector.split(":")
    
    # Handle different address formats: world:sector or longer formats
    if len(curr_parts) < 2:
      return ""
    
    curr_world = curr_parts[0]
    curr_sector = curr_parts[1]  # Only take the first 2 parts
    
    if not curr_sector: 
      return ""
    
    # Clean up sector name by removing any formatting characters
    curr_sector = curr_sector.strip()
    if curr_sector.startswith("{"):
      curr_sector = curr_sector[1:]
    if curr_sector.endswith("}"):
      curr_sector = curr_sector[:-1]
    curr_sector = curr_sector.strip()
    
    try:
      x = ", ".join(list(self.tree[curr_world][curr_sector].keys()))
    except KeyError:
      # If sector is not found, return empty string
      return ""
    return x


  def get_str_accessible_arena_game_objects(self, arena):
    """
    Get a str list of all accessible game objects that are in the arena. If 
    temp_address is specified, we return the objects that are available in
    that arena, and if not, we return the objects that are in the arena our
    persona is currently in. 

    INPUT
      temp_address: optional arena address
    OUTPUT 
      str list of all accessible game objects in the gmae arena. 
    EXAMPLE STR OUTPUT
      "phone, charger, bed, nightstand"
    """
    curr_parts = arena.split(":")
    
    # Handle different address formats: world:sector:arena or world:sector:arena:object
    if len(curr_parts) < 3:
      return ""
    
    curr_world = curr_parts[0]
    curr_sector = curr_parts[1]
    curr_arena = curr_parts[2]  # Only take the first 3 parts for arena access

    if not curr_arena: 
      return ""

    # Clean up arena name by removing any formatting characters
    curr_arena = curr_arena.strip()
    if curr_arena.startswith("{"):
      curr_arena = curr_arena[1:]
    if curr_arena.endswith("}"):
      curr_arena = curr_arena[:-1]
    curr_arena = curr_arena.strip()

    try: 
      x = ", ".join(list(self.tree[curr_world][curr_sector][curr_arena]))
    except KeyError: 
      try:
        x = ", ".join(list(self.tree[curr_world][curr_sector][curr_arena.lower()]))
      except KeyError:
        # If arena is not found, return empty string
        return ""
    return x


if __name__ == '__main__':
  x = f"../../../../environment/frontend_server/storage/the_ville_base_LinFamily/personas/Eddy Lin/bootstrap_memory/spatial_memory.json"
  x = MemoryTree(x)
  x.print_tree()

  print (x.get_str_accessible_sector_arenas("dolores double studio:double studio"))







