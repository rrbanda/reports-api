# app/models.py

from pydantic import BaseModel, Field
from typing import Optional

class Info(BaseModel):
    PatientID: str = Field(..., example="71054xfdsar")
    PatientName: str = Field(..., example="SMITH^JANE")
    PatientAge: str = Field(..., example="012Y")
    StudyDate: str = Field(..., example="20240923")

class Femur(BaseModel):
    Right_femur: str = Field(..., alias="Right femur", example="41.8 cm")
    Left_femur: str = Field(..., alias="Left femur", example="42.0 cm")
    Difference: str = Field(..., example="00.2 cm, left longer 0.5%")

class Tibia(BaseModel):
    Right_tibia: str = Field(..., alias="Right tibia", example="34.5 cm")
    Left_tibia: str = Field(..., alias="Left tibia", example="34.3 cm")
    Difference: str = Field(..., example="00.2 cm, right longer 0.6%")

class Total(BaseModel):
    Total_right: str = Field(..., alias="Total right", example="76.3 cm")
    Total_left: str = Field(..., alias="Total left", example="76.3 cm")
    Difference: str = Field(..., example="00.0 cm, equal 0.0%")

class PixelDistance(BaseModel):
    Left_femur: int = Field(..., alias="Left femur", example=1892)
    Left_tibia: int = Field(..., alias="Left tibia", example=1544)
    Right_femur: int = Field(..., alias="Right femur", example=1886)
    Right_tibia: int = Field(..., alias="Right tibia", example=1555)

class Details(BaseModel):
    AccessionNumber: str = Field(..., example="100876169")
    StudyDescription: str = Field(..., example="XR HIPS TO ANKLES LEG MEASUREMENTS")
    SeriesDescription: str = Field(..., example="Lower limbs")
    BodyPartExamined: str = Field(..., example="LEG")
    FieldOfViewDimensions: str = Field(..., example="[975, 391]")
    StationName: str = Field(..., example="EOSRM7")

class PatientRecord(BaseModel):
    study_id: str = Field(..., example="61928-1.2.250.1.118.3.1305.235.1.8008.46.1727122139")
    info: Info
    femur: Femur
    tibia: Tibia
    total: Total
    pixel_distance: PixelDistance
    details: Details

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "study_id": "61928-1.2.250.1.118.3.1305.235.1.8008.46.1727122139",
                "info": {
                    "PatientID": "71054xfdsar",
                    "PatientName": "SMITH^JANE",
                    "PatientAge": "012Y",
                    "StudyDate": "20240923"
                },
                "femur": {
                    "Right femur": "41.8 cm",
                    "Left femur": "42.0 cm",
                    "Difference": "00.2 cm, left longer 0.5%"
                },
                "tibia": {
                    "Right tibia": "34.5 cm",
                    "Left tibia": "34.3 cm",
                    "Difference": "00.2 cm, right longer 0.6%"
                },
                "total": {
                    "Total right": "76.3 cm",
                    "Total left": "76.3 cm",
                    "Difference": "00.0 cm, equal 0.0%"
                },
                "pixel_distance": {
                    "Left femur": 1892,
                    "Left tibia": 1544,
                    "Right femur": 1886,
                    "Right tibia": 1555
                },
                "details": {
                    "AccessionNumber": "100876169",
                    "StudyDescription": "XR HIPS TO ANKLES LEG MEASUREMENTS",
                    "SeriesDescription": "Lower limbs",
                    "BodyPartExamined": "LEG",
                    "FieldOfViewDimensions": "[975, 391]",
                    "StationName": "EOSRM7"
                }
            }
        }
