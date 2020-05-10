# SPARK_STREAMING_SF_Crime_Statistics



## How did changing values on the SparkSession property parameters affect the throughput and latency of the data?
It mainly affected processedRowsPerSecond by either decreasing it or increasing it. In other words, it directly influenced the 
rate which Spark is processing data


## What were the 2-3 most efficient SparkSession property key/value pairs? Through testing multiple variations on values, how can you tell these were the most optimal?

The 2 most efficient SparkSession property key/value pairs was

spark.streaming.kafka.maxRatePerPartition   10
spark.default.parallelism                   10000

processedRowsPerSecond  was used to test for a highest throughput.

