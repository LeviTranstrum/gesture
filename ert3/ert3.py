import m3io_py as m3io
from . import ert3_config

class Ert3:
    def __init__(self, config):
        self.config = ert3_config.Ert3Config(config)
        self.base_module = self.config.base_module
        self.output_slot = self.config.output_slot
    
    def set_output(self, output_num, value):
        return m3io.writeM3OutRelayP(self.base_module, self.output_slot, output_num, value)
    
    def alarm_on(self):
        return m3io.setM3AlmLed(1)
    
    def alarm_off(self):
        return m3io.setM3AlmLed(0)