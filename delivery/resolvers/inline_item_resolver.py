from bs4 import BeautifulSoup
from delivery.content_item import ContentItem


class InlineItemResolver:
    def __init__(self, client):
        self.custom_item_resolver = client.custom_item_resolver

    def resolve(self, content:ContentItem):
        elements = vars(content.elements)
        for element in elements.values():
            if element.type == "rich_text" and element.modular_content:
                modular_content_codenames = element.modular_content
                for codename in modular_content_codenames:
                    modular_content_item = content.modular_content[codename]
                    linked_item = ContentItem(modular_content_item["system"], modular_content_item["elements"])
                    resolved_item = self.custom_item_resolver.resolve_item(linked_item)
                    
                    if resolved_item:
                        soup = BeautifulSoup(element.value,"html.parser")
                        tag = soup.find("object", attrs={"data-codename": codename})
                        tag.replace_with(resolved_item)
                        element.value = soup.prettify(formatter=None)
        return content