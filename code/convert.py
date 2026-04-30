import sys
import csv
import json
from datetime import datetime, timezone


def process_csv(input_stream):
    """
    This parses RFC8805 format CSV and returns a JSON formatted string.
    """
    # Get current time in UTC, formatted as ISO 8601
    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    json_records = []

    reader = csv.DictReader(
        input_stream, fieldnames=["ip_prefix", "alpha2code", "region", "city"]
    )

    for row in reader:
        # Skip comment lines
        if row["ip_prefix"].startswith("#"):
            continue

        # Construct the dictionary using the keys from the CSV header
        record = {
            "ip_prefix": row.get("ip_prefix", ""),
            "alpha2code": row.get("alpha2code", ""),
            "region": row.get("region", ""),
            "city": row.get("city", ""),
            "last_updated": current_time,
        }

        json_records.append(record)

    return json.dumps(json_records, indent=2)


if __name__ == "__main__":
    output = process_csv(sys.stdin)
    print(output)
