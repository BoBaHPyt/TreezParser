#1FS_5-Q4fMCBDGKGoGCQ3MsEYlHCOwmLtTUmkIdvQ66A
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]
crenditals = ServiceAccountCredentials.from_json_keyfile_name("gapi.json", scope)
client = gspread.authorize(crenditals)

client.open_by_key()
sheet = client.open("https://docs.google.com/spreadsheets/d/1FS_5-Q4fMCBDGKGoGCQ3MsEYlHCOwmLtTUmkIdvQ66A/")
#service-account@curious-mender-235409.iam.gserviceaccount.com
worksheet = sheet.get_worksheet("Парсер остатков с сайта")
sheet.worksheet()
print(worksheet.get_all_values())
