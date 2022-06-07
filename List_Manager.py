"""
@author: Jibril Mohamed
"""
from typing import  List

class ListManager:
  def __init__(self) -> None:
    self.myList = []
  
  def add_new_item(self, item: str) -> None:
    self.myList.append(item)
  
  def display_all_items(self) -> List[str]:
    return self.myList
  
  def delete_item(self, index: int) -> None:
    if index == -1:
      raise ValueError
    else:
      self.myList.pop(index)
      print(f"item at index: {index} is deleted")
  
  def replace_item(self, index: int, new_item: str) -> None:
    self.myList.pop(index)
    self.myList.insert(index, new_item)
  
  def count(self):
    return len(self.myList)
    
  def display_valid_commands(self):
    print("===============================================")
    print("== ** Here is the list of valid Commands ** ===")
    print("=============== help ==========================")
    print("=============== add, <item> ===================")
    print("=============== list ==========================")
    print("=============== replace, <index>, <new item> ==")
    print("=============== delete, <index>: `0 indexed` ==")
    print("=============== exit ==========================")
    print("===============================================")
    
    
	  