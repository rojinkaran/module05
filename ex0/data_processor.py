import abc
import typing


class DataProcessor(abc.ABC):

    def __init__(self) -> None:
        self.data: list[tuple[int, str]] = []
        self.total_processed: int = 0

    @abc.abstractmethod
    def validate(self, data: typing.Any) -> bool:
        pass

    @abc.abstractmethod
    def ingest(self, data: typing.Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        return self.data.pop(0)

class NumericProcessor(DataProcessor):

    def validate(self, data: typing.Any) -> bool:

        if isinstance(data, (int, float)):
            return True

        if isinstance(data, list):
            return all(isinstance(item, (int, float)) for item in data)

        return False


    def ingest(self, data: int | float | list[int | float]) -> None:
        


