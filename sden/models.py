from enum import IntEnum

from pydantic import BaseModel, Field, UUID4


class ErrorCode(IntEnum):
    INVALID_REQUEST_FORMAT = 100
    SENSOR_TYPE_NOT_AVAILABLE = 101
    INVOICE_NOT_FOUND = 102
    PAYMENT_NOT_VERIFIED = 103
    INVOICE_EXPIRED = 104
    DATA_UNAVAILABLE = 105


class QuoteRequest(BaseModel):
    request_id: UUID4
    sensor_type: str
    quantity: int = Field(default=1, ge=1)
    timestamp_utc: str
    buyer_did: str | None = None
    signature: str


class QuoteResponse(BaseModel):
    request_id: UUID4
    price_sats: int
    invoice: str
    invoice_expiry: int = 3600
    checking_id: str


class VerifyPaymentRequest(BaseModel):
    request_id: UUID4
    checking_id: str


class VerifyPaymentResponse(BaseModel):
    request_id: UUID4
    paid: bool


class SensorReading(BaseModel):
    producer_did: str
    sensor_type: str
    timestamp_utc: str
    value: float
    units: str
    quality_score: float = Field(ge=0.0, le=1.0)
    signature: str


class ErrorResponse(BaseModel):
    error_code: int
    message: str


class ProducerInfo(BaseModel):
    producer_did: str
    sensor_type: str
    price_sats: int
    version: str = "1.0"


class HealthResponse(BaseModel):
    status: str = "ok"
