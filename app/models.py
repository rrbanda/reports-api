from pydantic import BaseModel
from typing import Dict

# Model for the "info" section of the patient data
class Info(BaseModel):
    PatientID: str
    PatientName: str
    PatientAge: str
    StudyDate: str

# Model for the "femur" measurements
class Femur(BaseModel):
    Right_femur: str
    Left_femur: str
    Difference: str

# Model for the "tibia" measurements
class Tibia(BaseModel):
    Right_tibia: str
    Left_tibia: str
    Difference: str

# Model for the "total" measurements
class Total(BaseModel):
    Total_right: str
    Total_left: str
    Difference: str

# Model for the "pixel_distance" section
class PixelDistance(BaseModel):
    Left_femur: int
    Left_tibia: int
    Right_femur: int
    Right_tibia: int

# Model for the "details" section of the patient data
class Details(BaseModel):
    AccessionNumber: str
    StudyDescription: str
    SeriesDescription: str
    BodyPartExamined: str
    FieldOfViewDimensions: str
    StationName: str

# Main model to combine all the above data
class PatientData(BaseModel):
    info: Info
    femur: Femur
    tibia: Tibia
    total: Total
    pixel_distance: PixelDistance
    details: Details

# The MeasurementData model, which will represent the complete dataset
class MeasurementData(BaseModel):
    data: Dict[str, PatientData]
