class FingerCounterConfig:
    def __init__(self, config):
        finger_counter_config = config.get("finger_counter_config")
        if finger_counter_config is not None:
            config = finger_counter_config

        self.thumb_length = config.get('thumb_length')
        self.index_length = config.get('index_length')
        self.middle_length = config.get('middle_length')
        self.ring_length = config.get('ring_length')
        self.pinky_length = config.get('pinky_length')
        self.min_confidence = config.get('min_confidence')