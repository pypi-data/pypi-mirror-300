"""ModelTemplateClass.py 

A template (interface-like) class for defining the expected methods of a model
NOTE: Every model will be a sub-class of this class
"""

from abc import ABC, abstractmethod
from typing import Union

from .ModelDataBlueprint import ModelDataBlueprint
from .PredictionResponse import PredictionResponse
from .InputData import InputData

class SAFTModelClass(ABC):
    @abstractmethod
    def predict(self, prediction_input: InputData) -> Union[PredictionResponse, None]:
        """
        Takes in dictionary of data points for prediction,
        returns a prediction response object
        """
        return None