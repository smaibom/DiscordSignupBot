import gspread
from oauth2client import file, client, tools

class Spreadsheet(object):
  """docstring for Spreadsheet"""
  def __init__(self, sheetID):
    self.sheet = load_spreadsheet(sheetID)

  def add_worksheet(self,sheetName,srows = 40,scols = 50):
    """
    Adds a new worksheet to the spreadsheet object

    Args:
      sheetName(string): Name of the worksheet to be created
      srows(int): The number of rows the worksheet is initialized with
      scols(int): The number of columns the worksheet is initialized with

    Returns:
      worksheet. A worksheet object on success, None if worksheet name already exist or failed to be created
    """
    try:
      worksheet = self.sheet.add_worksheet(title=sheetName, rows=str(srows), cols=str(scols))
    except gspread.exceptions.APIError as e:
      worksheet = None
    return worksheet

  def get_worksheets(self):
    """
    Returns the worksheets in the spreadsheet
    """
    worksheets = self.sheet.worksheets()
    return worksheets

  def del_worksheet(self,worksheet):
    """
    Deletes a worksheet from the spreadsheet

    Args:
      worksheet(Worksheet): A gspread worksheet object to be deleted

    Returns:
      True on success, False if failed to be deleted or does not exist

    """
    try:
      self.sheet.del_worksheet(worksheet)
      return True
    except Exception as e:
      return False

  def append_col(self,colnum,worksheet):
    




def load_spreadsheet(sheetID):
  scope = 'https://www.googleapis.com/auth/spreadsheets'
  store = file.Storage('token.json')
  creds = store.get()
  if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', scope)
    creds = tools.run_flow(flow, store)
  gc = gspread.authorize(creds)
  return gc.open_by_key(sheetID)

