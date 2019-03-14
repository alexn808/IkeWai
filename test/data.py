import json
reading = {'is_claimed': 'True', 'rating': 3.45}
reading = json.dumps(reading)
loaded_r = json.loads(reading)
loaded_r['rating'] #Output 3.5,
type(reading) #Output str
type(loaded_r) #Output dict
print loaded_r
print(reading)
sample = [{'ObjectInterpolator': 1629,  'PointInterpolator': 1675, 'RectangleInterpolator': 2042},
{'ObjectInterpolator': 1629, 'PointInterpolator': 1675, 'RectangleInterpolator': 2042}]
json = json.dumps(sample)
f = open("import.json","w")
f.write(json)
f.close()
