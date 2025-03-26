# Data Engineer Take-Home Assessment

## Overview
This repository contains my solution to the Linq Data Engineer Take-Home Assessment. The objective of this task is to design a **fault-tolerant event processing system** that efficiently processes **real-time event logs**, maintains **data consistency**, and recovers from **failures and crashes** without relying on a traditional database.

This document provides a **detailed explanation** of the implementation, testing setup, scalability considerations, and instructions for running the solution in **VS Code**.

---

## 🚀 Approach
### 1️⃣ **Event Processing Mechanism**
- Events are stored and processed from a **JSONL file** (`events.jsonl`).
- Each event is uniquely identified by an **`id`**, along with `category` and `value` attributes.
- The processor reads, validates, and processes each event, ensuring **duplicates are skipped**.

### 2️⃣ **Checkpointing & Recovery Strategy**
- A **checkpoint file** (`checkpoint.json`) is used to store the last processing state.
- Upon restart, the system reloads the checkpoint and **resumes from the last successfully processed event**.
- This ensures **fault tolerance and prevents duplicate processing**.

### 3️⃣ **Handling Duplicates & Out-of-Order Events**
- The system maintains a **set of processed event IDs** to avoid reprocessing.
- Events are **sorted by `id`** before processing to ensure correct order.

### 4️⃣ **Testing with `unittest`**
- All test cases are written in `test_event_processor.py` using **Python's `unittest` framework**. 
- Print statements in test cases allow **better visibility of state changes**.

---

## 🔍 Scenarios & Testing
The solution was thoroughly tested under multiple conditions:

✅ **Scenario 1: Initial Processing** – Ensures that the processor correctly processes all events when run for the first time.  
✅ **Scenario 2: Simulated Crash & Recovery** – Ensures that the processor correctly resumes processing from the last checkpoint.  
✅ **Scenario 3: Duplicate Event Handling** – Ensures that duplicate events are ignored and not reprocessed.  
✅ **Scenario 4: Out-of-Order Events** – Ensures that events are processed in correct order, even if they arrive out of sequence.  
✅ **Scenario 5: Large Volume Handling** – Tests how the processor handles a large dataset (1,000+ events).  

---

## ⚖️ Trade-offs & Assumptions
### 🔹 **Trade-offs**
- **File-based storage**: Instead of a database, this implementation relies on JSON files. This is simple but may not scale well for extremely large datasets.
- **Single-threaded processing**: The script processes events sequentially. If performance is a concern, **parallel processing or a distributed system** can be implemented.

### 🔹 **Assumptions**
- Each event has a **unique ID**.
- Events **arrive in an append-only manner** in `events.jsonl`.
- The event log will **not be externally modified** while processing is in progress.

---

## 📈 Scaling the System for Millions of Events per Hour
If this system were required to handle millions of events per hour, I would implement the following changes:

✔ **Use Apache Kafka or AWS Kinesis** – Instead of batch file processing, I would stream events in real-time.
✔ **Implement Database Sharding** – To distribute event storage and avoid single database bottlenecks.
✔ **Introduce Event Partitioning** – Ensuring that different categories of events are processed in parallel by separate workers.
✔ **Leverage Distributed Computing (Spark/Flink)** – To process massive amounts of data efficiently across clusters.
✔ **Use Cloud-Based Storage (S3, BigQuery, Snowflake)** – To store large volumes of event history and allow efficient querying.

These improvements would allow the system to process high-volume, real-time event data efficiently while maintaining **fault tolerance, high availability, and performance**.

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

4️⃣ **Run tests using VS Code UI**:
   - Open VS Code and ensure the **Python extension** is installed.
   - Open **Command Palette (`Ctrl+Shift+P`)** → Select **"Python: Configure Tests"** → Choose **unittest**.
   - Open the **Testing Panel (`Ctrl+Shift+T`)** → Click **Run All Tests**.

---

## 🔥 Why This Solution? (Key Highlights)
✔ **Fault Tolerant** – Uses checkpointing to prevent data loss in case of failures.  
✔ **Efficient** – Processes large event logs efficiently with minimal resource consumption.  
✔ **Handles Edge Cases** – Deals with duplicates, unordered events, and crash recovery seamlessly.  
✔ **Scalable** – Can be extended to handle real-time streaming data with minimal changes.  
✔ **Modular Testing** – `unittest` ensures correctness, and print statements give **clear visibility of outputs**.  
✔ **VS Code Compatible** – Fully tested and can be debugged using **breakpoints in VS Code**.  

---

**Thank you for reviewing my submission!** 🚀 Looking forward to your feedback.
