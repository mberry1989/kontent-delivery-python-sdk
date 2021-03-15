class DeliveryOptionsBuilder():
    def __init__(self):
        super().__init__()

    def build_client_options(self, options):
        for key, value in options.items():
            if "preview" in value:
                self.preview = value["preview"]
                try:
                    self.preview_api_key = value["preview_api_key"]
                except KeyError as e:
                    raise Exception("Enabling Preview API requires an API key.") from e
            if "secured" in value and value["secured"]:
                    self.secured = value["secured"]
                    try:
                        self.secured_api_key = value["secured_api_key"]
                    except KeyError as e:
                        raise Exception("Enabling Secured API requires an API key.") from e
            if "timeout" in value:
                self.timeout = value["timeout"]
        return self