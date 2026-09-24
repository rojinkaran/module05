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

        if not self.validate(data):
            raise ValueError("Improper numeric data")

        if not isinstance(data, list):
            self.data.append((self.total_processed, str(data)))
            self.total_processed += 1
        else:
            for item in data:
                self.data.append((self.total_processed, str(item)))
                self.total_processed += 1


class TextProcessor(DataProcessor):

    def validate(self, data: typing.Any) -> bool:

        if isinstance(data, str):
            return True

        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)

        return False

    def ingest(self, data: str | list[str]) -> None:

        if not self.validate(data):
            raise ValueError("Improper text data")

        if isinstance(data, str):
            self.data.append((self.total_processed, data))
            self.total_processed += 1
        else:
            for item in data:
                self.data.append((self.total_processed, item))
                self.total_processed += 1


class LogProcessor(DataProcessor):

    def validate(self, data: typing.Any) -> bool:

        if isinstance(data, dict):
            return all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in data.items()
            )

        if isinstance(data, list):
            return all(
                isinstance(item, dict)
                and all(
                    isinstance(key, str) and isinstance(value, str)
                    for key, value in item.items()
                )
                for item in data
            )

        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:

        if not self.validate(data):
            raise ValueError("Improper log data")

        if isinstance(data, dict):

            if "log_level" in data and "log_message" in data:
                log_text = f"{data['log_level']}: {data['log_message']}"
            else:
                log_text = str(data)

            self.data.append((self.total_processed, log_text))
            self.total_processed += 1

        else:
            for item in data:

                if "log_level" in item and "log_message" in item:
                    log_text = f"{item['log_level']}: {item['log_message']}"
                else:
                    log_text = str(item)

                self.data.append((self.total_processed, log_text))
                self.total_processed += 1


print("=== Code Nexus - Data Processor ===\n")

print("Testing Numeric Processor...")

numeric = NumericProcessor()

print(f"Trying to validate input '42': {numeric.validate(42)}")
print(f"Trying to validate input 'Hello': {numeric.validate('Hello')}")

print("Test invalid ingestion of string 'foo' without prior validation:")

try:
    numeric.ingest("foo")
except Exception as e:
    print(f"Got exception: {e}")


print("Processing data: [1, 2, 3, 4, 5]")
numeric.ingest([1, 2, 3, 4, 5])
print("Extracting 3 values...")

for _ in range(3):
    rank, value = numeric.output()
    print(f"Numeric value {rank}: {value}")

print()

print("Testing Text Processor...")
text = TextProcessor()
print(f"Trying to validate input '42': {text.validate(42)}")

print("Processing data: ['Hello', 'Nexus', 'World']")
text.ingest(["Hello", "Nexus", "World"])

print("Extracting 1 value...")
rank, value = text.output()
print(f"Text value {rank}: {value}\n")

print("Testing Log Processor...")
log = LogProcessor()
print(f"Trying to validate input 'Hello': {log.validate('Hello')}")

log_data = [
    {
        "log_level": "NOTICE",
        "log_message": "Connection to server"
    },
    {
        "log_level": "ERROR",
        "log_message": "Unauthorized access!!"
    }
]

print(f"Processing data: {log_data}")
log.ingest(log_data)
print("Extracting 2 values...")

for _ in range(2):
    rank, value = log.output()
    print(f"Log entry {rank}: {value}")
