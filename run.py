import argparse
import json

if __name__ == "__main__":
    from src.lambdas.import_csv_lambda import handler

    parser = argparse.ArgumentParser(description="Run the import_csv_lambda handler with a mock event.")
    parser.add_argument("--event-file", type=str, help="Path to the mock event JSON file.")
    args = parser.parse_args()

    if args.event_file:
        with open(args.event_file, "r") as f:
            event = json.load(f)
    else:
        # Default mock event
        event = {
            "Records": [
                {
                    "s3": {
                        "bucket": {"name": "example-bucket"},
                        "object": {"key": "example.csv"}
                    }
                }
            ]
        }

    context = None
    result = handler(event, context)
    print(result)
