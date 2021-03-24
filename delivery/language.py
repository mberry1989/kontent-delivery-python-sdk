from requests.models import Response

class Language:
    def __init__(self, system:dict, api_response:Response):
        self.id = system["id"]
        self.name = system["name"]
        self.codename = system["codename"]
        self.api_response = api_response

class LanguageListing:
    def __init__(self, languages:list, pagination:dict, api_response:Response):
        self.languages = languages
        self.pagination = pagination
        self.skip = pagination["skip"]
        self.limit = pagination["limit"]
        self.count = pagination["count"]
        self.next_page = pagination["next_page"]
        self.api_response = api_response