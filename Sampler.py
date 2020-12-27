import os, sys
from DataStructures import VoicemeeterMacroMap, Macrobutton
import re
import typing


def load_voicemeeter_macro_config(config_path:str):
    '''Loads voicemeeter macro button config at given path and returns it as a VoicemeeterMacroMap object'''
    
    # create VoicemeeterMacroMap object to store all data
    config_file = VoicemeeterMacroMap(config_path)
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
    # add try block because sometimes the / at the end disappears
    try:
        macro_button_config = re.search(r"<MacroButtonConfiguration (.*?) />", raw_data).group(1).replace(" ", ", ")
    except:
        macro_button_config = re.search(r"<MacroButtonConfiguration (.*?) >", raw_data).group(1).replace(" ", ", ")
    macro_button_config = f"dict({macro_button_config})"
    macro_button_config = eval(macro_button_config)
    config_file.macro_button_config = macro_button_config

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
            row_of_buttons.append(button)

    config_file.macro_buttons.append(row_of_buttons)
    return config_file


def get_all_loaded_soundbytes(config_file) -> typing.List[str]:
    '''Returns a list of all soundbytes that are currently loaded by sampler'''
    in_use = []

    # loop through all buttons
    for row in config_file.macro_buttons:
        for button in row:
            # button is a sampler play soundbyte button
            if "Recorder.Load" in button.mb_on_request:
                in_use.append(re.search(r" \"(.*?)\"", button.mb_on_request).group(1))

    return in_use


if __name__ == "__main__":
    # get button indexes from command line arguments
    row = int(sys.argv[1])
    col = int(sys.argv[2])

    # get path to default voicemeeter folder (where soundbytes are saved and where MacroButtonsConfig is saved)
    voicemeeter_folder_path = os.path.expanduser("~\OneDrive\Documents\\Voicemeeter")
    # add check for if documents are saved in OneDrive folder
    if os.path.exists(voicemeeter_folder_path) == False:
        voicemeeter_folder_path = os.path.expanduser("~\Documents\\Voicemeeter")

    # get all soundbytes in voicemeeter folder
    soundbytes = set([f"{voicemeeter_folder_path}\\{file}" for file in os.listdir(voicemeeter_folder_path) if ".wav" in file])

    # get last recorded soundbyte
    latest_file = max(soundbytes, key=os.path.getctime)

    # load MacroButtonConfig file
    config_path = f"{voicemeeter_folder_path}\\MacroButtonConfig.xml"
    config_file = load_voicemeeter_macro_config(config_path)

    # remove oldest soundbyte after 8 currently loaded and a buffer for 10
    if len(soundbytes) >= 19:
        # retrieve list of soundbytes in use
        in_use = set(get_all_loaded_soundbytes(config_file))

        # retrieve list of soundbytes not in use
        not_in_use = sorted(list(soundbytes - in_use))

        # delete soundbytes until theres only 18 in the folder
        num_to_delete = len(soundbytes) - 18
        for _ in range(num_to_delete):
            # remove oldest soundbyte
            os.remove(not_in_use.pop(0))


    config_file.update_soundbyte(row, col, latest_file)
    config_file.save_file()