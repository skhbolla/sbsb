# Cloudwatch Logs
## Intro

In an modern architecture, workloads are ephemeral—containers spin up, do a job, crash, and get terminated by an Auto Scaling Group in minutes. If your application writes its logs to a local file on the server's hard drive, that data is completely wiped out the second the instance dies.

Worse, if you have a cluster of 500 nodes and a customer reports a failed API request, you cannot manually SSH into 500 separate machines to search through text files. CloudWatch Logs solves this by acting as a highly scalable, centralized log aggregation data plane. It decouples the generation of a log from its physical storage, ensuring that your debugging data survives even if the underlying infrastructure is destroyed.

Think of CloudWatch Logs as a **distributed, schema-on-read log repository**. To manage millions of text lines systematically, CloudWatch Logs doesn't just dump everything into a massive bucket. It organizes data using a strict three-tier structural hierarchy:

- **Log Groups**: The top-level logical boundary, usually representing a specific application, service microservice, or environment tier (e.g., `/aws/containerinsights/llm-cluster/application`). This is where you configure global parameters like how long the data lives (Retention Policies), who can read it (IAM policies), and how it's encrypted (KMS Keys).
- **Log Streams**: Inside a Log Group, you have Log Streams. A stream represents an unbroken sequence of log events coming from one specific, unique source—like a single EC2 instance ID, a specific ECS task, or an individual Kubernetes pod name (e.g., `inference-pod-worker-01`).
- **Log Events**: This is the raw data payload itself. Every single event is immutable and contains exactly two attributes: a `Timestamp` (when it happened) and the raw `Message` string (the actual log line or JSON object)

## The 60-Second Interview Definition

> "Amazon CloudWatch Logs is an enterprise-grade log aggregation and centralized analytics engine designed to capture, index, and retain raw text and JSON log streams across transient cloud infrastructure. It organizes telemetry using a two-tier hierarchy of Log Groups for macro-level lifecycle management and Log Streams for distinct execution threads. By decoupling log generation from physical storage, it prevents data loss during infrastructure scaling. It features a built-in analytical engine called Logs Insights, which executes complex parallel queries using a purpose-built syntax, allowing engineers to parse and isolate failures across terabytes of data in seconds. Furthermore, it bridges the gap between logs and metrics through Metric Filters, which scan incoming text patterns in real time to increment CloudWatch Metrics synchronously."

---

```
 [ The CloudWatch Logs Structured Hierarchy ]
               
  +---------------------------------------------------------------+

  | Log Group: /aws/containerinsights/production-llm/application   |
  | (Defines: 30-Day Retention, KMS Encryption, Access Controls)  |
  +---------------------------------------------------------------+

         |
         +-------------------------+-------------------------+

         |                                                   |
         v                                                   v
  +-------------------------------+   +-------------------------------+

  | Log Stream: inference-pod-01  |   | Log Stream: inference-pod-02  |
  | (Thread from Container Alpha) |   | (Thread from Container Beta)  |
  +-------------------------------+   +-------------------------------+

         |
         v
  +---------------------------------------------------------------+

  | Log Event: { Timestamp: 17123456, Message: "OOM Kill Panic" } |
  +---------------------------------------------------------------+
```


## Ingestion Pipelines & The Payload Trap

Because CloudWatch Logs operates as a centralized API service, pushing log lines from your servers into AWS requires a shipping agent (like the CloudWatch Agent, Fluent Bit, or Logstash) running inside your operating system. This agent reads local text files or grabs `stdout` streams, bundles the logs into batches, and ships them over the network via the `PutLogEvents` API.

However, just like metrics, you can fall straight into an infrastructure trap if you don't respect the hard data-plane limits enforced by the AWS ingestion pipelines:

- **The Size Ceiling**: A single batch of log events sent over the network cannot exceed **1,048,576 bytes (1 MB)**. If your application dumps a massive, un-truncated database stack trace that breaches this limit, the AWS API will reject the entire payload immediately.
- **The Count Ceiling**: A single batch can contain a maximum of **10,000 log events**. Even if your logs are tiny, if you try to bundle 10,001 items into one API call, the pipeline breaks.
- **The Time Window Restraint**: ==The timestamps inside a single batch cannot span a window wider than **24 hours**. Furthermore, you cannot ingest logs that are older than **14 days** or more than **2 hours in the future**.==If a system clock drifts or an application logs old cached data, the ingestion pipeline flags it as invalid and drops it.

## The SequenceToken Evolution

Historically, CloudWatch Logs enforced a strict state-machine synchronization mechanism called a **SequenceToken** for every single Log Stream. If multiple processes or app threads tried to write to the exact same stream simultaneously, they would step on each other's tokens, resulting in a `InvalidSequenceTokenException` lock.

While modern AWS APIs have evolved to support sequence-tokenless uploads, trying to force multiple parallel app workers to share a single Log Stream will still choke your network throughput and create massive API bottlenecks. The golden rule for high-performance cloud operations is simple: **Give every single distinct thread or container its own uniquely named Log Stream.**

## Metric Filters

[CloudWatch](https://aws.amazon.com/cloudwatch/) includes a powerful feature called **Metric Filters** that connects the text engine to the math engine. A Metric Filter sits directly inside the ingestion pipeline. As raw logs stream into a Log Group, the filter evaluates them _in real-time_ before they are written to disk, looking for specific text patterns or parsing JSON keys (e.g., searching for the word `CRITICAL` or mapping `$.status == 500`).

The moment it finds a match, it synchronously increments a CloudWatch Custom Metric. The major operational benefit here is that you can turn unstructured text errors into clean, numeric metrics instantly. You can then attach standard CloudWatch Alarms to those metrics to trigger auto-scaling or automated self-healing scripts without writing complex log-parsing code.

## Logs Insights

Once logs are safely inside the database, viewing them chronologically in the AWS console is incredibly slow during an active production outage. To solve this, AWS provides **[CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html)**—a purpose-built, schema-on-read analytical engine.

Instead of opening individual log streams one by one, Logs Insights lets you write parallelized queries across an entire Log Group simultaneously. Using a Unix-like pipeline syntax (`fields`, `filter`, `stats`, `sort`), it scans terabytes of raw logs in seconds, automatically parses JSON logs into queryable fields, and lets you calculate error frequencies, isolate request IDs, and group errors by time blocks instantly. 

==Log Insights allow you to query multiple log groups even in different accounts.==
==Remember that insights is a query engine, not a real-engine.==


## Exporting logs to S3
Cloud watch logs can be batch exported to S3 via the `CreateExportTask` API call.

Note that this is not a real time operation i.e we are not streaming logs to S3 as they arrive at the log group. This is a simple batch-export.

If you need to real time stream logs, you have to use "cloudwatch logs subscriptions" instead.

## Cloudwatch Logs Subscriptions

- Get real time log events from CloudWatch logs for processsing and analysis
- Send to Kinesis Data Streams, Kinesis Data Firehose , or Lambda
![[_assets/Pasted image 20260805121606.png]]
- Subscription Filter : Subscriptions can be created by applying subscription filters to log groups. (There is no specific option to create a subscription.. subscriptions are implicitly created when a subscription filter is created). Subscription filters can be used decide which log events to deliver to destination. Type a pattern to stream only specific logs (e.g., `ERROR`), or leave it blank to stream all logs.

![[_assets/Pasted image 20260805112914.png]]
![[_assets/Pasted image 20260805112950.png]]
![[_assets/Pasted image 20260805113123.png]]

---

## CloudWatch Logs Data Protection

![[_assets/Pasted image 20260805122937.png]]
![[_assets/Pasted image 20260805123709.png]]
If you need to create an alarm when sensitive data is ingested to logs, then follow below process:
- Identify the log group you want to target
- Add your Data Protection Policy on the log group (This will mask the sensitive info)
- AWS automatically creates a `LogEventsWithFindings` metric which creates a datapoint every time sensitive info is found by protection policy.
- Create an alarm over this metric.