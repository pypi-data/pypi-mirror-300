from field_manager_api.config.config import DATA_URL
from field_manager_api.config.request_handler import get_request_handler
from pydantic import BaseModel
from datetime import datetime
import uuid
import pandas as pd


class Method(BaseModel):
    project_id: uuid.UUID
    location_id: uuid.UUID
    method_id: uuid.UUID
    method_type_id: int
    name: str
    remarks: str | None = None

    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str

    depth_top: float
    depth_base: float

    stopcode: int | None = None
    headers: dict | None = None

    _method_data: pd.DataFrame | None = None

    @property
    def method_type(self):
        url = f"{DATA_URL}/method_types/{self.method_type_id}"
        request_handler = get_request_handler
        method_type = request_handler(url=url, headers=self.headers)
        return MethodType(**method_type)

    @property
    def data(self):
        if self._method_data is None:
            self._method_data = self.fetch_and_set_method_data(headers=self.headers)
        return self._method_data

    def fetch_and_set_method_data(self, headers: dict):
        """Fetch and set methods for the location"""
        url = f"{DATA_URL}/projects/{self.project_id}/locations/{self.location_id}/methods/{self.method_id}/data"
        request_handler = get_request_handler
        method_data_lines = request_handler(url=url, headers=headers)
        df = pd.DataFrame(method_data_lines)

        remove_cols = [
            "method_data_id",
            "method_id",
            "method_type_id",
        ]
        for col in remove_cols:
            if col in df.columns:
                df.drop(columns=[col], inplace=True)

        # Reorder columns
        cols = list(df.columns)
        if "depth" in cols:  # place depth first
            cols.remove("depth")
            cols = ["depth"] + cols

        back_cols = ["created_at", "created_by", "updated_by"]
        for back_col in back_cols:
            if back_col in cols:
                cols.remove(back_col)
                cols = cols + [back_col]
        df = df[cols]

        return df

    class Config:
        extra = "allow"
        # TODO: Is this a good idea..?


class MethodType(BaseModel):
    method_type_id: int
    name: str
    description: str
