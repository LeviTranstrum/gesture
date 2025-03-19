class Ert3Config:
    def __init__(self, config):
        ert3_config = config.get("ert3_config")
        if ert3_config is not None:
            config = ert3_config

        self.base_module = config.get("base_module")
        self.output_slot = config.get("output_slot")