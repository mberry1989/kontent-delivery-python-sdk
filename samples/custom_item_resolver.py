class CustomItemResolver:
    @staticmethod
    def resolve_item(linked_item):
        if linked_item.content_type == "article":
            return f"<h1>{linked_item.elements.title.value}</h1>"
            
        if linked_item.content_type == "tweet":
            return (f"<blockquote class='twitter-tweet' data-lang='en'"
                    f"data-theme={linked_item.elements.theme.value[0].codename}>"
                    f"<a href={linked_item.elements.tweet_link.value}></a></blockquote>")