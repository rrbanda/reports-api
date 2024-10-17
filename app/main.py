from fastapi import FastAPI, HTTPException
from models import PatientRecordModel
from init import Neo4jConnectionManager

app = FastAPI()

neo4j_manager = Neo4jConnectionManager()

@app.on_event("startup")
async def startup_event():
    try:
        await neo4j_manager.get_patient_record("test")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to connect to Neo4j")

@app.on_event("shutdown")
async def shutdown_event():
    neo4j_manager.close()

@app.get("/health", status_code=200)
async def health_check():
    return {"status": "healthy"}

@app.post("/patients/", status_code=201)
async def create_patient(patient_record: PatientRecordModel):
    try:
        result = await neo4j_manager.create_patient_record(patient_record.dict())
        return {"status": "Patient created", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/patients/{patient_id}", status_code=200)
async def get_patient(patient_id: str):
    try:
        result = await neo4j_manager.get_patient_record(patient_id)
        if not result:
            raise HTTPException(status_code=404, detail="Patient not found")
        return {"status": "Patient found", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/patients/{patient_id}", status_code=200)
async def update_patient(patient_id: str, update_data: PatientRecordModel):
    try:
        result = await neo4j_manager.update_patient_record(patient_id, update_data.dict())
        return {"status": "Patient updated", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/patients/{patient_id}", status_code=204)
async def delete_patient(patient_id: str):
    try:
        await neo4j_manager.delete_patient_record(patient_id)
        return {"status": "Patient deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
