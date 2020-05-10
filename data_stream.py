
import logging
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pyspark.sql.functions as psf

# TODO Create a schema for incoming resources
schema = StructType([
    StructField('crime_id', StringType(), True),
    StructField('original_crime_type_name', StringType(), True),
    StructField('report_date', StringType(), True),
    StructField('call_date', StringType(), True),
    StructField('offense_date', StringType(), True),
    StructField('call_time', StringType(), True),
    StructField('call_date_time', TimestampType(), True),
    StructField('disposition', StringType(), True),
    StructField('address', StringType(), True),
    StructField('city', StringType(), True),
    StructField('state', StringType(), True),
    StructField('agency_id', StringType(), True),
    StructField('address_type', StringType(), True),
    StructField('common_location', StringType(), True),
])

def run_spark_job(spark):

    # Create Spark configuration
    df = spark \
        .readStream \
        .format('kafka') \
        .option('kafka.bootstrap.servers','localhost:9092') \
        .option('subscribe', 'com.udacity.crime.police-event') \
        .option('startingOffsets', 'earliest') \
        .option('maxOffsetsPerTrigger', 10) \
        .option('maxRatePerPartition', 10) \
        .option('stopGracefullyOnShutdown', "true") \
        .load()

    # Show schema 
    df.printSchema()

    # Extract the correct column from the kafka input resources
    kafka_df = df.selectExpr("CAST(value AS STRING)")

    service_table = kafka_df\
        .select(psf.from_json(psf.col('value'), schema).alias("DF"))\
        .select("DF.*")

    # Select original_crime_type_name and disposition
    distinct_table = service_table \
        .select('original_crime_type_name', 'disposition', 'call_date_time') \
        .distinct() \
        .withWatermark('call_date_time', "1 minute")

    # Count the number of original crime type
    agg_df = distinct_table \
        .dropna() \
        .select('original_crime_type_name') \
        .groupby('original_crime_type_name') \
        .agg({'original_crime_type_name': 'count'}) \
        .orderBy('count(original_crime_type_name)', ascending=True)

    # Submit a screen shot of a batch ingestion of the aggregation
    query = agg_df \
        .writeStream \
        .format('console') \
        .outputMode('Complete') \
        .start()


    # Attach a ProgressReporter
    query.awaitTermination()

    # Get the right radio code json path
    radio_code_json_filepath = "radio_code.json"
    radio_code_df = spark.read.json(radio_code_json_filepath)


    # Rename disposition_code column to disposition
    radio_code_df = radio_code_df.withColumnRenamed("disposition_code", "disposition")

    # Join on disposition column
    join_query = agg_df.join(radio_code_df, col('agg_df.disposition') == col('radio_code_df.disposition'), 'left_outer')


    join_query.awaitTermination()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    # Create Spark in Standalone mode
    spark = SparkSession \
        .builder \
        .master("local[*]") \
        .appName("KafkaSparkStructuredStreaming") \
        .config("spark.ui.port", 3000) \
        .getOrCreate()

    logger.info("Spark started")

    run_spark_job(spark)

    spark.stop()