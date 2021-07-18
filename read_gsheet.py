from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE='keys.json'

def read_sheet(SCOPES, SERVICE_ACCOUNT_FILE, RANGE):
    creds = None
    creds = service_account.Credentials.from_service_account_file(\
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
           
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID='1-vkyd27C-dIk5ecHJ102iQhZtDg3Oh7d-hhL10znChk'
    
    service = build('sheets', 'v4', credentials=creds)
    
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=RANGE).execute()
    values = result.get('values', [])
    return values
