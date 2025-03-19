class ImageServiceConfig:
    def __init__(self, config):
        image_service_config = config.get("image_service_config")
        if image_service_config is not None:
            config = image_service_config
        
        self.server = config.get("server")
        self.port = config.get("port")
        self.endpoint = config.get("endpoint")