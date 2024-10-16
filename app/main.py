# app/main.py

from fastapi import FastAPI, HTTPException, Query
from app.models import PatientRecord
from app.database import collection
from typing import List, Optional

app = FastAPI(title="Patient Management API", version="1.0")

@app.post("/patients/", response_model=PatientRecord, status_code=201)
def create_patient_record(record: PatientRecord):
    record_dict = record.dict(by_alias=True)
    try:
        collection.insert_one(record_dict)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Study ID already exists")
    return record

@app.get("/patients/{study_id}", response_model=PatientRecord)
def get_patient_record(study_id: str):
    record = collection.find_one({"study_id": study_id})
    if record:
        return PatientRecord(**record)
    raise HTTPException(status_code=404, detail="Patient record not found")

@app.put("/patients/{study_id}", response_model=PatientRecord)
def update_patient_record(study_id: str, record: PatientRecord):
    if study_id != record.study_id:
        raise HTTPException(status_code=400, detail="Study ID in URL and body do not match")
    update_result = collection.update_one({"study_id": study_id}, {"$set": record.dict(by_alias=True)})
    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Patient record not found")
    return record

@app.delete("/patients/{study_id}", status_code=204)
def delete_patient_record(study_id: str):
    delete_result = collection.delete_one({"study_id": study_id})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Patient record not found")
    return

@app.get("/patients/", response_model=List[PatientRecord])
def list_patient_records(patient_id: Optional[str] = Query(None, description="Filter by PatientID")):
    if patient_id:
        records = list(collection.find({"info.PatientID": patient_id}))
    else:
        records = list(collection.find())
    return [PatientRecord(**record) for record in records]
