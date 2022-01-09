import requests
import json
import math
import smtplib
# Import the email modules we'll need
from email.message import EmailMessage


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1000)))
   p = math.pow(1000, i)
   s = round(size_bytes / p, 2)
   return "{} {}".format(s, size_name[i])

# Define part 
endpoint = 'https://<StraogeGrid Portal>/api/v3'

# Email
msg = EmailMessage()
msg['Subject'] = 'StorageGrid Usage'
msg['From'] = "<From Adress>"
msg['To'] = "<To Adress>"


# Auth Section
AuthDict = {
    "accountId": "<AccountID>",
    "username": "<username>",
    "password": "<Password>",
    "cookie": True,
    "csrfToken": False
}
jsonData = json.dumps(AuthDict)
response = requests.post(endpoint+"/authorize", json=AuthDict)
response_json = response.json()
Authtoken = response_json['data']
print("Status code: ", response.status_code)
print("Status: {}, AuthToken: {}".format(response_json['status'],Authtoken))
print()

# DataUsage Section
headers = {"Authorization": "Bearer "+Authtoken}
response = requests.get(endpoint+"/org/usage", headers=headers)
response_json = response.json()
datausage = convert_size(response_json['data']["dataBytes"])

print("Status: {}, data usage: {}".format(response_json['status'],response_json['data']["dataBytes"]))

# Get Limit
response = requests.get(endpoint+"/org/config", headers=headers)
response_json = response.json()
qouta = convert_size(response_json['data']["account"]['policy']["quotaObjectBytes"])

print("Status: {}, Qouta: {}".format(response_json['status'],response_json['data']["account"]['policy']["quotaObjectBytes"]))



#Logout
response = requests.delete(endpoint+"/authorize", headers=headers)
if response.status_code == 204:
    LogOff = "Succes"
else:
    LogOff = "Failed"

print("Logout: {}".format(LogOff))


# Print relevant data 
msg.set_content("Usage {}, Limit {}".format(datausage,qouta))
print("Usage {}, Limit {}".format(datausage,qouta))

s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()
