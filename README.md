# Data Engineer Take-Home Assessment

## Overview
Hi there! 👋
This repo contains my solution to the Linq Data Engineer take-home challenge. The main goal of this project is to build a **reliable event processing system** that can handle **real-time logs**, maintain **data consistency**, and recover from any kind of **failures or crashes** — all without using a traditional database.

In this write-up, I’ll walk you through how I approached the problem, how I tested it, and some thoughts on scaling it further. You’ll also find instructions on how to run everything in **VS Code**.

---

## 🚀 Approach
### 1️⃣ **Event Processing Logic**
- I used a **JSONL file** (`events.jsonl`) to store incoming events.
- Each event has an `id`, `category`, and `value`.
- The processor reads each event, validates it, and skips any duplicates.

### 2️⃣ **Checkpointing & Crash Recovery**
- To make the system fault-tolerant, I added a **checkpointing mechanism** using a file called `checkpoint.json`.
- This file keeps track of the last successfully processed event.
- So, if the program crashes, it picks up right where it left off — no data loss, no duplicate processing.

### 3️⃣ **Duplicate & Order Handling**
- I keep a set of already seen `event IDs` to prevent processing the same event more than once.
- Even if events come in out of order, I **sort them by** `id` before processing to make sure everything happens in the correct sequence.

### 4️⃣ **Testing with `unittest`**
- All test cases are written in `test_event_processor.py` using **Python's `unittest` framework**. 
- Print statements in test cases allow **better visibility of state changes**.

---

## 🔍 Scenarios & Testing
I tested the solution under different scenarios. Here's what I checked:

✅ **Scenario 1: Initial Processing** – Ensures that the processor correctly processes all events when run for the first time.  
✅ **Scenario 2: Simulated Crash & Recovery** – Ensures that the processor correctly resumes processing from the last checkpoint.  
✅ **Scenario 3: Duplicate Event Handling** – Ensures that duplicate events are ignored and not reprocessed.  
✅ **Scenario 4: Out-of-Order Events** – Ensures that events are processed in correct order, even if they arrive out of sequence.  
✅ **Scenario 5: Large Volume Handling** – Tests how the processor handles a large dataset (1,000+ events).  

---

## ⚖️ Trade-offs & Assumptions
### 🔹 **Trade-offs**
- I went with a **file-based approach** (instead of a database) to keep things simple and focused on logic. But of course, this might not scale for very large datasets.
- Everything runs on a **single thread**, which works fine for now, but it can be optimized with parallel or distributed processing if needed.

### 🔹 **Assumptions**
- Each event has a **unique ID**.
- Events are **appended only** to the JSONL file (no in-place edits).
- No external modifications are made to the event file while processing is running.

---

## 📈 Scaling the System for Millions of Events per Hour
If this needed to support real-time processing at a massive scale, here’s what I’d do:

- Use a streaming platform like **Apache Kafka** or **AWS Kinesis** instead of reading from a file.
- Add **event partitioning** so that events can be split and processed in parallel.
- Use **distributed frameworks** like **Apache Flink** or **Spark Structured Streaming** for real-time processing across multiple machines.
- Store data in cloud-based storage systems like **S3, BigQuery, or Snowflake** for long-term storage and analytics.
- Implement **sharding and worker queues** to distribute the workload efficiently.

---

## 🔄 How the Approach Would Change with More Tools
If I had access to additional tools such as **a database, logs, or real-time processing frameworks**, my approach would be significantly more robust and scalable:

### **1️⃣ Using a Database for Event Storage**
- Instead of storing events in a JSONL file, I would store them in a **SQL (PostgreSQL, MySQL) or NoSQL (MongoDB, DynamoDB) database**.
- This would allow **faster lookups, indexing, and query-based analysis**.
- **State persistence would be more reliable** and **concurrent processing** would be much easier to handle.

### **2️⃣ Implementing a Real-Time Streaming System**
- If real-time processing was required, I would leverage **Apache Kafka, AWS Kinesis, or Google Pub/Sub** for **event ingestion and streaming**.
- This would allow for distributed event processing using **consumer groups and parallel workers**.

### **3️⃣ Improved Logging & Monitoring**
- Using **Elasticsearch + Kibana**, AWS CloudWatch, or Prometheus, I could **track event failures, latencies, and system health**.
- Logs would help in **debugging missed or incorrectly processed events**, reducing the need for manual checkpoint handling.

### **4️⃣ Parallel Processing for Performance Optimization**
- Instead of single-threaded processing, I would implement **multi-threading (Python’s multiprocessing) or distributed processing (Apache Spark, Flink)**.
- This would allow the system to handle **millions of events per hour** by **scaling horizontally** across multiple nodes.

---

## 🛠 Running the Solution in VS Code
### **Prerequisites**
- **Python 3.x installed** (Check with `python --version`)
- **VS Code installed** with the **Python extension**

### **Steps to Run**
1️⃣ Clone the repository:
   ```sh
   git clone <https://github.com/sreekarvss29/Linq-Data-Take-Home.git>
   ```

2️⃣ Run the event processing script manually:
   ```sh
   python event_processor.py
   ```

3️⃣ Run the **test suite** to verify functionality:
   ```sh
   python -m unittest test_event_processor.py
   ```
   This will execute all test cases and print **detailed state outputs** in the terminal.

---

## 🔥 Why This Solution? (Key Highlights)
✔ **Fault Tolerant** – Uses checkpointing to prevent data loss in case of failures.  
✔ **Efficient** – Processes large event logs efficiently with minimal resource consumption.  
✔ **Handles Edge Cases** – Deals with duplicates, unordered events, and crash recovery seamlessly.  
✔ **Scalable** – Can be extended to handle real-time streaming data with minimal changes.  
✔ **Modular Testing** – `unittest` ensures correctness, and print statements give **clear visibility of outputs**.  
✔ **VS Code Compatible** – Fully tested and can be debugged using **breakpoints in VS Code**.  

---

**Thank you for reviewing my submission!** I had fun working on this challenge and would love to discuss more in an interview or follow-up call. 🚀


