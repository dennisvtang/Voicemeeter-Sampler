from dataclasses import dataclass

@dataclass
class VoicemeeterMacroMap():
    xml_info:dict = None
    macro_button_config:dict = None
    macro_buttons:list = None

@dataclass
class Macrobutton:
    mb_midi:dict
    mb_trigger:dict
    mb_xinput:dict
    mb_name:str
    mb_subname:str
    mb_init_request:str
    mb_on_request:str
    mb_off_request:str