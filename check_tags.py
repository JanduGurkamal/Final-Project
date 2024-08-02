import json

file = open('intents.json', 'r')
file_contents = json.load(file)

print(file_contents[0])