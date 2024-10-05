
class OHLCV():
    def __init__(self, measured_at: int, open: int, high: int, low: int, close: int, volume: int) -> None:
        self.measured_at = measured_at # millis since epoch

        # all monetary values in cents
        self.open = open
        self.high = high 
        self.low = low 
        self.close = close

        self.volume = volume

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            measured_at=data['measured_at'],
            open=data['open'],
            high=data['high'],
            low=data['low'],
            close=data['close'],
            volume=data['volume']
        )