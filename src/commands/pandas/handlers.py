from dataclasses import dataclass
import pandas as pd
from typing import Any
from ..handlers import Handler
from .command import ReadCSVCommand, ComputePredictedAudienceCommand, MergeAvailableTimeCommand

@dataclass(frozen=True)
class PandasSummarizeCommand:
    data_frame: str
    column: str
    operation: str


    def __str__(self):
        return f"PandasReadCSVCommand(file_path={self.file_path}, delimiter={self.delimiter}, header={self.header}, index_col={self.index_col}, usecols={self.usecols}, dtype={self.dtype})"

class ReadCSVHandler(Handler):
    def execute(self, command: ReadCSVCommand) -> pd.DataFrame:
        """
        Reads a CSV file into a pandas DataFrame using provided parse_dates and dayfirst.
        """
        return pd.read_csv(
            command.file_path,
            dialect=command.dialect,
            parse_dates=command.parse_dates,
            dayfirst=command.dayfirst
        )

class ComputePredictedAudienceHandler(Handler):
    def execute(self, command: ComputePredictedAudienceCommand) -> pd.DataFrame:
        df = command.df.copy()

        # 1) make sure the average‐audience column is float
        df[command.average_col] = pd.to_numeric(df[command.average_col],
                                                errors="coerce")

        # 2) extract weekday
        df['weekday'] = df[command.date_col].dt.day_name()

        # 3) sort for rolling
        df = df.sort_values([
            command.signal_col,
            command.program_code_col,
            'weekday',
            command.date_col
        ])

        # 4) compute shifted rolling‐median via transform
        df['predicted_audience'] = (
            df
            .groupby([command.signal_col,
                      command.program_code_col,
                      'weekday'])[command.average_col]
            .transform(lambda s: s
                       .rolling(window=command.window, min_periods=1)
                       .median())
        )

        return df

class MergeAvailableTimeHandler(Handler):
    def execute(self, command: MergeAvailableTimeCommand) -> pd.DataFrame:
        """
        Merges available time slots with predicted audience DataFrame.
        """
        merged = command.slots_df.merge(
            command.predictions_df,
            left_on=command.left_on,
            right_on=command.right_on,
            how=command.how
        )
        # select the final schema
        return merged[[
            'signal', 'program_code', 'weekday', 'exhibition_date', 'available_time', 'predicted_audience'
        ]]