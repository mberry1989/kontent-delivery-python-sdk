class ContentItem():
    def __init__(self, system, elements):
        self.id = system["id"]
        self.name = system["name"]
        self.codename = system["codename"]
        self.language = system["language"]
        self.content_type = system["type"]
        self.last_modified = system["last_modified"]
        self.collection = system["collection"]
        self.workflow_step = system["workflow_step"]
        self.elements = elements