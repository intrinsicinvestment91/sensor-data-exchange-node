# sden-client

Python buyer SDK for [SDEN](https://github.com/Intrinsicinvestment91/sensor-data-exchange-node) sensor data nodes.

```python
from sden_client import SDENBuyer, SDENWallet

wallet = SDENWallet(lnbits_url="https://...", api_key="...")
with SDENBuyer("https://producer.example.com", wallet=wallet) as buyer:
    reading = buyer.buy(sensor_type="temperature")

assert reading.verify()
print(f"{reading.value} {reading.units}")  # 22.4 celsius
```

Or from the command line:

```bash
sden-buy --url https://producer.example.com --type temperature
```

See the [main repository](https://github.com/Intrinsicinvestment91/sensor-data-exchange-node) for full documentation.
