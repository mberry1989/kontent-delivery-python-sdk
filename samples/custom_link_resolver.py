class CustomLinkResolver:
    @staticmethod
    def resolve_link(link):
        if link.type == "coffee":
            return f"/coffees/{link.url_slug}"
        if link.type == "article":
            return f"/articles/{link.url_slug}"