# 🌍 CO₂ Emissions Data Pipeline
Serverless AWS pipeline for processing and analysing annual CO₂ emissions data (2010–2024)  

This project ingests a curated global CO₂ emissions dataset, processes it through a serverless ETL pipeline, stores structured results in DynamoDB, and publishes analytics JSON for downstream APIs and dashboards.  

The architecture is lightweight, cost‑efficient, and designed for real‑time updates whenever new data is uploaded to S3.

---
### Columns

| Column | Description |
|--------|-------------|
| Entity | Country name |
| Code | ISO‑3166 alpha‑3 code |
| Year | Year of measurement |
| Annual CO₂ emissions | Emissions in tonnes (integer) |

The dataset is intentionally lightweight to keep the pipeline fast and inexpensive while still supporting meaningful global emissions insights.

---

## 📦 Dataset Overview

The pipeline processes a curated CSV containing:

- 34 countries + World aggregate  
- 15 years of data (2010–2024)  
- 526 total rows (including header)

---

## 🏗 Architecture Diagram

![FPI Data Pipeline](architecture/co2_pipeline_architecture.drawio.png)

---

## 🔁 How the Pipeline Works

1. **Raw Data Ingestion (S3 Raw bucket)**  
Raw CSV files are sourced and uploaded to an S3 Bucket. This will be the designated landing zone for unprocessed data.

3. **Transformation (Lambda Function)**  
A Lambda function is triggered to clean, parse, and transform the raw FPI records, preparing them for fast lookups in DynamoDB and analytics processing in S3.

4. **Fast Lookups (DynamoDB Processed Table)**  
Transformed records are stored in DynamoDB for low-latency access and API-driven use cases.

5. **SQL Querying (Athena)**  
Processed data is exported to an S3 bucket dedicated for analytics in a query-friendly format.

6. **Visualisation (QuickSight Dashboard)**
QuickSight connects to Athena to build interactive, palatable, visual dashboards  
**NOTE: --- dashed lined arrows indicate queried data, not movement of data**

---

## 📈 Future Improvements

- Add Glue Crawler for schema automation
- Add Api Gateway + Lambda for realtime lookups
- Add CloudWatch alarms and metrics
- Add S3 lifecycle policies
- Add CI/CD pipeline for Lambda deployments

---

## 📜 License

MIT License
