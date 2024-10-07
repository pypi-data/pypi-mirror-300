from dataclasses import dataclass
from . import enums

@dataclass
class VerificationStatus:
    status: enums.VerificationResult
    updated_at: int
    code_entered: str | None = None

@dataclass
class DeliveryStatus:
    status: enums.MessageDelivery
    updated_at: int

@dataclass
class RequestStatus:
    request_id: str
    phone_number: str
    request_cost: float
    remaining_balance: float | None = None
    delivery_status: DeliveryStatus | None = None
    verification_status: VerificationStatus | None = None
    payload: str | None = None
