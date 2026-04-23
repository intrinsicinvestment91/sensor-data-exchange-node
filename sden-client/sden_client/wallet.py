import httpx


class SDENWallet:
    """Wraps a LNbits wallet for paying Lightning invoices outbound.

    Requires an admin key (not invoice/read key) to pay outgoing invoices.
    Set LNBITS_URL and LNBITS_API_KEY in env, or pass explicitly.
    """

    def __init__(self, lnbits_url: str, api_key: str) -> None:
        self._url = lnbits_url.rstrip("/")
        self._headers = {"X-Api-Key": api_key}
        self._client = httpx.Client(timeout=30.0)

    def pay_invoice(self, bolt11: str) -> None:
        """Pay a BOLT11 invoice. Raises httpx.HTTPStatusError on failure."""
        resp = self._client.post(
            f"{self._url}/api/v1/payments",
            headers=self._headers,
            json={"out": True, "bolt11": bolt11},
        )
        resp.raise_for_status()

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "SDENWallet":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
