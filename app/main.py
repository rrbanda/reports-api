# File: app/main.py
from fastapi import FastAPI, HTTPException
from typing import Dict

from .database import get_driver
from .models import PatientData, MeasurementData

app = FastAPI()
driver = get_driver()

@app.post("/add_data")
async def add_data(patient_data: PatientData):
    async with driver.session() as session:
        query = """
        MERGE (patient:Patient {PatientID: $PatientID})
        SET patient += {
            PatientName: $PatientName,
            PatientAge: $PatientAge,
            StudyDate: $StudyDate,
            Femur_Right: $Femur_Right,
            Femur_Left: $Femur_Left,
            Femur_Difference: $Femur_Difference,
            Tibia_Right: $Tibia_Right,
            Tibia_Left: $Tibia_Left,
            Tibia_Difference: $Tibia_Difference,
            Total_Right: $Total_Right,
            Total_Left: $Total_Left,
            Total_Difference: $Total_Difference,
            PixelDistance_LeftFemur: $PixelDistance_LeftFemur,
            PixelDistance_LeftTibia: $PixelDistance_LeftTibia,
            PixelDistance_RightFemur: $PixelDistance_RightFemur,
            PixelDistance_RightTibia: $PixelDistance_RightTibia
        }
        WITH patient
        MERGE (patient)-[:HAS_DETAILS]->(details:Details {
            AccessionNumber: $AccessionNumber,
            StudyDescription: $StudyDescription,
            SeriesDescription: $SeriesDescription,
            BodyPartExamined: $BodyPartExamined,
            FieldOfViewDimensions: $FieldOfViewDimensions,
            StationName: $StationName
        })
        """
        for key, value in patient_data.data.items():
            try:
                await session.run(
                    query,
                    PatientID=value.info.PatientID,
                    PatientName=value.info.PatientName,
                    PatientAge=value.info.PatientAge,
                    StudyDate=value.info.StudyDate,
                    Femur_Right=value.femur.Right_femur,
                    Femur_Left=value.femur.Left_femur,
                    Femur_Difference=value.femur.Difference,
                    Tibia_Right=value.tibia.Right_tibia,
                    Tibia_Left=value.tibia.Left_tibia,
                    Tibia_Difference=value.tibia.Difference,
                    Total_Right=value.total.Total_right,
                    Total_Left=value.total.Total_left,
                    Total_Difference=value.total.Difference,
                    PixelDistance_LeftFemur=value.pixel_distance.Left_femur,
                    PixelDistance_LeftTibia=value.pixel_distance.Left_tibia,
                    PixelDistance_RightFemur=value.pixel_distance.Right_femur,
                    PixelDistance_RightTibia=value.pixel_distance.Right_tibia,
                    AccessionNumber=value.details.AccessionNumber,
                    StudyDescription=value.details.StudyDescription,
                    SeriesDescription=value.details.SeriesDescription,
                    BodyPartExamined=value.details.BodyPartExamined,
                    FieldOfViewDimensions=value.details.FieldOfViewDimensions,
                    StationName=value.details.StationName
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    return {"message": "Data added successfully"}

@app.get("/get_data/{patient_id}")
async def get_data(patient_id: str):
    async with driver.session() as session:
        query = """
        MATCH (patient:Patient {PatientID: $patient_id})
        OPTIONAL MATCH (patient)-[:HAS_DETAILS]->(details:Details)
        RETURN patient, details
        """
        result = await session.run(query, patient_id=patient_id)
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="Patient not found")

        patient_node = record["patient"]
        details_node = record["details"]

        response = {
            patient_node.get("PatientID"): {
                "info": {
                    "PatientID": patient_node.get("PatientID"),
                    "PatientName": patient_node.get("PatientName"),
                    "PatientAge": patient_node.get("PatientAge"),
                    "StudyDate": patient_node.get("StudyDate"),
                },
                "femur": {
                    "Right femur": patient_node.get("Femur_Right"),
                    "Left femur": patient_node.get("Femur_Left"),
                    "Difference": patient_node.get("Femur_Difference"),
                },
                "tibia": {
                    "Right tibia": patient_node.get("Tibia_Right"),
                    "Left tibia": patient_node.get("Tibia_Left"),
                    "Difference": patient_node.get("Tibia_Difference"),
                },
                "total": {
                    "Total right": patient_node.get("Total_Right"),
                    "Total left": patient_node.get("Total_Left"),
                    "Difference": patient_node.get("Total_Difference"),
                },
                "pixel_distance": {
                    "Left femur": patient_node.get("PixelDistance_LeftFemur"),
                    "Left tibia": patient_node.get("PixelDistance_LeftTibia"),
                    "Right femur": patient_node.get("PixelDistance_RightFemur"),
                    "Right tibia": patient_node.get("PixelDistance_RightTibia"),
                },
                "details": {
                    "AccessionNumber": details_node.get("AccessionNumber"),
                    "StudyDescription": details_node.get("StudyDescription"),
                    "SeriesDescription": details_node.get("SeriesDescription"),
                    "BodyPartExamined": details_node.get("BodyPartExamined"),
                    "FieldOfViewDimensions": details_node.get("FieldOfViewDimensions"),
                    "StationName": details_node.get("StationName"),
                }
            }
        }

        return response

@app.get("/get_all_patients")
async def get_all_patients():
    async with driver.session() as session:
        query = """
        MATCH (patient:Patient)
        OPTIONAL MATCH (patient)-[:HAS_DETAILS]->(details:Details)
        RETURN patient, details
        """
        result = await session.run(query)
        patients = {}
        async for record in result:
            patient_node = record["patient"]
            details_node = record["details"]

            patients[patient_node.get("PatientID")] = {
                "info": {
                    "PatientID": patient_node.get("PatientID"),
                    "PatientName": patient_node.get("PatientName"),
                    "PatientAge": patient_node.get("PatientAge"),
                    "StudyDate": patient_node.get("StudyDate"),
                },
                "femur": {
                    "Right femur": patient_node.get("Femur_Right"),
                    "Left femur": patient_node.get("Femur_Left"),
                    "Difference": patient_node.get("Femur_Difference"),
                },
                "tibia": {
                    "Right tibia": patient_node.get("Tibia_Right"),
                    "Left tibia": patient_node.get("Tibia_Left"),
                    "Difference": patient_node.get("Tibia_Difference"),
                },
                "total": {
                    "Total right": patient_node.get("Total_Right"),
                    "Total left": patient_node.get("Total_Left"),
                    "Difference": patient_node.get("Total_Difference"),
                },
                "pixel_distance": {
                    "Left femur": patient_node.get("PixelDistance_LeftFemur"),
                    "Left tibia": patient_node.get("PixelDistance_LeftTibia"),
                    "Right femur": patient_node.get("PixelDistance_RightFemur"),
                    "Right tibia": patient_node.get("PixelDistance_RightTibia"),
                },
                "details": {
                    "AccessionNumber": details_node.get("AccessionNumber"),
                    "StudyDescription": details_node.get("StudyDescription"),
                    "SeriesDescription": details_node.get("SeriesDescription"),
                    "BodyPartExamined": details_node.get("BodyPartExamined"),
                    "FieldOfViewDimensions": details_node.get("FieldOfViewDimensions"),
                    "StationName": details_node.get("StationName"),
                }
            }

        return {"patients": patients}

@app.put("/update_data/{patient_id}")
async def update_data(patient_id: str, patient_data: MeasurementData):
    async with driver.session() as session:
        query = """
        MATCH (patient:Patient {PatientID: $PatientID})
        SET patient += {
            PatientName: $PatientName,
            PatientAge: $PatientAge,
            StudyDate: $StudyDate,
            Femur_Right: $Femur_Right,
            Femur_Left: $Femur_Left,
            Femur_Difference: $Femur_Difference,
            Tibia_Right: $Tibia_Right,
            Tibia_Left: $Tibia_Left,
            Tibia_Difference: $Tibia_Difference,
            Total_Right: $Total_Right,
            Total_Left: $Total_Left,
            Total_Difference: $Total_Difference,
            PixelDistance_LeftFemur: $PixelDistance_LeftFemur,
            PixelDistance_LeftTibia: $PixelDistance_LeftTibia,
            PixelDistance_RightFemur: $PixelDistance_RightFemur,
            PixelDistance_RightTibia: $PixelDistance_RightTibia
        }
        WITH patient
        OPTIONAL MATCH (patient)-[r:HAS_DETAILS]->(details:Details)
        DELETE r, details
        WITH patient
        MERGE (patient)-[:HAS_DETAILS]->(new_details:Details {
            AccessionNumber: $AccessionNumber,
            StudyDescription: $StudyDescription,
            SeriesDescription: $SeriesDescription,
            BodyPartExamined: $BodyPartExamined,
            FieldOfViewDimensions: $FieldOfViewDimensions,
            StationName: $StationName
        })
        """
        try:
            await session.run(
                query,
                PatientID=patient_id,
                PatientName=patient_data.info.PatientName,
                PatientAge=patient_data.info.PatientAge,
                StudyDate=patient_data.info.StudyDate,
                Femur_Right=patient_data.femur.Right_femur,
                Femur_Left=patient_data.femur.Left_femur,
                Femur_Difference=patient_data.femur.Difference,
                Tibia_Right=patient_data.tibia.Right_tibia,
                Tibia_Left=patient_data.tibia.Left_tibia,
                Tibia_Difference=patient_data.tibia.Difference,
                Total_Right=patient_data.total.Total_right,
                Total_Left=patient_data.total.Total_left,
                Total_Difference=patient_data.total.Difference,
                PixelDistance_LeftFemur=patient_data.pixel_distance.Left_femur,
                PixelDistance_LeftTibia=patient_data.pixel_distance.Left_tibia,
                PixelDistance_RightFemur=patient_data.pixel_distance.Right_femur,
                PixelDistance_RightTibia=patient_data.pixel_distance.Right_tibia,
                AccessionNumber=patient_data.details.AccessionNumber,
                StudyDescription=patient_data.details.StudyDescription,
                SeriesDescription=patient_data.details.SeriesDescription,
                BodyPartExamined=patient_data.details.BodyPartExamined,
                FieldOfViewDimensions=patient_data.details.FieldOfViewDimensions,
                StationName=patient_data.details.StationName
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    return {"message": "Data updated successfully"}

@app.delete("/delete_data/{patient_id}")
async def delete_data(patient_id: str):
    async with driver.session() as session:
        query = """
        MATCH (patient:Patient {PatientID: $patient_id})
        OPTIONAL MATCH (patient)-[r:HAS_DETAILS]->(details:Details)
        DELETE r, details, patient
        """
        try:
            result = await session.run(query, patient_id=patient_id)
            if result.consume().counters.nodes_deleted == 0:
                raise HTTPException(status_code=404, detail="Patient not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    return {"message": "Data deleted successfully"}

@app.get("/health_check")
async def health_check():
    return {"status": "ok"}
