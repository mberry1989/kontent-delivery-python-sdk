class Filter:
    def __init__(self, api_property: str, operation: str, value):
        self.api_property = api_property
        self.operation = operation
        self.value = value

class FilterBuilder:
    def __init__(self, filters):
        self.filters = filters
        self.return_url = None

    @property
    def return_url(self):
        return self._return_url

    @return_url.setter
    def return_url(self, value):
        query_string = []

        for filter in self.filters:
            if isinstance(filter, Filter):
                position = self.filters.index(filter)
                if position == 0:
                    separator = "?"
                else:
                    separator = "&"            
                operation = f"{filter.operation}="
                url_segment = f"{separator}{filter.api_property}{operation}{filter.value}"
            else:
                raise TypeError("Filters must be of type 'Filter'")
            query_string.append(url_segment)

        self._return_url = "".join(query_string)
        