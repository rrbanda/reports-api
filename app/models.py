from pydantic import BaseModel

class InfoModel(BaseModel):
    PatientID: str
    PatientName: str
    PatientAge: str
    StudyDate: str

class FemurModel(BaseModel):
    Right_femur: str
    Left_femur: str
    Difference: str

class TibiaModel(BaseModel):
    Right_tibia: str
    Left_tibia: str
    Difference: str

class TotalModel(BaseModel):
    Total_right: str
    Total_left: str
    Difference: str

class PixelDistanceModel(BaseModel):
    Left_femur: int
    Left_tibia: int
    Right_femur: int
    Right_tibia: int

class DetailsModel(BaseModel):
    AccessionNumber: str
    StudyDescription: str
    SeriesDescription: str
    BodyPartExamined: str
    FieldOfViewDimensions: str
    StationName: str

class PatientRecordModel(BaseModel):
    info: InfoModel
    femur: FemurModel
    tibia: TibiaModel
    total: TotalModel
    pixel_distance: PixelDistanceModel
    details: DetailsModel
