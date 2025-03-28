class ImageServiceConfig:
    def __init__(self, config):
        image_service_config = config.get("image_service_config")
        if image_service_config is not None:
            config = image_service_config
        
        self.server = config.get("server")
        self.port = config.get("port")
        self.image_endpoint = config.get("image_endpoint")
        self.visualization_endpoint = config.get("visualization_endpoint")