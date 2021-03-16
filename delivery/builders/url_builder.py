class UrlBuilder:
    @staticmethod
    def build_url(client, endpoint, query_string=""):
        PROTOCOL = "https://"
        DELIVERY_DOMAIN = "deliver.kontent.ai/"
        PREVIEW_DOMAIN = "preview-deliver.kontent.ai/"

        domain = DELIVERY_DOMAIN
        if client.client_options:
            if client.client_options.preview:
                domain = PREVIEW_DOMAIN
        url = f"{PROTOCOL}{domain}{client.project_id}{endpoint}{query_string}"

        return url
        
