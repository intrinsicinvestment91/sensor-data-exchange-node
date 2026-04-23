import random
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class RawReading:
    value: float
    units: str
    quality_score: float
    timestamp_utc: str


class SensorReader(ABC):
    @abstractmethod
    def read(self) -> RawReading:
        ...

    @property
    @abstractmethod
    def sensor_type(self) -> str:
        ...


class MockSensorReader(SensorReader):
    """Produces realistic randomized readings with configurable drift.

    Works with no hardware. Required for CI, grant evaluators, and contributors.
    """

    _SENSORS: dict[str, dict] = {
        "temperature": {"base": 22.0, "drift": 2.0, "units": "celsius"},
        "humidity": {"base": 55.0, "drift": 5.0, "units": "percent"},
        "pressure": {"base": 1013.25, "drift": 3.0, "units": "hPa"},
        "co2": {"base": 400.0, "drift": 20.0, "units": "ppm"},
    }

    def __init__(self, sensor_type: str = "temperature", seed: int | None = None) -> None:
        if sensor_type not in self._SENSORS:
            raise ValueError(
                f"Unknown sensor type '{sensor_type}'. "
                f"Available: {list(self._SENSORS)}"
            )
        self._sensor_type = sensor_type
        self._config = self._SENSORS[sensor_type]
        self._rng = random.Random(seed)

    @property
    def sensor_type(self) -> str:
        return self._sensor_type

    def read(self) -> RawReading:
        from datetime import datetime, timezone

        drift = self._rng.uniform(-self._config["drift"], self._config["drift"])
        value = round(self._config["base"] + drift, 2)
        quality = round(self._rng.uniform(0.90, 1.00), 4)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        return RawReading(
            value=value,
            units=self._config["units"],
            quality_score=quality,
            timestamp_utc=ts,
        )


class DHT22Reader(SensorReader):
    """Physical DHT22 sensor reader (requires hardware + Adafruit-DHT or adafruit-circuitpython-dht)."""

    def __init__(self, pin: int = 4) -> None:
        self._pin = pin
        self._sensor_type = "temperature"  # DHT22 also reads humidity; extend as needed
        try:
            import adafruit_dht
            import board

            self._device = adafruit_dht.DHT22(getattr(board, f"D{pin}"))
        except ImportError as exc:
            raise RuntimeError(
                "adafruit-circuitpython-dht not installed. "
                "Set USE_MOCK_SENSOR=true for development."
            ) from exc

    @property
    def sensor_type(self) -> str:
        return self._sensor_type

    def read(self) -> RawReading:
        from datetime import datetime, timezone

        for _ in range(3):
            try:
                value = self._device.temperature
                if value is not None:
                    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                    return RawReading(
                        value=round(float(value), 2),
                        units="celsius",
                        quality_score=1.0,
                        timestamp_utc=ts,
                    )
            except RuntimeError:
                time.sleep(0.5)
        raise RuntimeError("DHT22 read failed after 3 attempts")


def make_reader(sensor_type: str, use_mock: bool) -> SensorReader:
    if use_mock:
        return MockSensorReader(sensor_type)
    return DHT22Reader()
