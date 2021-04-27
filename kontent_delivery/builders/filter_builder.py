class Filter:
    def __init__(self, api_property: str, operation: str, value):
        self.api_property = api_property
        self.operation = operation
        self.value = value


class FilterBuilder:
    def __init__(self):
        pass

    def build_return_url(self, filters):
        query_string = []

        for filter in filters:
            if isinstance(filter, Filter):
                position = filters.index(filter)
                separator = "&"
                if position == 0:
                    separator = "?"
                if type(filter.value) == list:
                    filter.value = ','.join(map(str, filter.value))
                url_segment = f"{separator}{filter.api_property}{filter.operation}={filter.value}"
            else:
                raise TypeError("Filters must be of type 'Filter'")
            query_string.append(url_segment)

        return "".join(query_string)
