from kontent_delivery.content_item import ContentItem
from bs4 import BeautifulSoup


class ContentLinkResolver:
    def __init__(self, client):
        self.custom_link_resolver = client.custom_link_resolver

    def resolve(self, content: ContentItem):
        elements = vars(content.elements)
        for element in elements.values():
            if element.type == "rich_text" and element.links:
                links = vars(element.links)
                for link_key, link_values in links.items():
                    resolved_link = self.custom_link_resolver.resolve_link(link_values)
                    soup = BeautifulSoup(element.value, "html.parser")
                    tag = soup.find("a", attrs={"data-item-id": link_key})
                    tag["href"] = resolved_link
                    element.value = soup.prettify()
        return content
