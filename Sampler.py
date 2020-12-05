import os

# get path to default voicemeeter folder (where soundbytes are saved and where MacroButtonsConfig is saved)
voicemeeter_folder_path = os.path.expanduser("~\Documents\\Voicemeeter")

# get all soundbytes in voicemeeter folder
soundbytes = [f"{voicemeeter_folder_path}\\{file}" for file in os.listdir(voicemeeter_folder_path) if ".wav" in file]

# get last recorded soundbyte
latest_file = max(soundbytes, key=os.path.getctime)
print('latest file: ', latest_file)

