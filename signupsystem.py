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
      Fix the upcoming sheet by updating the sumif and adding -values to upcoming events
    """
    usersheet = self.worksheets["Users"]
    pastsheet = self.worksheets["Past"]
    upcomingsheet = self.worksheets["Upcoming"]
    users = usersheet.col_values(1)[1:]
    if not userID in users:
      #Starting index for inserting values
      si = 2+len(users)
      numevents = len(upcomingsheet.row_values(1))-1
      usersheet.insert_row([userID,numChars],si)
      pastsheet.insert_row([userID],si)
      upcomingsheet.insert_row([userID] + [-1] * numevents,si)
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
    length = len(upcoming.col_values(1))
    
    #If we only have 2 values we do not have any registered users as first and last entry is reserved
    if length <= 2:
      return False
    
    col = len(upcoming.row_values(1))
    #The letter for a range 
    letter = chr(65+col)

    #gspread dosent support insert column so we have to get the range of cells and update each cell
    cellrange = letter + '1:'+letter+str(length)

    cells = upcoming.range(cellrange)
    
    #Format of event is date, signup for each registered person and ending is a sumif for total chars available based on signups
    cells[0].value = "placeholder"

    for i in range(1,len(cells)-1):
      cells[i].value = -1

    #Need to create a sumif statement rangeing from 2:len-1
    #example: =sumif(B2:B5,=1,Users!B2:B5)
    sumif = "=sumif(" + letter + '2:' + letter + str(length-1) 
    sumif += ',"=1",'
    sumif += 'Users!B2:B' + str(length-1) + ')'

    cells[-1].value = sumif

    upcoming.update_cells(cells[:-1])
    #Update cells has a bug where it appends a ' to the front of a cell starting with = causing it to give a wrong statement
    upcoming.update_acell(letter+str(length),sumif)




def main():
  sheet = SignupSystem("19lDNiH55dpAJNG573fwxQvM3o3YmY-8M_8k8wDGkDD0")
  #sheet.unregister('ragnors')
  sheet.register('ragn',5)
  #sheet.create_event("tommorow")

if __name__ == '__main__':
  main()

