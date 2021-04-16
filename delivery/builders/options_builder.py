class DeliveryOptionsBuilder():
    def __init__(self):
        super().__init__()

    def build_client_options(self, options):
        for key, value in options.items():
            if "preview" in value:
                if  options["options"].get("secured") == True:
                    raise ValueError("Preview and Secured API cannot be used simultaneously. Disable one in your application's configuration.")
                self.preview = value["preview"]
                try:
                    self.preview_api_key = value["preview_api_key"]
                except KeyError as e:
                    raise Exception("Enabling Preview API requires an API key.") from e
            if "secured" in value and value["secured"]:
                if  options["options"].get("preview") == True:
                    raise ValueError("Preview and Secured API cannot be used simultaneously. Disable one in your application's configuration.")
                self.secured = value["secured"]
                try:
                    self.secured_api_key = value["secured_api_key"]
                except KeyError as e:
                    raise Exception("Enabling Secured API requires an API key.") from e
            if "timeout" in value:
                self.timeout = value["timeout"]
            if "retry_attempts" in value and value["retry_attempts"] != None:
                try:
                    self.retry_attempts = value["retry_attempts"]
                except KeyError as e:
                    raise Exception("An error setting retry_attempts.") from e
        return self