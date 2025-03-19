import m3io_py as m3io
from ert3_config import Ert3Config

class Ert3:
    def __init__(self, config):
        self.config = Ert3Config(config)
        self.base_module = self.config.base_module
        self.output_slot = self.config.output_slot
    
    def set_output(self, output_num, value):
        return m3io.writeM3OutRelayP(self.base_module, self.output_slot, output_num, value)
    
    def alarm_on():
        return m3io.setM3AlmLed(1)
    
    def alarm_off():
        return m3io.setM3AlmLed(0)