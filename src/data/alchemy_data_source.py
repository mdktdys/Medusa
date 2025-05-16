from .data_source import DataSource

class AlchemyDataSource(DataSource):
    def __init__(self, session):
        self.session = session