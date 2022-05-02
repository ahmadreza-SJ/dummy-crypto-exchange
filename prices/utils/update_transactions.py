import json

def update_transactions(ws, message):
    data = json.loads(message)
    print(data)