
from .TradingStrategy import TradingStrategy
from .ModelDataBlueprint import ModelDataBlueprint

class ModelBlueprint():
    def __init__(self,
                 trading_strategy: TradingStrategy,
                 data_blueprint: ModelDataBlueprint) -> None:
        self.trading_strategy = trading_strategy
        self.data_blueprint = data_blueprint