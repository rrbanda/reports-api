// app/init-mongo/init.js

db = db.getSiblingDB('patient_db'); // Switch to the desired database

const data = [
    {
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
    },
    {
        "study_id": "61928-1.2.250.1.118.3.1305.235.1.8008.46.1727122140",
        "info": {
            "PatientID": "71054xfdsar1",
            "PatientName": "DOE^JOHN",
            "PatientAge": "015Y",
            "StudyDate": "20240924"
        },
        "femur": {
            "Right femur": "41.7 cm",
            "Left femur": "42.2 cm",
            "Difference": "00.5 cm, left longer 1.2%"
        },
        "tibia": {
            "Right tibia": "34.4 cm",
            "Left tibia": "34.6 cm",
            "Difference": "00.2 cm, left longer 0.6%"
        },
        "total": {
            "Total right": "75.8 cm",
            "Total left": "76.8 cm",
            "Difference": "01.0 cm, left longer 1.3%"
        },
        "pixel_distance": {
            "Left femur": 1900,
            "Left tibia": 1550,
            "Right femur": 1890,
            "Right tibia": 1560
        },
        "details": {
            "AccessionNumber": "100876170",
            "StudyDescription": "XR HIPS TO ANKLES LEG MEASUREMENTS",
            "SeriesDescription": "Lower limbs",
            "BodyPartExamined": "LEG",
            "FieldOfViewDimensions": "[980, 400]",
            "StationName": "EOSRM8"
        }
    },
    {
        "study_id": "61928-1.2.250.1.118.3.1305.235.1.8008.46.1727122141",
        "info": {
            "PatientID": "71054xfdsar2",
            "PatientName": "BROWN^ALICE",
            "PatientAge": "010Y",
            "StudyDate": "20240925"
        },
        "femur": {
            "Right femur": "41.6 cm",
            "Left femur": "42.3 cm",
            "Difference": "00.7 cm, left longer 1.7%"
        },
        "tibia": {
            "Right tibia": "34.2 cm",
            "Left tibia": "34.5 cm",
            "Difference": "00.3 cm, left longer 0.9%"
        },
        "total": {
            "Total right": "75.0 cm",
            "Total left": "76.8 cm",
            "Difference": "01.8 cm, left longer 2.4%"
        },
        "pixel_distance": {
            "Left femur": 1910,
            "Left tibia": 1560,
            "Right femur": 1900,
            "Right tibia": 1570
        },
        "details": {
            "AccessionNumber": "100876171",
            "StudyDescription": "XR HIPS TO ANKLES LEG MEASUREMENTS",
            "SeriesDescription": "Lower limbs",
            "BodyPartExamined": "LEG",
            "FieldOfViewDimensions": "[990, 410]",
            "StationName": "EOSRM9"
        }
    }
    // Add more records as needed
]
