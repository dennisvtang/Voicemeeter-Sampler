from dataclasses import dataclass

@dataclass
class VoicemeeterMacroMap():
    config_path:str
    xml_info:dict = None
    macro_button_config:dict = None
    macro_buttons:list = None

    def update_soundbyte(self, row:int, col:int, new_soundbyte:str):
        self.macro_buttons[row][col].mb_on_request = f'Recorder.Load = "{new_soundbyte}"'

    def save_file(self):
        with open(self.config_path, 'w') as f:
            # write xml_info
            f.write(f"<?xml")
            for key, value in self.xml_info.items():
                f.write(f' {key}="{value}"')
            f.write(f"?>")
            f.write(f"\n")

            # write MacroButtonMap boilerplate stuff
            f.write('<VBAudioVoicemeeterMacroButtonMap>')
            f.write(f"\n")

            # write macro_pad_config
            f.write('<MacroButtonConfiguration')
            for key, value in self.macro_button_config.items():
                f.write(f" {key}='{value}'")
            f.write(' />')
            f.write(f"\n")

            # write all MacroButtons
            for row_of_buttons in self.macro_buttons:
                for button in row_of_buttons:
                    # write macro_button_info
                    f.write('\t<MacroButton')
                    for key, value in button.macro_button_info.items():
                        f.write(f" {key}='{value}'")
                    f.write('>')
                    f.write(f"\n")
                    
                    # write mb_midi
                    f.write('\t\t<MB_MIDI')
                    for key, value in button.mb_midi.items():
                        f.write(f" {key}='{value}'")
                    f.write(' />')
                    f.write(f"\n")

                    # write mb_trigger
                    f.write('\t\t<MB_TRIGGER')
                    for key, value in button.mb_trigger.items():
                        f.write(f" {key}='{value}'")
                    f.write(' />')
                    f.write(f"\n")
                    
                    # write mb_xinput
                    f.write('\t\t<MB_XINPUT')
                    for key, value in button.mb_xinput.items():
                        f.write(f" {key}='{value}'")
                    f.write(' />')
                    f.write(f"\n")

                    # write mb_name
                    f.write('\t\t<MB_Name>')
                    f.write(f"{button.mb_name}")
                    f.write('</MB_Name>')
                    f.write(f"\n")

                    # write mb_subname
                    f.write('\t\t<MB_Subname>')
                    f.write(f"{button.mb_subname}")
                    f.write('</MB_Subname>')
                    f.write(f"\n")

                    # write mb_init_request
                    f.write('\t\t<MB_InitRequest>')
                    f.write(f"{button.mb_init_request}")
                    f.write('</MB_InitRequest>')
                    f.write(f"\n")

                    # write mb_on_request
                    f.write('\t\t<MB_OnRequest>')
                    f.write(f"{button.mb_on_request}")
                    f.write('</MB_OnRequest>')
                    f.write(f"\n")

                    # write mb_off_request
                    f.write('\t\t<MB_OffRequest>')
                    f.write(f"{button.mb_off_request}")
                    f.write('</MB_OffRequest>')
                    f.write(f"\n")

                    # write MacroButton boilerplate stuff
                    f.write('\t</MacroButton>')
                    f.write(f"\n")

            # write MacroButtonMap boilerplate stuff
            f.write('\n')
            f.write('</MacroButtonConfiguration>')
            f.write('\n')
            f.write('</VBAudioVoicemeeterMacroButtonMap>')
            f.write('\n')


@dataclass
class Macrobutton:
    macro_button_info:dict
    mb_midi:dict
    mb_trigger:dict
    mb_xinput:dict
    mb_name:str
    mb_subname:str
    mb_init_request:str
    mb_on_request:str
    mb_off_request:str