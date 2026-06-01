import boto3
import csv
import json
import os
from datetime import datetime

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

RAW_BUCKET = os.environ["RAW_BUCKET"]
ANALYTICS_BUCKET = os.environ["ANALYTICS_BUCKET"]
DDB_TABLE = os.environ["DDB_TABLE"]

table = dynamodb.Table(DDB_TABLE)

def lambda_handler(event, context):
    # 1. Extract S3 object info from event
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    # 2. Download raw CSV file
    obj = s3.get_object(Bucket=bucket, Key=key)
    raw_data = obj["Body"].read().decode("utf-8").splitlines()

    reader = csv.DictReader(raw_data)

    processed_items = []
    analytics_rows = []

    for row in reader:
        # 3. Clean + transform fields
        country = row["Country"].strip()
        category = row["Category"].strip()
        price = float(row["Price"])
        date = row["Date"]

        # Normalise date format
        date_iso = datetime.strptime(date, "%Y-%m-%d").date().isoformat()

        # DynamoDB item
        item = {
            "PK": f"{country}#{category}",
            "SK": date_iso,
            "Country": country,
            "Category": category,
            "Price": price,
            "Date": date_iso
        }

        processed_items.append(item)

        # Analytics row (JSON)
        analytics_rows.append(item)

    # 4. Write each item to DynamoDB
    with table.batch_writer() as batch:
        for item in processed_items:
            batch.put_item(Item=item)

    # 5. Write analytics-ready JSON to S3
    analytics_key = f"processed/{key.replace('.csv', '.json')}"
    s3.put_object(
        Bucket=ANALYTICS_BUCKET,
        Key=analytics_key,
        Body=json.dumps(analytics_rows),
        ContentType="application/json"
    )

    return {
        "statusCode": 200,
        "message": f"Processed {len(processed_items)} records from {key}"
    }
