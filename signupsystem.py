import numpy as np
import gsheetsapi

class SignupSystem(object):
  """docstring for SignupSystem"""
  def __init__(self,sheetID):
    self.spreadsheet = gsheetsapi.Spreadsheet(sheetID)
    self.worksheets = dict()
    wsl = self.spreadsheet.get_worksheets()
    for ws in wsl:
      self.worksheets[ws.title] = wsl
    print(self.worksheets)
    

  def register(self, userID, chars=[]):
    """
    Register user to system
    userID is discord user name
    chars is charecters registered to user, defaults to empty array if no parameter is passed
    returns true if user is registered to system, false if user already exist
    """
    if userID in self.users:
      return False
    else:
      chars = np.unique(chars)
      self.users[userID] = (len(chars),chars)
      self.spreadsheet
      return True

  def add_chars_to_user(self,userID,chars):
    """
    Adds chars to registered userID, duplicates will not be added
    userID is discord user name
    Returns true if userID exist and chars are added, false if userID is not registered
    """
    if userID in self.users:
      self.users[userID] = np.unique(self.users[userID]+chars)
      return True
    else:
      return False

  def remove_char_from_user(self,userID,chars):
    """
    Removes chars from userID, only removes chars which are registered to user already
    userID is discord user name
    Returns (True,[removed chars]) if userID exit, False otherwise
    """
    if userID in self.users:
      arr = self.users[userID]
      interArr = np.intersect1d(arr,chars)
      self.users[userID] = np.delete(arr,chars)
      return (True,interArr)
    else:
      return False

  def get_user_chars(self,userID):
    """
    Gets the charecters of a given userID
    userID is discord user name
    Returns an array of names if userID exists, None otherwise
    """
    if userID in self.users:
      return self.users[userID]
    else:
      return None

def main():
  sheet = SignupSystem("19lDNiH55dpAJNG573fwxQvM3o3YmY-8M_8k8wDGkDD0")

if __name__ == '__main__':
  main()