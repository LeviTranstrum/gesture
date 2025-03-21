from . import ert3_config

class Test_Ert3:
    def __init__(self, config):
        self.config = ert3_config.Ert3Config(config)
        self.base_module = self.config.base_module
        self.output_slot = self.config.output_slot
    
    def set_output(self, output_num, value):
        print(f"{output_num}: {value}")
    
    def alarm_on(self):
        print(f"ALARM ON")
    
    def alarm_off(self):
        print(f"ALARM OFF")
