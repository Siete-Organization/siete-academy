from pydantic import BaseModel, HttpUrl


class LiveSessionUpsert(BaseModel):
    module_window_id: int
    title: str
    zoom_url: HttpUrl
    recording_url: HttpUrl | None = None


class LiveSessionOut(BaseModel):
    id: int
    module_window_id: int
    title: str
    zoom_url: str
    recording_url: str | None

    class Config:
        from_attributes = True
