from fastapi import FastAPI, HTTPException, Query
from app.models import PatientRecord, PatientInfo, Femur, Tibia, Total, PixelDistance, Details
from app.database import get_session
from typing import List, Optional
import uuid

app = FastAPI(title="Patient Management API with Neo4j", version="1.0")

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Patient Management API with Neo4j"}

@app.post("/patients/", response_model=PatientRecord, status_code=201)
def create_patient_record(record: PatientRecord):
    with get_session() as session:
        # Check if study_id already exists
        result = session.run(
            "MATCH (p:Patient {study_id: $study_id}) RETURN p",
            study_id=record.study_id
        )
        if result.single():
            raise HTTPException(status_code=400, detail="Study ID already exists")
        
        # Create a new patient node
        session.run(
            """
            CREATE (p:Patient {
                study_id: $study_id,
                PatientID: $PatientID,
                PatientName: $PatientName,
                PatientAge: $PatientAge,
                StudyDate: $StudyDate,
                Right_femur: $Right_femur,
                Left_femur: $Left_femur,
                femur_Difference: $Difference_femur,
                Right_tibia: $Right_tibia,
                Left_tibia: $Left_tibia,
                tibia_Difference: $Difference_tibia,
                Total_right: $Total_right,
                Total_left: $Total_left,
                total_Difference: $Difference_total,
                Left_femur_distance: $Left_femur_distance,
                Left_tibia_distance: $Left_tibia_distance,
                Right_femur_distance: $Right_femur_distance,
                Right_tibia_distance: $Right_tibia_distance,
                AccessionNumber: $AccessionNumber,
                StudyDescription: $StudyDescription,
                SeriesDescription: $SeriesDescription,
                BodyPartExamined: $BodyPartExamined,
                FieldOfViewDimensions: $FieldOfViewDimensions,
                StationName: $StationName,
                vector: $vector
            })
            """,
            study_id=record.study_id,
            PatientID=record.info.PatientID,
            PatientName=record.info.PatientName,
            PatientAge=record.info.PatientAge,
            StudyDate=record.info.StudyDate,
            Right_femur=record.femur.Right_femur,
            Left_femur=record.femur.Left_femur,
            Difference_femur=record.femur.Difference,
            Right_tibia=record.tibia.Right_tibia,
            Left_tibia=record.tibia.Left_tibia,
            Difference_tibia=record.tibia.Difference,
            Total_right=record.total.Total_right,
            Total_left=record.total.Total_left,
            Difference_total=record.total.Difference,
            Left_femur_distance=record.pixel_distance.Left_femur,
            Left_tibia_distance=record.pixel_distance.Left_tibia,
            Right_femur_distance=record.pixel_distance.Right_femur,
            Right_tibia_distance=record.pixel_distance.Right_tibia,
            AccessionNumber=record.details.AccessionNumber,
            StudyDescription=record.details.StudyDescription,
            SeriesDescription=record.details.SeriesDescription,
            BodyPartExamined=record.details.BodyPartExamined,
            FieldOfViewDimensions=record.details.FieldOfViewDimensions,
            StationName=record.details.StationName,
            vector=record.vector
        )
    return record

@app.get("/patients/{study_id}", response_model=PatientRecord)
def get_patient_record(study_id: str):
    with get_session() as session:
        result = session.run(
            "MATCH (p:Patient {study_id: $study_id}) RETURN p",
            study_id=study_id
        )
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="Patient record not found")
        
        p = record["p"]
        return PatientRecord(
            study_id=p["study_id"],
            info=PatientInfo(
                PatientID=p["PatientID"],
                PatientName=p["PatientName"],
                PatientAge=p["PatientAge"],
                StudyDate=p["StudyDate"]
            ),
            femur=Femur(
                Right_femur=p["Right_femur"],
                Left_femur=p["Left_femur"],
                Difference=p["femur_Difference"]
            ),
            tibia=Tibia(
                Right_tibia=p["Right_tibia"],
                Left_tibia=p["Left_tibia"],
                Difference=p["tibia_Difference"]
            ),
            total=Total(
                Total_right=p["Total_right"],
                Total_left=p["Total_left"],
                Difference=p["total_Difference"]
            ),
            pixel_distance=PixelDistance(
                Left_femur=p["Left_femur_distance"],
                Left_tibia=p["Left_tibia_distance"],
                Right_femur=p["Right_femur_distance"],
                Right_tibia=p["Right_tibia_distance"]
            ),
            details=Details(
                AccessionNumber=p["AccessionNumber"],
                StudyDescription=p["StudyDescription"],
                SeriesDescription=p["SeriesDescription"],
                BodyPartExamined=p["BodyPartExamined"],
                FieldOfViewDimensions=p["FieldOfViewDimensions"],
                StationName=p["StationName"]
            ),
            vector=p["vector"]
        )

@app.put("/patients/{study_id}", response_model=PatientRecord)
def update_patient_record(study_id: str, record: PatientRecord):
    if study_id != record.study_id:
        raise HTTPException(status_code=400, detail="Study ID in URL and body do not match")
    
    with get_session() as session:
        # Check if patient exists
        result = session.run(
            "MATCH (p:Patient {study_id: $study_id}) RETURN p",
            study_id=study_id
        )
        existing = result.single()
        if not existing:
            raise HTTPException(status_code=404, detail="Patient record not found")
        
        # Update patient node
        session.run(
            """
            MATCH (p:Patient {study_id: $study_id})
            SET
                p.PatientID = $PatientID,
                p.PatientName = $PatientName,
                p.PatientAge = $PatientAge,
                p.StudyDate = $StudyDate,
                p.Right_femur = $Right_femur,
                p.Left_femur = $Left_femur,
                p.femur_Difference = $Difference_femur,
                p.Right_tibia = $Right_tibia,
                p.Left_tibia = $Left_tibia,
                p.tibia_Difference = $Difference_tibia,
                p.Total_right = $Total_right,
                p.Total_left = $Total_left,
                p.total_Difference = $Difference_total,
                p.Left_femur_distance = $Left_femur_distance,
                p.Left_tibia_distance = $Left_tibia_distance,
                p.Right_femur_distance = $Right_femur_distance,
                p.Right_tibia_distance = $Right_tibia_distance,
                p.AccessionNumber = $AccessionNumber,
                p.StudyDescription = $StudyDescription,
                p.SeriesDescription = $SeriesDescription,
                p.BodyPartExamined = $BodyPartExamined,
                p.FieldOfViewDimensions = $FieldOfViewDimensions,
                p.StationName = $StationName,
                p.vector = $vector
            """,
            study_id=record.study_id,
            PatientID=record.info.PatientID,
            PatientName=record.info.PatientName,
            PatientAge=record.info.PatientAge,
            StudyDate=record.info.StudyDate,
            Right_femur=record.femur.Right_femur,
            Left_femur=record.femur.Left_femur,
            Difference_femur=record.femur.Difference,
            Right_tibia=record.tibia.Right_tibia,
            Left_tibia=record.tibia.Left_tibia,
            Difference_tibia=record.tibia.Difference,
            Total_right=record.total.Total_right,
            Total_left=record.total.Total_left,
            Difference_total=record.total.Difference,
            Left_femur_distance=record.pixel_distance.Left_femur,
            Left_tibia_distance=record.pixel_distance.Left_tibia,
            Right_femur_distance=record.pixel_distance.Right_femur,
            Right_tibia_distance=record.pixel_distance.Right_tibia,
            AccessionNumber=record.details.AccessionNumber,
            StudyDescription=record.details.StudyDescription,
            SeriesDescription=record.details.SeriesDescription,
            BodyPartExamined=record.details.BodyPartExamined,
            FieldOfViewDimensions=record.details.FieldOfViewDimensions,
            StationName=record.details.StationName,
            vector=record.vector
        )
    return record

@app.delete("/patients/{study_id}", status_code=204)
def delete_patient_record(study_id: str):
    with get_session() as session:
        result = session.run(
            "MATCH (p:Patient {study_id: $study_id}) DELETE p RETURN count(p) as deleted_count",
            study_id=study_id
        )
        deleted_count = result.single()["deleted_count"]
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="Patient record not found")
    return

@app.get("/patients/", response_model=List[PatientRecord])
def list_patient_records(patient_id: Optional[str] = Query(None, description="Filter by PatientID")):
    with get_session() as session:
        if patient_id:
            query = """
                MATCH (p:Patient {PatientID: $patient_id})
                RETURN p
            """
            result = session.run(query, patient_id=patient_id)
        else:
            query = """
                MATCH (p:Patient)
                RETURN p
            """
            result = session.run(query)
        
        records = []
        for record in result:
            p = record["p"]
            records.append(
                PatientRecord(
                    study_id=p["study_id"],
                    info=PatientInfo(
                        PatientID=p["PatientID"],
                        PatientName=p["PatientName"],
                        PatientAge=p["PatientAge"],
                        StudyDate=p["StudyDate"]
                    ),
                    femur=Femur(
                        Right_femur=p["Right_femur"],
                        Left_femur=p["Left_femur"],
                        Difference=p["femur_Difference"]
                    ),
                    tibia=Tibia(
                        Right_tibia=p["Right_tibia"],
                        Left_tibia=p["Left_tibia"],
                        Difference=p["tibia_Difference"]
                    ),
                    total=Total(
                        Total_right=p["Total_right"],
                        Total_left=p["Total_left"],
                        Difference=p["total_Difference"]
                    ),
                    pixel_distance=PixelDistance(
                        Left_femur=p["Left_femur_distance"],
                        Left_tibia=p["Left_tibia_distance"],
                        Right_femur=p["Right_femur_distance"],
                        Right_tibia=p["Right_tibia_distance"]
                    ),
                    details=Details(
                        AccessionNumber=p["AccessionNumber"],
                        StudyDescription=p["StudyDescription"],
                        SeriesDescription=p["SeriesDescription"],
                        BodyPartExamined=p["BodyPartExamined"],
                        FieldOfViewDimensions=p["FieldOfViewDimensions"],
                        StationName=p["StationName"]
                    ),
                    vector=p["vector"]
                )
            )
        return records
