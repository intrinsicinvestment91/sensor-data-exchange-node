"""Buy a signed temperature reading from a SDEN producer node.

Requires:
  pip install sden-client
  LNBITS_URL and LNBITS_API_KEY set in environment (admin key for outgoing payments)
"""

import os
from sden_client import SDENBuyer, SDENWallet

wallet = SDENWallet(
    lnbits_url=os.environ["LNBITS_URL"],
    api_key=os.environ["LNBITS_API_KEY"],
)

with SDENBuyer("http://localhost:8080", wallet=wallet) as buyer:
    reading = buyer.buy(sensor_type="temperature")

assert reading.verify(), "Signature verification failed"
print(f"Paid {buyer.last_price_sats} sats.")
print(f"{reading.sensor_type.capitalize()}: {reading.value} {reading.units}")
print(f"Quality: {reading.quality_score:.0%} | Producer: {reading.producer_did}")
