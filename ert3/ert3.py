import m3io_py as m3io
from . import ert3_config

class Ert3:
    def __init__(self, config):
        self.config = ert3_config.Ert3Config(config)
        self.base_module = self.config.base_module
        self.input_slot = self.config.input_slot
        self.output_slot = self.config.output_slot
        self.reset_outputs()
        self.alarm_off()
    
    def get_input(self, input_num):
        value = []
        error = m3io.readM3InRelayP(self.base_module, self.input_slot, input_num, value)
        if error == -1:
            raise Exception(f"failed to read input {input_num} from slot {self.input_slot}")
        return value[0]

    def set_output(self, output_num, value):
        return m3io.writeM3OutRelayP(self.base_module, self.output_slot, output_num, value)
    
    def reset_outputs(self):
        for i in range(64):
            self.set_output(i, 0)

    def alarm_on(self):
        return m3io.setM3AlmLed(1)
    
    def alarm_off(self):
        return m3io.setM3AlmLed(0)