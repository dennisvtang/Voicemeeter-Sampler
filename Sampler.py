import os
from DataStructures import VoicemeeterMacroMap, Macrobutton
import re

# get path to default voicemeeter folder (where soundbytes are saved and where MacroButtonsConfig is saved)
voicemeeter_folder_path = os.path.expanduser("~\Documents\\Voicemeeter")

# get all soundbytes in voicemeeter folder
soundbytes = [f"{voicemeeter_folder_path}\\{file}" for file in os.listdir(voicemeeter_folder_path) if ".wav" in file]

# get last recorded soundbyte
latest_file = max(soundbytes, key=os.path.getctime)
print('latest file: ', latest_file)

config_file = VoicemeeterMacroMap()
config_file.macro_buttons = [[] for i in range(8)]
# load MacroButtonConfig file
voicemeeter_config_file = f"{voicemeeter_folder_path}\\MacroButtonConfig.xml"
with open(voicemeeter_config_file) as f:
    raw_data = "".join(f.readlines())
    
    # get xml_info
    xml_info = re.search(r"<\?xml (.*?)\?>", raw_data).group(1).replace(" ", ", ")
    xml_info = f"dict({xml_info})"
    xml_info = eval(xml_info)
    config_file.xml_info = xml_info

    # get MacroButtonConfiguration
    MacroButtonConfiguration = re.search(r"<MacroButtonConfiguration (.*?) />", raw_data).group(1).replace(" ", ", ")
    MacroButtonConfiguration = f"dict({MacroButtonConfiguration})"
    MacroButtonConfiguration = eval(MacroButtonConfiguration)
    config_file.MacroButtonConfiguration = MacroButtonConfiguration

