# FastAPI Neo4j Patient Data Management API

## Overview
This is a FastAPI application that provides a RESTful API to manage patient data using a Neo4j database. The application allows you to perform CRUD (Create, Read, Update, Delete) operations for managing patient records. This solution is containerized, making it easy to deploy using Podman.

The patient data structure is comprehensive and includes:
- General information (`info`)
- Measurements for femur and tibia (`femur`, `tibia`)
- Total measurements (`total`)
- Pixel distances (`pixel_distance`)
- Study details (`details`)

## Features
- Asynchronous RESTful API endpoints using FastAPI.
- Neo4j database integration for storing and managing patient data.
- Containerized deployment using Podman.
- Full support for CRUD operations on patient data.

## Prerequisites
- Podman installed
- Podman Desktop installed (Optional, for easy management)
- Python 3.9 or above
- Neo4j Docker image available locally

## Setup and Run using Podman
The following steps guide you through building and running the FastAPI application and Neo4j database using Podman.

### Step 1: Build the FastAPI Docker Image
From the root of the project, run:

` podman build -t fastapi-neo4j-app . `


Step 2: Create and Run the Pod

Create a pod and run the FastAPI and Neo4j containers within it:

# Create a Pod

` podman pod create --name fastapi-pod -p 8000:8000 -p 7687:7687 `

# Run the Neo4j container

` podman run -d --pod fastapi-pod --name neo4j-container -e NEO4J_AUTH=neo4j/password neo4j `

# Run the FastAPI container

` podman run -d --pod fastapi-pod --name fastapi-container fastapi-neo4j-app `


Step 3: Access the API
The API will be accessible at http://localhost:8000.

API Endpoints and Testing

Below are the API endpoints available and the curl commands to test each one.

1. Add Patient Data - POST /add_data
Adds a new patient record.

```
curl -X POST "http://localhost:8000/add_data" -H "Content-Type: application/json" -d '{
  "data": {
    "61928-1.2.250.1.118.3.1305.235.1.8008.46.1727122139": {
      "info": {
        "PatientID": "71054xfdsar",
        "PatientName": "SMITH^JANE",
        "PatientAge": "012Y",
        "StudyDate": "20240923"
      },
      "femur": {
        "Right_femur": "41.8 cm",
        "Left_femur": "42.0 cm",
        "Difference": "00.2 cm, left longer 0.5%"
      },
      "tibia": {
        "Right_tibia": "34.5 cm",
        "Left_tibia": "34.3 cm",
        "Difference": "00.2 cm, right longer 0.6%"
      },
      "total": {
        "Total_right": "76.3 cm",
        "Total_left": "76.3 cm",
        "Difference": "00.0 cm, equal 0.0%"
      },
      "pixel_distance": {
        "Left_femur": 1892,
        "Left_tibia": 1544,
        "Right_femur": 1886,
        "Right_tibia": 1555
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
}'

```


2. Update Patient Data - PUT /update_data/{patient_id}
Updates an existing patient's data.
```
curl -X PUT "http://localhost:8000/update_data/71054xfdsar" -H "Content-Type: application/json" -d '{
  "data": {
    "61928-1.2.250.1.118.3.1305.235.1.8008.46.1727122139": {
      "info": {
        "PatientID": "71054xfdsar",
        "PatientName": "SMITH^JOHN",
        "PatientAge": "013Y",
        "StudyDate": "20240925"
      },
      "femur": {
        "Right_femur": "42.0 cm",
        "Left_femur": "42.5 cm",
        "Difference": "00.5 cm, left longer 1.2%"
      },
      "tibia": {
        "Right_tibia": "34.7 cm",
        "Left_tibia": "34.6 cm",
        "Difference": "00.1 cm, right longer 0.3%"
      },
      "total": {
        "Total_right": "77.0 cm",
        "Total_left": "77.5 cm",
        "Difference": "00.5 cm, left longer 0.7%"
      },
      "pixel_distance": {
        "Left_femur": 1900,
        "Left_tibia": 1560,
        "Right_femur": 1895,
        "Right_tibia": 1570
      },
      "details": {
        "AccessionNumber": "100876169",
        "StudyDescription": "Updated XR HIPS TO ANKLES LEG MEASUREMENTS",
        "SeriesDescription": "Lower limbs - updated",
        "BodyPartExamined": "LEG",
        "FieldOfViewDimensions": "[980, 400]",
        "StationName": "EOSRM8"
      }
    }
  }
}'
```

3. Get Patient Data - GET /get_data/{patient_id}
Retrieves data for a specific patient by their PatientID.


` curl -X GET "http://localhost:8000/get_data/71054xfdsar" -H "Content-Type: application/json" `


4. Get All Patients Data - GET /get_all_patients


Retrieves data for all patients.

` curl -X GET "http://localhost:8000/get_all_patients" -H "Content-Type: application/json" `


5. Delete Patient Data - DELETE /delete_data/{patient_id}
Deletes a specific patient's data.


` curl -X DELETE "http://localhost:8000/delete_data/71054xfdsar" -H "Content-Type: application/json" `


6. Health Check - GET /health_check
Checks the health of the API and database connection.

` curl -X GET "http://localhost:8000/health_check" -H "Content-Type: application/json" `



Summary of API Endpoints

POST /add_data: Add a new patient record.
PUT /update_data/{patient_id}: Update a specific patient's data.
GET /get_data/{patient_id}: Retrieve the data for a specific patient.
GET /get_all_patients: Retrieve the data for all patients.
DELETE /delete_data/{patient_id}: Delete a specific patient's data.
GET /health_check: Health check for the API and database.
License

This project is licensed under the MIT License.

Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

Contact

For questions or support, please reach out to the project maintainer.
