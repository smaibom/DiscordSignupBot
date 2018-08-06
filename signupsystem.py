import numpy as np
import gspread
import gsheetsapi

class SignupSystem(object):
  """docstring for SignupSystem"""
  def __init__(self,sheetID):
    self.spreadsheet = gsheetsapi.Spreadsheet(sheetID)
    self.worksheets = dict()
    wsl = self.spreadsheet.get_worksheets()
    for ws in wsl:
      self.worksheets[ws.title] = ws
    

  def register(self, userID, numChars=1):
    """
    Register user to system

    Args:
      userID(string): Discord userID
      numChars(int): Number of chars to register, defaults to 1

    Returns:
      True on successfull registration, False if user exists

    TODO:
      Add changes to the signup sheet
    """
    usersheet = self.worksheets["Users"]
    pastsheet = self.worksheets["Past"]
    upcomingsheet = self.worksheets["Upcoming"]
    users = usersheet.col_values(1)[1:]
    if not userID in users:
      #Starting index for inserting values
      si = 2+len(users)
      usersheet.insert_row([userID,numChars],si)
      pastsheet.insert_row([userID],si)
      upcomingsheet.insert_row([userID],si)
      return True
    else:
      return False

  def unregister(self,userID):
    """
    Removes user from system

    Args:
      userID(string): Discord userID

    Returns:
      True on successfull removal, False if userID does not exist

    TODO:
      Add changes to the signup sheet
    """
    usersheet = self.worksheets["Users"]
    pastsheet = self.worksheets["Past"]
    upcomingsheet = self.worksheets["Upcoming"]
    try:
      cell = usersheet.find(userID)
      usersheet.delete_row(cell.row)
      pastsheet.delete_row(cell.row)
      upcomingsheet.delete_row(cell.row)
      return True
    except gspread.exceptions.CellNotFound:
      return False


  def update_num_chars(self,userID,numChars):
    """
    Updates the number of chars registrated to a userID

    Args:
      userID(string): Discord userID
      numChars(int): The new number of chars

    Returns:
      True on successfull update, False if userID does not exists
    """
    try:
      cell = self.worksheets["Users"].find(userID)
      self.worksheets["Users"].update_cell(cell.row,2,numChars)
      return True
    except gspread.exceptions.CellNotFound:
      return False

  def get_num_chars(self,userID):
    """
    Gets the number of chars of a user

    Args:
      userID(string): Discord userID

    Returns:
      The number of chars, -1 if userID is not registered
    """
    try:
      cell = self.worksheets["Users"].find(userID)
      val = self.worksheets["Users"].cell(cell.row,2)
      return val
    except gspread.exceptions.CellNotFound:
      return -1

  def create_event(self,date):
    """
    """
    upcoming = self.worksheets["Upcoming"]
    col = len(upcoming.row_values(1))
    users = len(upcoming.col_values(1))-1
    letter = chr(65+col)
        # [date,-1 for each user, sum field]
    #Creates a sumif statement over the users 
    sumstring = '=sumif(' + letter+ '2:' + letter+str(users)+',"=1,Users!B2:B' + str(users) + ')'  
    vals = [date] + [-1]*(users-1) + [sumstring]
    upcoming.insert_col(vals,col)



def main():
  sheet = SignupSystem("19lDNiH55dpAJNG573fwxQvM3o3YmY-8M_8k8wDGkDD0")
  sheet.create_event("tommorow")

if __name__ == '__main__':
  main()