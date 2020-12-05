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
config_file.macro_buttons = []
# load MacroButtonConfig file
voicemeeter_config_file = f"{voicemeeter_folder_path}\\MacroButtonConfig.xml"
with open(voicemeeter_config_file) as f:
    raw_data = "".join(f.readlines())

def load_voicemeeter_macro_config(config_path:str):
    '''Loads voicemeeter macro button config at given path and returns it as a VoicemeeterMacroMap object'''
    
    # create VoicemeeterMacroMap object to store all data
    config_file = VoicemeeterMacroMap()
    config_file.macro_buttons = []

    # load raw string from xml file
    with open(config_path) as f:
        raw_data = "".join(f.readlines())
        
    # parse xml_info
    xml_info = re.search(r"<\?xml (.*?)\?>", raw_data).group(1).replace(" ", ", ")
    xml_info = f"dict({xml_info})"
    xml_info = eval(xml_info)
    config_file.xml_info = xml_info

    # parse MacroButtonConfiguration
    MacroButtonConfiguration = re.search(r"<MacroButtonConfiguration (.*?) />", raw_data).group(1).replace(" ", ", ")
    MacroButtonConfiguration = f"dict({MacroButtonConfiguration})"
    MacroButtonConfiguration = eval(MacroButtonConfiguration)
    config_file.MacroButtonConfiguration = MacroButtonConfiguration

    # parse MacroButtons
    all_macro_buttons = re.findall(r"<MacroButton (.*?)</MacroButton>", raw_data, re.DOTALL|re.MULTILINE)
    # process each MacroButton
    row_of_buttons = []
    for mb in all_macro_buttons:
        # parse macro_button_info
        macro_button_info = mb[:mb.find(">")].replace(" ", ", ")
        macro_button_info = f"dict({macro_button_info})"
        macro_button_info = eval(macro_button_info)

        # parse mb_midi
        mb_midi = re.search(r"<MB_MIDI (.*?) />", mb).group(1).replace(" ", ", ")
        mb_midi = f"dict({mb_midi})"
        mb_midi = eval(mb_midi)

        # parse mb_trigger
        mb_trigger = re.search(r"<MB_TRIGGER (.*?) />", mb).group(1).replace(" ", ", ")
        mb_trigger = f"dict({mb_trigger})"
        mb_trigger = eval(mb_trigger)
        
        # parse mb_xinput
        mb_xinput = re.search(r"<MB_XINPUT (.*?) />", mb).group(1).replace(" ", ", ")
        mb_xinput = f"dict({mb_xinput})"
        mb_xinput = eval(mb_xinput)
        
        # parse mb_name
        mb_name = re.search(r"<MB_Name>(.*?)</MB_Name>", mb).group(1)

        # parse mb_subname
        mb_subname = re.search(r"<MB_Subname>(.*?)</", mb).group(1)
        
        # parse mb_init_request
        mb_init_request = re.search(r"<MB_InitRequest>(.*?)</", mb, re.DOTALL|re.MULTILINE).group(1)
        
        # parse mb_on_request
        mb_on_request = re.search(r"<MB_OnRequest>(.*?)</", mb, re.DOTALL|re.MULTILINE).group(1)
        
        # parse mb_off_request
        mb_off_request = re.search(r"<MB_OffRequest>(.*?)</", mb, re.DOTALL|re.MULTILINE).group(1)

        # encapsulate MacroButton
        button = Macrobutton(macro_button_info, mb_midi, mb_trigger, mb_xinput, mb_name, mb_subname, mb_init_request, mb_on_request, mb_off_request)
        
        # convert button index into 2D array indexing
        if len(row_of_buttons) <= 9:
            row_of_buttons.append(button)
        else:
            config_file.macro_buttons.append(row_of_buttons)
            row_of_buttons = []
    
    return config_file

