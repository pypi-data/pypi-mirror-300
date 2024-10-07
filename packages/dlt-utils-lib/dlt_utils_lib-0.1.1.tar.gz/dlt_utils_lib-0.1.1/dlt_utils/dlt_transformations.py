from pyspark.sql import DataFrame
from pyspark.sql.types import TimestampType, DateType
from pyspark.sql.functions import col, expr, greatest, when, datediff, lag, min as spark_min, expr, count, coalesce
from pyspark.sql.window import Window


def apply_partitions(df: DataFrame, partitions: dict):
    # apply partitioning to the dataframe
    if partitions:
        for col_name, expression in partitions.items():
            if expression.replace(" ", "") != '':
                df = df.withColumn(col_name, expr(expression))
    return df
    
def update_cdc_timestamp(df: DataFrame, time_diff_threshold: int) -> DataFrame:
    # if cdc_timestamp is null or time difference is greater than threshold, set it to the max timestamp in the row
    timestamp_cols = [col.name for col in df.schema.fields if isinstance(col.dataType, (TimestampType, DateType)) and col.name != 'cdc_timestamp']

    if timestamp_cols:
        max_timestamp_per_row = None

        if len(timestamp_cols) > 1:
            max_timestamp_per_row = greatest(*[col(col_name) for col_name in timestamp_cols])
            # temp fix for market table if possible need take last_update_date becouse of market table contnin close time
            if 'last_update_date' in timestamp_cols:
                max_timestamp_per_row = when(
                                                col('last_update_date').isNotNull(), 
                                                col('last_update_date')
                                            ).otherwise(max_timestamp_per_row)
            # temp fix for artemis table if possible need take last_update_date becouse of market table contnin close time
            if 'version' in timestamp_cols:
                max_timestamp_per_row = when(
                                                col('version').isNotNull(), 
                                                col('version')
                                            ).otherwise(max_timestamp_per_row)        
        else:
            max_timestamp_per_row = col(timestamp_cols[0])
            
        df = df.withColumn(
            'cdc_timestamp',
                when(
                    (col('cdc_timestamp').isNull()) | 
                    (datediff(col('cdc_timestamp'), max_timestamp_per_row) > time_diff_threshold), 
                    max_timestamp_per_row
                ).otherwise(col('cdc_timestamp'))
            )
    return df

def compare_cdc_timestamp_and_commit_timestamp(df, uniq_columns):
    
    if 'commit_timestamp' in df.columns:
        df = df.withColumn('commit_timestamp', coalesce(col('commit_timestamp').cast('timestamp'), col('cdc_timestamp').cast('timestamp')))
    else:
        df = df.withColumn('commit_timestamp', col('cdc_timestamp').cast('timestamp'))

    columns = uniq_columns + ['cdc_timestamp']
    df = df.withWatermark('cdc_timestamp', '5 minutes')  

    grouped_df = df.groupBy(columns).agg(
        count("*").alias("record_count"),
    )
    df_with_conditions = df.join(grouped_df, on=columns, how="left")
    
    df_adjusted = df_with_conditions.withColumn(
        "cdc_timestamp",
        when((col("record_count") > 1) & (col("commit_timestamp").isNotNull()), col("commit_timestamp"))
         .otherwise(col("cdc_timestamp"))
    )
    df_adjusted = df_adjusted.drop("record_count")
    return df_adjusted



def adjust_sequence_operation(df: DataFrame, uniq_columns: list) -> DataFrame:
    window_spec = Window.partitionBy(uniq_columns).orderBy("cdc_timestamp")

    df_with_lag = df.withColumn("prev_op", lag("Op").over(window_spec)) \
                    .withColumn("prev_cdc_timestamp", lag("cdc_timestamp").over(window_spec))

    window_spec_all = Window.partitionBy(uniq_columns)
    df_with_max_u_timestamp = df_with_lag.withColumn(
        "min_u_cdc_timestamp", spark_min(when(col("Op") == "U", col("cdc_timestamp"))).over(window_spec_all)
    )

    df_adjusted = df_with_max_u_timestamp.withColumn(
        "cdc_timestamp",
        when((col("Op") == "I") & (col("min_u_cdc_timestamp").isNotNull()), col("min_u_cdc_timestamp") -expr("interval 1 milliseconds")).otherwise(col("cdc_timestamp"))
    )
    df_final = df_adjusted.drop("prev_op", "prev_cdc_timestamp", "min_u_cdc_timestamp")
    return df_final
