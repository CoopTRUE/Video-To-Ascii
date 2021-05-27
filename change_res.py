from json import load, dump

with open('settings.json', 'r') as f:
	json_data = load(f)

print("Current height:", json_data['height'])
height_input = input("New height: ")
json_data['height'] = int(height_input)

with open('settings.json', 'w') as f:
	dump(json_data, f)