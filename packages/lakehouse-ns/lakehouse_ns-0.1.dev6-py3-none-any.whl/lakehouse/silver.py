from lakehouse.etl import ETL
from pyspark.sql import functions as F
from delta.tables import DeltaMergeBuilder, DeltaTable


class Silver(ETL):
    def __init__(self, spark, **options):
        super().__init__(spark, **options)

    def filter_load(self, sdf, table):
        return sdf

    def load(self, table):
        tbl_name = f"{self.catalog}.{self.schema_to}.{table}"
        sdf = self.spark.read.format("delta").loadTable(tbl_name)
        return self.filter_load(sdf, table)
    
    def transform(self, sdf, table: str):
        return sdf
    
    def _transform(self, sdf, table: str):
        cols = sdf.columns
        t = {
            "LH_SilverTS": F.current_timestamp().cast("timestamp"),
        }
        sdf = sdf.withColumns(t)
        return sdf.select(*cols, "LH_BronzeTS", "LH_SilverTS")

class SilverOverwrite(Silver):
    def write(self, sdf, table: str):
        tbl_name = f"{self.catalog}.{self.schema_to}.{table}"
        sdf.write.format("delta").mode("overwrite").saveAsTable(tbl_name)

class SilverAppend(Silver):
    def write(self, sdf, table: str):
        tbl_name = f"{self.catalog}.{self.schema_to}.{table}"
        sdf.write.format("delta").mode("append").saveAsTable(tbl_name)

class SilverReplaceWhere(Silver):
    def get_replace_condition(self, sdf, table: str) -> str:
        pass

    def write(self, sdf, table: str):
        tbl_name = f"{self.catalog}.{self.schema_to}.{table}"
        ops = {"replaceWhere": self.get_replace_condition(sdf, table)}
        sdf.write.format("delta").options(**ops).mode("overwrite").saveAsTable(tbl_name)
    
class SilverMerge(Silver):
    def get_delta_merge_builder(self, delta_table: DeltaTable) -> DeltaMergeBuilder:
        pass

    def write(self, sdf, table: str):
        tbl_name = f"{self.catalog}.{self.schema_to}.{table}"
        delta_table = DeltaTable.forName(self.spark, tbl_name)
        delta_merge_builder = self.get_delta_merge_builder(delta_table)
        delta_merge_builder.execute()