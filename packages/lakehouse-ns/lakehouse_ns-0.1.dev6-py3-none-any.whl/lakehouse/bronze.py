from lakehouse.etl import ETL
from pyspark.sql import functions as F
from delta.tables import DeltaMergeBuilder, DeltaTable


class Bronze(ETL):
    def __init__(self, spark, **options):
        super().__init__(spark, **options)

    def load(self, table):
        pass
    
    def transform(self, sdf, table: str):
        return sdf
    
    def _transform(self, sdf, table: str):
        t = {
            "LH_BronzeTS": F.current_timestamp().cast("timestamp"),
        }
        return sdf.withColumns(t)

class BronzeOverwrite(Bronze):
    def write(self, sdf, table: str):
        tbl_name = f"{self.catalog}.{self.schema_to}.{table}"
        sdf.write.format("delta").mode("overwrite").saveAsTable(tbl_name)

class BronzeAppend(Bronze):
    def write(self, sdf, table: str):
        tbl_name = f"{self.catalog}.{self.schema_to}.{table}"
        sdf.write.format("delta").mode("append").saveAsTable(tbl_name)

class BronzeReplaceWhere(Bronze):
    def get_replace_condition(self, sdf, table: str) -> str:
        pass

    def write(self, sdf, table: str):
        tbl_name = f"{self.catalog}.{self.schema_to}.{table}"
        ops = {"replaceWhere": self.get_replace_condition(sdf, table)}
        sdf.write.format("delta").options(**ops).mode("overwrite").saveAsTable(tbl_name)
    
class BronzeMerge(Bronze):
    def get_delta_merge_builder(self, delta_table: DeltaTable) -> DeltaMergeBuilder:
        pass

    def write(self, sdf, table: str):
        tbl_name = f"{self.catalog}.{self.schema_to}.{table}"
        delta_table = DeltaTable.forName(self.spark, tbl_name)
        delta_merge_builder = self.get_delta_merge_builder(delta_table)
        delta_merge_builder.execute()