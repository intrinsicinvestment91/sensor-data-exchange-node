import logging
import os

import uvicorn
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s — %(message)s")

from sden.did_identity import DIDIdentity
from sden.pricing import FlatPricingEngine
from sden.sensor_agent import SensorAgent, build_app
from sden.sensor_reader import make_reader


def main() -> None:
    sensor_type = os.environ.get("SENSOR_TYPE", "temperature")
    use_mock = os.environ.get("USE_MOCK_SENSOR", "true").lower() == "true"
    audit_db_path = os.environ.get("AUDIT_DB_PATH", "audit.db")
    key_path = os.environ.get("DID_KEY_PATH", "identity.pem")
    host = os.environ.get("SDEN_HOST", "0.0.0.0")
    port = int(os.environ.get("SDEN_PORT", "8080"))

    identity = DIDIdentity.load_or_generate(key_path)
    reader = make_reader(sensor_type, use_mock)
    pricing = FlatPricingEngine()
    agent = SensorAgent(
        sensor_reader=reader,
        pricing_engine=pricing,
        audit_db_path=audit_db_path,
        identity=identity,
    )
    app = build_app(agent)

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
