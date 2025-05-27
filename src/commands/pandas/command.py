import csv
from dataclasses import dataclass
from typing import List, Any

@dataclass(frozen=True)
class ReadCSVCommand:
    """
    Command to read a CSV file into a pandas DataFrame.
    """
    file_path: str
    dialect: csv.Dialect = None
    header: int = 0
    parse_dates: List[str] = None
    dayfirst: bool = False

@dataclass(frozen=True)
class ComputePredictedAudienceCommand:
    """
    Command to compute rolling median 'predicted_audience' by signal, program_code, weekday.
    """
    df: Any  # pandas.DataFrame
    signal_col: str
    program_code_col: str
    date_col: str
    average_col: str
    window: int = 4

@dataclass(frozen=True)
class MergeAvailableTimeCommand:
    """
    Command to merge available time slots with predicted audience.
    """
    slots_df: Any  # pandas.DataFrame
    predictions_df: Any  # pandas.DataFrame
    left_on: List[str]
    right_on: List[str]
    how: str = "left"
