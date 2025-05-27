from src.commands.bus import get_command_bus
from src.commands.s3 import S3ReadCommand
from src.commands.pandas import (
    ReadCSVCommand,
    ComputePredictedAudienceCommand,
    MergeAvailableTimeCommand
)
import io

from src.database.postgres import write_program_predictions

AUDIENCE_FILE = "tvaberta_program_audience.csv"
SLOTS_FILE = "tvaberta_inventory_availability.csv"

def _get_bucket_key_from_event(event):
    """
    Extracts bucket and key from the event.
    """
    bucket = event.get("Records")[0].get("s3").get("bucket").get("name")
    return bucket

def _get_dialect_from_csv_sample(sample):
    """
    Detects the delimiter used in the CSV file.
    """
    import csv
    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(sample)
    return dialect

def handler(event, context):
    """
    Lambda to import two CSVs from S3, compute predicted audience
    and merge with available time slots.
    Expects event keys: bucket, audience_key, slots_key
    """
    bus = get_command_bus()
    bucket = _get_bucket_key_from_event(event)

    # read audience CSV
    aud_body = bus.dispatch(
        S3ReadCommand(
            bucket=bucket,
            key=AUDIENCE_FILE
        )
    )
    aud_text = aud_body
    # Detect CSV dialect.
    dialect = _get_dialect_from_csv_sample(aud_text[:1024])
    audience_df = bus.dispatch(
        ReadCSVCommand(
            file_path=io.StringIO(aud_text),
            dialect=dialect,
            parse_dates=["exhibition_date", "program_start_time"],
            dayfirst=False
        )
    )

    # read available time slots CSV
    slots_body = bus.dispatch(
        S3ReadCommand(
            bucket=bucket,
            key=SLOTS_FILE
        )
    )
    slots_text = slots_body
    # Detect CSV dialect.
    slots_dialect = _get_dialect_from_csv_sample(slots_text[:1024])
    # Read available time slots CSV
    slots_df = bus.dispatch(
        ReadCSVCommand(
            file_path=io.StringIO(slots_text),
            dialect=slots_dialect,
            parse_dates=["date"],
            dayfirst=True
        )
    )

    # compute predicted audience
    pred_df = bus.dispatch(
        ComputePredictedAudienceCommand(
            df=audience_df,
            average_col="average_audience",
            date_col="exhibition_date",
            signal_col="signal",
            program_code_col="program_code",
            window=4
        )
    )

    slots_df["weekday"] = slots_df["date"].dt.day_name()

    # merge predictions with available time slots
    # Note: the merge is done on signal, program_code and weekday
    result_df = bus.dispatch(
        MergeAvailableTimeCommand(
            slots_df=slots_df,
            predictions_df=pred_df,
            left_on=["signal", "program_code", "weekday"],
            right_on=["signal", "program_code", "weekday"],
            how="left"
        )
    )
    
    
    write_program_predictions(result_df)
    
    return {
        "statusCode": 200,
    }


