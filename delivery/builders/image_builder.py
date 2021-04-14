class ImageBuilder:
    def __init__(self, url):
        self.url = url  

    def transform(self, *args):
        query_string = []

        for arg in args:
            result = arg
            if result != "":
                if len(query_string) == 0:
                    separator = "?"
                else:
                    separator = "&"
                url_segment = f"{separator}{result}"
                query_string.append(url_segment)
            
        query_string = "".join(query_string)
        transformed_url = f"{self.url}{query_string}"

        return transformed_url

    def width(self, width:int):
        width_url = f"w={width}"
        return width_url

    def height(self, height:int):
        return f"h={height}"

    def pixel_ratio(self, dpr:float):
        return f"dpr={dpr}"

    def fit_mode(self, fit:str):
        FITMODE = ["crop", "clip","scale"]
        if fit in FITMODE:
            fit_url = f"fit={fit}"
            return fit_url
        else:
            raise ValueError("fit mode parameter needs to be 'crop', 'clip' or 'scale'.")

    def rect(self, x:float, y:float, width:float, height: float):
        rect = f"rect={x},{y},{width},{height}"
        return rect

    def focal_point(self, x:float, y: float, z:int):
        fp = f"crop=focalpoint&fp-x={x}&fp-y={y}&fp-z={z}"
        return fp

    def background_color(self, color:str):
        return f"bg={color}"

    def output_format(self, format:str):
        return f"fm={format}"

    def quality(self, quality:int):
        return f"quality={quality}"

    def lossless(self, lossless:bool):
        return f"lossless={lossless}"

    def auto_format_selection(self, auto):
        if auto:
            return f"auto=format"
        return ""