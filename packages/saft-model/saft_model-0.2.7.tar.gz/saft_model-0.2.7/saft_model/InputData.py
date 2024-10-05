
from typing import List

from saft_model.classes.TimeInterval import TimeInterval
from saft_model.classes.OHLCV import OHLCV

class InitialData():
    def __init__(self, name: str, ticker: str, time_interval: TimeInterval, measurements: List[OHLCV]) -> None:
        self.name = name # unique identifier
        self.ticker = ticker
        self.time_interval = time_interval
        self.measurements = measurements
    
    @classmethod
    def from_dict(cls, data: dict):
        measurements = [OHLCV.from_dict(measurement) for measurement in data['measurements']]
        return cls(
            name=data['name'],
            ticker=data['ticker'],
            time_interval=data['time_interval'],
            measurements=measurements
        )

class ReoccurData():
    def __init__(self, ticker: str, time_interval: TimeInterval, measurements: List[OHLCV]) -> None:
        self.ticker = ticker
        self.time_interval = time_interval
        self.measurements = measurements
    
    @classmethod
    def from_dict(cls, data: dict):
        measurements = [OHLCV.from_dict(measurement) for measurement in data['measurements']]
        return cls(
            ticker=data['ticker'],
            time_interval=data['time_interval'],
            measurements=measurements
        )

class InputData():
    def __init__(self, initial_data: List[InitialData], reoccur_data: List[ReoccurData]) -> None:
        self.initial_data: List[InitialData] = initial_data
        self.reoccur_data: List[ReoccurData] = reoccur_data

    @classmethod
    def from_dict(cls, data: dict):
        initial_measurements = [InitialData.from_dict(initial) for initial in data['initial_data']]
        reoccur_measurements = [ReoccurData.from_dict(reoccur) for reoccur in data['reoccur_data']]
        return cls(
            initial_data = initial_measurements,
            reoccur_data = reoccur_measurements
        )