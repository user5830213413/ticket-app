import requests

# """access
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNzA0MzgzMzEzLCJqdGkiOiJiMjVmZjJkMi0xYTBhLTQ1NzItYjBhMC1mMzkwNzFiM2RiNWUiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoxLCJuYmYiOjE3MDQzODMzMTMsImNzcmYiOiJjZTkwMDI0Ni01MjlhLTQ0YWItYTRhMi01ZWQ1NjQwODI1YzciLCJleHAiOjE3MDQzODQyMTN9.RcJLy-y3ArtgLKTXgsZoLed1_gkMy-hMudiYFcTA_J8
# """

# """refresh
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDM4MzMxMywianRpIjoiOTRkZDhiMGQtMWMwMy00NTQ0LWI0ZmQtZTNlZDVlNjhkODVmIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOjEsIm5iZiI6MTcwNDM4MzMxMywiY3NyZiI6ImM1N2JlZGM0LTk5OGMtNGRmOS05YjBmLTIxMWQyYzQxZDRjYyIsImV4cCI6MTcwNjk3NTMxM30.GMpQHKtHPElEc0tW9rUoLw8xPCb1N-YztRjbUrZtZB8"""

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNzA0NDUzOTQyLCJqdGkiOiJhMzFlZjllZS1jZGJjLTRkNGItOGRmMC03ZDIzOTU1ZDQ4NGQiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoxLCJuYmYiOjE3MDQ0NTM5NDIsImNzcmYiOiJkOTA5NjQzNy01NmYyLTRlZGMtYjliNi1hZWM0NDQ5ZDkzZGMiLCJleHAiOjE3MDQ0NTQ4NDJ9.49ghBhbxKfqv2OIN76TP6GDA-_zf2igPxqSmK3-UUWc"

# data = {
#     'username': 'andrey',
#     'password': '12345556!',
#     'balance': 200.20
# }

data = {
    'ticket_key': 234,
}

headers = {
    # 'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

response = requests.post('http://127.0.0.1:5000/ticket/winner')

print(response.json())
# import json

# array = [('{"ticket": [234]}',), ('{"ticket": [502]}',)]

# test = [json.loads(x[0])['ticket'][0] for x in array]

# array = [[500], [700, 300, 400]]
# results = {}

# found = any(300 in x for x in array)

# print(found)



# print(test)