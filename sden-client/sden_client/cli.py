import json
import sys

import click

from sden_client.buyer import SDENBuyer
from sden_client.models import SensorReading
from sden_client.wallet import SDENWallet


@click.command()
@click.option("--url", required=True, help="Producer node URL (e.g. http://localhost:8080)")
@click.option("--type", "sensor_type", default="temperature", show_default=True, help="Sensor type to buy")
@click.option("--quantity", default=1, show_default=True, help="Number of readings")
@click.option("--lnbits-url", envvar="LNBITS_URL", default=None, help="LNbits instance URL [$LNBITS_URL]")
@click.option("--lnbits-key", envvar="LNBITS_API_KEY", default=None, help="LNbits admin API key [$LNBITS_API_KEY]")
@click.option(
    "--output",
    type=click.Choice(["human", "json"]),
    default="human",
    show_default=True,
    help="Output format",
)
@click.option(
    "--verify-only",
    type=click.Path(exists=True),
    default=None,
    help="Verify a saved reading JSON file without paying",
)
def main(url, sensor_type, quantity, lnbits_url, lnbits_key, output, verify_only):
    """Buy a signed sensor reading from a SDEN producer node."""

    # --verify-only: no payment, just check the signature on a saved reading
    if verify_only:
        try:
            with open(verify_only) as f:
                reading = SensorReading(**json.load(f))
        except Exception as exc:
            _err(output, f"Failed to load reading: {exc}")
            sys.exit(1)

        valid = reading.verify()
        if output == "json":
            click.echo(json.dumps({"valid": valid, "reading": reading.model_dump()}))
        else:
            status = "✓ signature verified" if valid else "✗ signature INVALID"
            click.echo(
                f"{reading.sensor_type.capitalize()}: {reading.value} {reading.units} "
                f"(quality: {reading.quality_score:.2f}) [{status}]"
            )
        sys.exit(0 if valid else 1)

    # Normal buy flow
    if not lnbits_url or not lnbits_key:
        raise click.UsageError(
            "LNBITS_URL and LNBITS_API_KEY are required "
            "(set via environment or --lnbits-url / --lnbits-key)"
        )

    try:
        wallet = SDENWallet(lnbits_url=lnbits_url, api_key=lnbits_key)
        with SDENBuyer(url, wallet=wallet) as buyer:
            if output == "human":
                click.echo(f"Requesting {sensor_type} reading from {url} …")

            reading = buyer.buy(sensor_type=sensor_type, quantity=quantity)
            price = buyer.last_price_sats

            if output == "json":
                click.echo(json.dumps(reading.model_dump()))
            else:
                click.echo(
                    f"Paid {price} sats. "
                    f"{reading.sensor_type.capitalize()}: {reading.value} {reading.units} "
                    f"(quality: {reading.quality_score:.2f}) [✓ signature verified]"
                )
    except Exception as exc:
        _err(output, str(exc))
        sys.exit(1)


def _err(output: str, message: str) -> None:
    if output == "json":
        click.echo(json.dumps({"error": message}), err=True)
    else:
        click.echo(f"Error: {message}", err=True)
