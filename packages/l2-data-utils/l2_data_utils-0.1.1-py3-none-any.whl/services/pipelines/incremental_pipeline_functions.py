from pyspark.sql.functions import col, min as spark_min


def get_last_partitions(df, column_name, limit=7):
    """Retrieve the last unique partitions from the specified column."""
    return [row[column_name] for row in df
            .select(col(column_name))
            .distinct()
            .orderBy(col(column_name).desc())
            .limit(limit)
            .collect()]
    

def get_min_cdc_bets_timestamps_and_partition(df, sourse_table_col, min_value_name, partition_column_name):

    """Group by source_table and get the minimum cdc bet timestamps and a list of cdc_timestamp_partition_month."""

    return df.groupBy(sourse_table_col) \
        .agg(
            spark_min(min_value_name).alias("min_source_cdc_timestamp"),
            spark_min(partition_column_name).alias("min_source_partition") 
        ) \
        .toPandas() \
        .set_index(sourse_table_col)[['min_source_cdc_timestamp', 'min_source_partition']].to_dict('index')


def get_partition_values(df, partition_column_name):
    """Retrieve distinct partition values from the DataFrame."""
    return [row[partition_column_name] for row in df.select(col(partition_column_name)).distinct().collect()]