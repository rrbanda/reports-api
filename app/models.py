# File: app/models.py
from pydantic import BaseModel, Field
from typing import Dict

class Info(BaseModel):
    PatientID: str
    PatientName: str
    PatientAge: str
    StudyDate: str

class Femur(BaseModel):
    Right_femur: str = Field(alias="Right femur")
    Left_femur: str = Field(alias="Left femur")
    Difference: str

class Tibia(BaseModel):
    Right_tibia: str = Field(alias="Right tibia")
    Left_tibia: str = Field(alias="Left tibia")
    Difference: str

class Total(BaseModel):
    Total_right: str = Field(alias="Total right")
    Total_left: str = Field(alias="Total left")
    Difference: str

class PixelDistance(BaseModel):
    Left_femur: int = Field(alias="Left femur")
    Left_tibia: int = Field(alias="Left tibia")
    Right_femur: int = Field(alias="Right femur")
    Right_tibia: int = Field(alias="Right tibia")

class Details(BaseModel):
    AccessionNumber: str
    StudyDescription: str
    SeriesDescription: str
    BodyPartExamined: str
    FieldOfViewDimensions: str
    StationName: str

class MeasurementData(BaseModel):
    info: Info
    femur: Femur
    tibia: Tibia
    total: Total
    pixel_distance: PixelDistance
    details: Details

class PatientData(BaseModel):
    data: Dict[str, MeasurementData]
