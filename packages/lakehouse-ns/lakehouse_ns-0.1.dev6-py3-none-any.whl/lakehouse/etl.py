class ETL:
    def __init__(self, spark, **options):
        self.options = options
        self.catalog = options["catalog"]
        self.schema_from = options.get("schema_from", None)
        self.schema_to = options["schema_to"]
        self.spark = spark
        assert spark.catalog.databaseExists("schema_to") == True


    def load(self, table: str):
        pass

    def transform(self, sdf, table: str):
        pass

    def _transform(self, sdf, table: str):
        pass
        
    def write(self, sdf, table: str):
        pass

    def execute_one(self, table: str):
        sdf = self.load(table)
        sdf = self.transform(sdf, table)
        sdf = self._transform(sdf, table)
        self.write(sdf, table)

    def debug_one(self, table: str, n: int):
        assert n>=0 and n<3
        sdf = self.load(table)
        if n >=1:
            sdf = self.transform(sdf, table)
        if n ==2:
            sdf = self._transform(sdf, table)
        return sdf


    def execute_all(self, tables: list[str]):
        for t in tables:
            self.execute_one(t)

