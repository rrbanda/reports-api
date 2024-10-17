from fastapi import FastAPI, HTTPException
from neo4j import AsyncGraphDatabase
from typing import Dict

from .database import get_driver
from .models import MeasurementData, PatientData

app = FastAPI()
driver = get_driver()

@app.post("/add_data")
async def add_data(patient_data: MeasurementData):
    try:
        async with driver.session() as session:
            for key, value in patient_data.data.items():
                # Correctly accessing fields from PatientData instance
                info = value.info
                details = value.details
                femur = value.femur
                tibia = value.tibia
                total = value.total
                pixel_distance = value.pixel_distance

                query = """
                MERGE (patient:Patient {PatientID: $PatientID})
                SET patient += {
                    PatientName: $PatientName,
                    PatientAge: $PatientAge,
                    StudyDate: $StudyDate,
                    Right_femur: $Right_femur,
                    Left_femur: $Left_femur,
                    Femur_Difference: $Femur_Difference,
                    Right_tibia: $Right_tibia,
                    Left_tibia: $Left_tibia,
                    Tibia_Difference: $Tibia_Difference,
                    Total_right: $Total_right,
                    Total_left: $Total_left,
                    Total_Difference: $Total_Difference,
                    PixelDistance_LeftFemur: $PixelDistance_LeftFemur,
                    PixelDistance_LeftTibia: $PixelDistance_LeftTibia,
                    PixelDistance_RightFemur: $PixelDistance_RightFemur,
                    PixelDistance_RightTibia: $PixelDistance_RightTibia
                }
                WITH patient
                CREATE (patient)-[:HAS_DETAIL]->(detail:Detail {
                    AccessionNumber: $AccessionNumber,
                    StudyDescription: $StudyDescription,
                    SeriesDescription: $SeriesDescription,
                    BodyPartExamined: $BodyPartExamined,
                    FieldOfViewDimensions: $FieldOfViewDimensions,
                    StationName: $StationName
                })
                """
                await session.run(
                    query,
                    PatientID=info.PatientID,
                    PatientName=info.PatientName,
                    PatientAge=info.PatientAge,
                    StudyDate=info.StudyDate,
                    Right_femur=femur.Right_femur,
                    Left_femur=femur.Left_femur,
                    Femur_Difference=femur.Difference,
                    Right_tibia=tibia.Right_tibia,
                    Left_tibia=tibia.Left_tibia,
                    Tibia_Difference=tibia.Difference,
                    Total_right=total.Total_right,
                    Total_left=total.Total_left,
                    Total_Difference=total.Difference,
                    PixelDistance_LeftFemur=pixel_distance.Left_femur,
                    PixelDistance_LeftTibia=pixel_distance.Left_tibia,
                    PixelDistance_RightFemur=pixel_distance.Right_femur,
                    PixelDistance_RightTibia=pixel_distance.Right_tibia,
                    AccessionNumber=details.AccessionNumber,
                    StudyDescription=details.StudyDescription,
                    SeriesDescription=details.SeriesDescription,
                    BodyPartExamined=details.BodyPartExamined,
                    FieldOfViewDimensions=details.FieldOfViewDimensions,
                    StationName=details.StationName
                )
        return {"message": "Data added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/get_data/{patient_id}")
async def get_data(patient_id: str):
    try:
        async with driver.session() as session:
            query = """
            MATCH (patient:Patient {PatientID: $patient_id})
            OPTIONAL MATCH (patient)-[:HAS_DETAIL]->(detail:Detail)
            RETURN patient, detail
            """
            result = await session.run(query, patient_id=patient_id)
            record = await result.single()

            if not record:
                raise HTTPException(status_code=404, detail="Patient not found")

            patient_data = record["patient"]
            details = record["detail"]

            # Construct response by including all required sections
            response = {
                "info": {
                    "PatientID": patient_data.get("PatientID"),
                    "PatientName": patient_data.get("PatientName"),
                    "PatientAge": patient_data.get("PatientAge"),
                    "StudyDate": patient_data.get("StudyDate")
                },
                "femur": {
                    "Right_femur": patient_data.get("Right_femur"),
                    "Left_femur": patient_data.get("Left_femur"),
                    "Difference": patient_data.get("Femur_Difference")
                },
                "tibia": {
                    "Right_tibia": patient_data.get("Right_tibia"),
                    "Left_tibia": patient_data.get("Left_tibia"),
                    "Difference": patient_data.get("Tibia_Difference")
                },
                "total": {
                    "Total_right": patient_data.get("Total_right"),
                    "Total_left": patient_data.get("Total_left"),
                    "Difference": patient_data.get("Total_Difference")
                },
                "pixel_distance": {
                    "Left_femur": patient_data.get("PixelDistance_LeftFemur"),
                    "Left_tibia": patient_data.get("PixelDistance_LeftTibia"),
                    "Right_femur": patient_data.get("PixelDistance_RightFemur"),
                    "Right_tibia": patient_data.get("PixelDistance_RightTibia")
                },
                "details": {
                    "AccessionNumber": details.get("AccessionNumber"),
                    "StudyDescription": details.get("StudyDescription"),
                    "SeriesDescription": details.get("SeriesDescription"),
                    "BodyPartExamined": details.get("BodyPartExamined"),
                    "FieldOfViewDimensions": details.get("FieldOfViewDimensions"),
                    "StationName": details.get("StationName")
                }
            }

            return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/get_all_patients")
async def get_all_patients():
    try:
        async with driver.session() as session:
            query = """
            MATCH (patient:Patient)
            OPTIONAL MATCH (patient)-[:HAS_DETAIL]->(detail:Detail)
            RETURN patient, collect(detail) AS details
            """
            result = await session.run(query)
            records = await result.data()

            response = {
                "patients": []
            }

            for record in records:
                patient_data = record["patient"]
                details = record["details"][0] if record["details"] else None

                patient_info = {
                    "info": {
                        "PatientID": patient_data.get("PatientID"),
                        "PatientName": patient_data.get("PatientName"),
                        "PatientAge": patient_data.get("PatientAge"),
                        "StudyDate": patient_data.get("StudyDate")
                    },
                    "femur": {
                        "Right_femur": patient_data.get("Right_femur"),
                        "Left_femur": patient_data.get("Left_femur"),
                        "Difference": patient_data.get("Femur_Difference")
                    },
                    "tibia": {
                        "Right_tibia": patient_data.get("Right_tibia"),
                        "Left_tibia": patient_data.get("Left_tibia"),
                        "Difference": patient_data.get("Tibia_Difference")
                    },
                    "total": {
                        "Total_right": patient_data.get("Total_right"),
                        "Total_left": patient_data.get("Total_left"),
                        "Difference": patient_data.get("Total_Difference")
                    },
                    "pixel_distance": {
                        "Left_femur": patient_data.get("PixelDistance_LeftFemur"),
                        "Left_tibia": patient_data.get("PixelDistance_LeftTibia"),
                        "Right_femur": patient_data.get("PixelDistance_RightFemur"),
                        "Right_tibia": patient_data.get("PixelDistance_RightTibia")
                    },
                    "details": {
                        "AccessionNumber": details.get("AccessionNumber") if details else None,
                        "StudyDescription": details.get("StudyDescription") if details else None,
                        "SeriesDescription": details.get("SeriesDescription") if details else None,
                        "BodyPartExamined": details.get("BodyPartExamined") if details else None,
                        "FieldOfViewDimensions": details.get("FieldOfViewDimensions") if details else None,
                        "StationName": details.get("StationName") if details else None
                    }
                }

                response["patients"].append(patient_info)

            return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.put("/update_data/{patient_id}")
async def update_data(patient_id: str, patient_data: MeasurementData):
    try:
        async with driver.session() as session:
            # Extract the first and only entry from patient_data.data
            key, value = next(iter(patient_data.data.items()))
            info = value.info
            details = value.details
            femur = value.femur
            tibia = value.tibia
            total = value.total
            pixel_distance = value.pixel_distance

            query = """
            MATCH (patient:Patient {PatientID: $patient_id})
            SET patient.PatientName = $PatientName,
                patient.PatientAge = $PatientAge,
                patient.StudyDate = $StudyDate,
                patient.Right_femur = $Right_femur,
                patient.Left_femur = $Left_femur,
                patient.Femur_Difference = $Femur_Difference,
                patient.Right_tibia = $Right_tibia,
                patient.Left_tibia = $Left_tibia,
                patient.Tibia_Difference = $Tibia_Difference,
                patient.Total_right = $Total_right,
                patient.Total_left = $Total_left,
                patient.Total_Difference = $Total_Difference,
                patient.PixelDistance_LeftFemur = $PixelDistance_LeftFemur,
                patient.PixelDistance_LeftTibia = $PixelDistance_LeftTibia,
                patient.PixelDistance_RightFemur = $PixelDistance_RightFemur,
                patient.PixelDistance_RightTibia = $PixelDistance_RightTibia
            WITH patient
            OPTIONAL MATCH (patient)-[:HAS_DETAIL]->(d:Detail)
            DETACH DELETE d

            WITH patient
            CREATE (patient)-[:HAS_DETAIL]->(detail:Detail {
                AccessionNumber: $AccessionNumber,
                StudyDescription: $StudyDescription,
                SeriesDescription: $SeriesDescription,
                BodyPartExamined: $BodyPartExamined,
                FieldOfViewDimensions: $FieldOfViewDimensions,
                StationName: $StationName
            })
            """
            await session.run(
                query,
                patient_id=patient_id,
                PatientName=info.PatientName,
                PatientAge=info.PatientAge,
                StudyDate=info.StudyDate,
                Right_femur=femur.Right_femur,
                Left_femur=femur.Left_femur,
                Femur_Difference=femur.Difference,
                Right_tibia=tibia.Right_tibia,
                Left_tibia=tibia.Left_tibia,
                Tibia_Difference=tibia.Difference,
                Total_right=total.Total_right,
                Total_left=total.Total_left,
                Total_Difference=total.Difference,
                PixelDistance_LeftFemur=pixel_distance.Left_femur,
                PixelDistance_LeftTibia=pixel_distance.Left_tibia,
                PixelDistance_RightFemur=pixel_distance.Right_femur,
                PixelDistance_RightTibia=pixel_distance.Right_tibia,
                AccessionNumber=details.AccessionNumber,
                StudyDescription=details.StudyDescription,
                SeriesDescription=details.SeriesDescription,
                BodyPartExamined=details.BodyPartExamined,
                FieldOfViewDimensions=details.FieldOfViewDimensions,
                StationName=details.StationName
            )
        return {"message": f"Patient {patient_id} data updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.delete("/delete_data/{patient_id}")
async def delete_data(patient_id: str):
    try:
        async with driver.session() as session:
            query = """
            MATCH (patient:Patient {PatientID: $patient_id})
            DETACH DELETE patient
            """
            await session.run(query, patient_id=patient_id)
        return {"message": f"Patient {patient_id} data deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health_check")
async def health_check():
    try:
        async with driver.session() as session:
            # Simple query to verify database connection
            await session.run("RETURN 1")
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
