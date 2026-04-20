from datetime import datetime

from pydantic import BaseModel


class CertificateOut(BaseModel):
    id: int
    user_id: int
    cohort_id: int
    verification_code: str
    pdf_url: str | None
    issued_at: datetime

    class Config:
        from_attributes = True


class CertificatePublic(BaseModel):
    """Datos del holder visibles en la página pública /certificate/{code}."""

    verification_code: str
    holder_name: str
    cohort_name: str
    issued_at: datetime
    valid: bool
