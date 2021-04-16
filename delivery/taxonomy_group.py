import json
from types import SimpleNamespace
from requests.models import Response


class TaxonomyGroup:
    def __init__(self, system: dict, terms:dict, 
                 api_response:Response = None):
        self.id = system["id"]
        self.name = system["name"]
        self.codename = system["codename"]
        self.last_modified = system["last_modified"]
        self.terms = json.loads(json.dumps(terms), 
                                object_hook=lambda d: SimpleNamespace(**d))
        self.api_response = api_response


class TaxonomyGroupListing:
    def __init__(self, taxonomy_groups:list, pagination:dict,
                 api_response:Response):
        self.taxonomy_groups = taxonomy_groups
        self.pagination = pagination
        self.skip = pagination["skip"]
        self.limit = pagination["limit"]
        self.count = pagination["count"]
        self.next_page = pagination["next_page"]
        self.api_response = api_response