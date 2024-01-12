from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
spreadsheet_id = '1dLPQXepIssZmKrY31SR3rNHarWQF6OhjPGZ0_5ziEnI'
range_name_all = 'ЗАЯВКИ'
range_name_promo = 'Промокоди'
range_name_user = 'користувачі'
range_name_log = 'Логи'

sheet = service.spreadsheets()

# values = [['Значение', 'Значение321313'], ['Значение2']]
# body = {'values': values}

folder_id = '1bkJV0B_p_v9sC681h0mG03prLzwh78tG'
file_path = 'clients.db'  # путь к файлу на локальной машине


# def add_googleDrive():
#     time = datetime.now().date()
#     time = time.strftime("%d.%m.%Y, %H:%M")
#     file_metadata = {
#         'name': time,
#         'parents': [folder_id]}
#
#     media = MediaFileUpload(file_path, resumable=True)
#     file = build('drive', 'v3', credentials=credentials).files().create(
#         body=file_metadata,
#         media_body=media,
#         fields='id'
#     ).execute()


def log_sheets(values1):
    try:
        request = service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id, range=range_name_log, body={})
        response = request.execute()

        values = values1
        body = {'values': values}
        result = sheet.values().update(
            spreadsheetId=spreadsheet_id, range=range_name_log, valueInputOption='RAW', body=body).execute()
        return True

    except Exception as ex:
        print(ex)
        return False


def user_info_sheets(values1):
    try:
        request = service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id, range=f'{range_name_user}!A1:Z', body={})
        response = request.execute()

        values = values1
        body = {'values': values}
        result = sheet.values().update(
            spreadsheetId=spreadsheet_id, range=range_name_user, valueInputOption='RAW', body=body).execute()
        return True

    except Exception as ex:
        print(ex)
        return False


def status_info_sheets(values1):
    try:
        request = service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id, range=f'{range_name_all}!A1:Z', body={})
        response = request.execute()
        if values1:
            values = values1
            body = {'values': values}
            result = sheet.values().update(
                spreadsheetId=spreadsheet_id, range=range_name_all, valueInputOption='RAW', body=body).execute()
            return True
        else:
            return False

    except Exception as ex:
        print(ex)
        return False


def promo_info_sheets(values1):
    try:
        request = service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id, range=f'{range_name_all}!A1:Z', body={})
        response = request.execute()
        if values1:
            values = values1
            body = {'values': values}
            result = sheet.values().update(
                spreadsheetId=spreadsheet_id, range=range_name_promo, valueInputOption='RAW', body=body).execute()
            return True
        else:
            return False

    except Exception as ex:
        print(ex)
        return False