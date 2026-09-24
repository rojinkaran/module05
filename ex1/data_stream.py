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


class DataStream:
    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)

    def process_stream(self, stream: list[typing.Any]) -> None:
        for element in stream:
            for proc in self.processors:
                if proc.validate(element):
                    proc.ingest(element)
                    break

            else:
                print(
                    f"DataStream error - Can't process element in stream:"
                    f"{element}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")

        if not self.processors:
            print("No processor found, no data")
            return

        for proc in self.processors:
            name = proc.__class__.__name__.replace("Processor", " Processor")
            print(
                f"{name}: total {proc.total_processed} items processed, "
                f"remaining {len(proc.data)} on processor"
            )


print("=== Code Nexus - Data Stream ===\n")
print("Initialize Data Stream...")

data_stream = DataStream()

data_stream.print_processors_stats()

print()

print("Registering Numeric Processor\n")

numeric = NumericProcessor()

data_stream.register_processor(numeric)

batch = [
    "Hello world",
    [3.14, -1, 2.71],
    [
        {
            "log_level": "WARNING",
            "log_message": "Telnet access! Use ssh instead"
        },
        {
            "log_level": "INFO",
            "log_message": "User wil is connected"
        }
    ],
    42,
    ["Hi", "five"]
]

print(f"Send first batch of data on stream: {batch}")

data_stream.process_stream(batch)

data_stream.print_processors_stats()

print()

print("Registering other data processors")

text = TextProcessor()
log = LogProcessor()

data_stream.register_processor(text)
data_stream.register_processor(log)

print("Send the same batch again")
data_stream.process_stream(batch)

data_stream.print_processors_stats()

print()

print(
    "Consume some elements from the data processors: "
    "Numeric 3, Text 2, Log 1"
)

for _ in range(3):
    numeric.output()

for _ in range(2):
    text.output()

log.output()

data_stream.print_processors_stats()
