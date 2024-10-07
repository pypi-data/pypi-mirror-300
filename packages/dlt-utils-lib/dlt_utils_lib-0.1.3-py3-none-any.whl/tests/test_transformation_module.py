import sys
import os

# Set the path to the top-level directory containing dlt_utils_lib
sys.path.append('/Workspace/Repos/main_pipelines/dlt-pipeline/dlt_utils_lib')
print('check import test')
print(os.getcwd())

import pytest
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import expr
from pyspark.sql.types import TimestampType, StringType
from datetime import datetime
import warnings
from databricks.sdk.runtime import *


from dlt_utils.dlt_transformations import update_cdc_timestamp, apply_partitions

@pytest.fixture(scope="session")
def spark() -> SparkSession:
    return SparkSession.builder.getOrCreate()


def test_apply_partitions(spark):
    # Create a sample dataframe
    data = [
        Row(id=1, name="Alice", age=25),
        Row(id=2, name="Bob", age=30),
        Row(id=3, name="Charlie", age=35)
    ]
    df = spark.createDataFrame(data)
    
    # Define partitions (in this case, expressions for new columns)
    partitions = {
        "age_group": "CASE WHEN age < 30 THEN 'Young' ELSE 'Adult' END"
    }

    # Apply the function
    result_df = apply_partitions(df, partitions)
    
    # Check if the new partitioned column has been added correctly
    result = result_df.select("age_group").collect()

    assert result[0]['age_group'] == "Young"
    assert result[1]['age_group'] == "Adult"
    assert result[2]['age_group'] == "Adult"

def test_update_cdc_timestamp(spark):
    # Create a sample dataframe
    data = [
        Row(id=1, created_at=datetime(2024, 1, 1), updated_at=datetime(2024, 1, 10), cdc_timestamp=None),
        Row(id=2, created_at=datetime(2024, 1, 5), updated_at=datetime(2024, 1, 15), cdc_timestamp=datetime(2024, 1, 1)),
        Row(id=3, created_at=datetime(2024, 1, 8), updated_at=datetime(2024, 1, 12), cdc_timestamp=None)
    ]
    
    df = spark.createDataFrame(data)

    # Apply the function with a threshold of 5 days
    result_df = update_cdc_timestamp(df, time_diff_threshold=5)
    
    # Collect the results
    result = result_df.select("cdc_timestamp").collect()

    # The first and third rows should get updated with the greatest timestamp (updated_at)
    assert result[0]['cdc_timestamp'] == datetime(2024, 1, 10)
    assert result[2]['cdc_timestamp'] == datetime(2024, 1, 12)
    
    # The second row should retain its original cdc_timestamp because the difference is less than 5 days
    assert result[1]['cdc_timestamp'] == datetime(2024, 1, 1)