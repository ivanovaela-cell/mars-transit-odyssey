import base64

output = []
for name in ['vance', 'romanova', 'chen', 'reid']:
    path = f'D:/mars-transit-odyssey/assets/crew/{name}.jpg'
    with open(path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('ascii')
    output.append(f'{name.upper()}_B64 = "data:image/jpeg;base64,{b64}"\n')

with open('D:/mars-transit-odyssey/crew_b64.py', 'w', encoding='utf-8') as f:
    f.writelines(output)
print('crew_b64.py created successfully!')
