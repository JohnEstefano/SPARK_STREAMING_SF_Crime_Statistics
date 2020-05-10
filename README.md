# SPARK_STREAMING_SF_Crime_Statistics

### Project Overview
In this project a real-world dataset, extracted from Kaggle, on San Francisco crime incidents,was used to provide statistical analyses of the data using Apache Spark Structured Streaming. 

### Development Environment
A preconfigured workspace was used but this project could be ran locally, you will need to set up your environment properly as described below:

Spark 2.4.3

Scala 2.11.x

Java 1.8.x

Kafka build with Scala 2.11.x

Python 3.6.x or 3.7.x

### Beginning the Project
This project required creating topics, starting Zookeeper and Kafka servers, and your Kafka bootstrap server. Modifications to the zookeeper.properties and server.properties was also performed.

#### Local Environment
> Install requirements using ./start.sh if you use conda for Python. If you use pip rather than conda, then use pip install -r requirements.txt.

> Use the commands below to start the Zookeeper and Kafka servers. You can find the bin and config folder in the Kafka binary that you have downloaded and unzipped.

```
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
```

> You can start the bootstrap server using this Python command: python producer_server.py.

#### Workspace Environment

> Modify the zookeeper.properties and producer.properties given to suit your topic and port number of your choice. Start up these servers in the terminal using the commands:
```
/usr/bin/zookeeper-server-start zookeeper.properties
/usr/bin/kafka-server-start producer.properties
```

> You’ll need to open up two terminal tabs to execute each command.

> Install requirements using the provided ./start.sh script. This needs to be done every time you re-open the workspace, or anytime after you've refreshed, or woken up, or reset data, or used the "Get New Content" button in this workspace.

> In the terminal, to install other packages that you think are necessary to complete the project, use conda install <package_name>. You may need to reinstall these packages every time you re-open the workspace, or anytime after you've refreshed, or woken up, or reset data, or used the "Get New Content" button in this workspace.


### Step 1
> The first step is to build a simple Kafka server.

#### Local Environment
> To see if server was correctly implemented, the following command was used:
```
bin/kafka-console-consumer.sh --bootstrap-server localhost:<your-port-number> --topic <your-topic-name> --from-beginning to see your output.
```

#### Workspace Environment
> The kafka-consumer-console was started, using the following command: 
```
/usr/bin/kafka-consumer-console.
```
A screenshot of the kafka-consumer-console output is provided below:

#### Kafka Consumer Console Output
<img src='1.PNG'/>

### Step 2
> Apache Spark already has an integration with Kafka brokers, so we would not normally need a separate Kafka consumer. However, one was created anyway. A dummy producer was created.

> Submit Spark Job.

> Do a spark-submit using this command: 
```
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.4 --master local[*] data_stream.py
```

> A screenshot of the progress reporter after executing a Spark job was provided. 

#### Progress reporter 
<img src='2.1.PNG'/>
<img src='2.2.PNG'/>

> A screenshot of the Spark Streaming UI as the streaming continued was provided. 

#### Spark Streaming UI
<img src='3.PNG'/>


### QUESTIONS TO ANSWER

#### How did changing values on the SparkSession property parameters affect the throughput and latency of the data?
It mainly affected ```processedRowsPerSecond``` by either decreasing it or increasing it. In other words, it directly influenced the 
rate which Spark is processing data


#### What were the 2-3 most efficient SparkSession property key/value pairs? Through testing multiple variations on values, how can you tell these were the most optimal?

The 2 most efficient SparkSession property key/value pairs was
```
spark.streaming.kafka.maxRatePerPartition   10

spark.default.parallelism                   10000
```
```processedRowsPerSecond```  was used to test for a highest throughput.

