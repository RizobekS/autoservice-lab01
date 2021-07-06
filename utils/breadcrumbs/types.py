class Breadcrumb:
    __slots__ = ('title', 'url')

    def __init__(self, title: str, url: str):
        self.title: str = title
        self.url: str = url

    def __repr__(self):
        return f'Breadcrumb(title="{self.title}", url="{self.url}")'
