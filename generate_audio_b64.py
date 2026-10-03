import base64
import os

mp3_path = r'D:\mars-transit-odyssey\assets\audio\main_theme.mp3'
out_path = r'D:\mars-transit-odyssey\audio_b64.py'

if os.path.exists(mp3_path):
    with open(mp3_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode('utf-8')
    data_uri = f'data:audio/mp3;base64,{b64}'
    with open(out_path, 'w', encoding='utf-8') as out:
        out.write(f'MAIN_THEME_B64 = "{data_uri}"\n')
    print("audio_b64.py created successfully. Length:", len(data_uri))
else:
    print("Error: mp3 file not found at", mp3_path)
