import pytest

from sden.sensor_reader import MockSensorReader


def test_mock_returns_valid_reading():
    reader = MockSensorReader("temperature", seed=42)
    reading = reader.read()
    assert reading.units == "celsius"
    assert 0.0 <= reading.quality_score <= 1.0
    assert reading.timestamp_utc.endswith("Z")


def test_mock_all_sensor_types():
    for sensor_type in ["temperature", "humidity", "pressure", "co2"]:
        reader = MockSensorReader(sensor_type)
        reading = reader.read()
        assert reading.value is not None


def test_mock_unknown_sensor_raises():
    with pytest.raises(ValueError, match="Unknown sensor type"):
        MockSensorReader("unknown_sensor")


def test_mock_seeded_is_deterministic():
    r1 = MockSensorReader("temperature", seed=0)
    r2 = MockSensorReader("temperature", seed=0)
    assert r1.read().value == r2.read().value
