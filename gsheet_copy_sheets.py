from __future__ import print_function
import httplib2
import os
import time
from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from pprint import pprint

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                'version=v4')
service = discovery.build('sheets', 'v4', http=http,
                          discoveryServiceUrl=discoveryUrl)
###need to modify!!!
##append values
listname = ['Yoyo','Alice','Mango','Cindy']

for a in listname:
    spreadsheet_body = {'properties': {'title':'Created_by_api for {}'.format(a)}}

    request = service.spreadsheets().create(body=spreadsheet_body)
    response = request.execute()
    spreadsheet_id=response['spreadsheetId']
    #write sheetid in the first cell
    range_ = 'A1'  
    value_input_option = 'USER_ENTERED'  
    insert_data_option = 'OVERWRITE'  
    value_range_body = {
        'values': [
                    [spreadsheet_id]
                  ]
    }
    result = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body=value_range_body).execute()
    #copy to one sheet
    sheet_id = 0  # TODO: Update placeholder value.

    copy_sheet_to_another_spreadsheet_request_body = {
    # The ID of the spreadsheet to copy the sheet to.
    'destination_spreadsheet_id': '1UtnMFyf4gtLT9R-KQdox0Jaf5e55zOyS9E0VGu6e1e4',  # TODO: Update placeholder value.
    # TODO: Add desired entries to the request body.
    }

    request1 = service.spreadsheets().sheets().copyTo(spreadsheetId=spreadsheet_id, sheetId=sheet_id, body=copy_sheet_to_another_spreadsheet_request_body)
    response1 = request1.execute()

