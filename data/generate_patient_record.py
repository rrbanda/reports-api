import json

patient_record = {
    "study_id": "61928-1.2.250.1.113.3.1305.235.1.8008.46.1727122139",
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
    },
    "vector": [0.1 for _ in range(768)]  # Generates a list with 768 elements, each 0.1
}

with open('patient_record.json', 'w') as f:
    json.dump(patient_record, f, indent=4)
