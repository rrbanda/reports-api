# API for image analysis reports in json format
<img width="1512" alt="Screenshot 2024-10-17 at 12 41 39 AM" src="https://github.com/user-attachments/assets/44dafb75-a139-4e7a-a3ff-c1daf8feb804">


<img width="1512" alt="Screenshot 2024-10-17 at 12 49 20 AM" src="https://github.com/user-attachments/assets/88344202-e6df-4ab2-ae85-84fd45992d2c">


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

Note : If you do not want to build you can use image `quay.io/rbrhssa/reports-api:latest` and run it as well using podman , Check pod.yaml for the same.

### Build the FastAPI Docker Image
From the root of the project, run:

` podman build -t fastapi-neo4j-app . `


# Using Podman Desktop 

<img width="1512" alt="Screenshot 2024-10-16 at 10 47 04 PM" src="https://github.com/user-attachments/assets/56a084a4-9741-4df6-9c24-61607aea9ea3">
<img width="1512" alt="Screenshot 2024-10-16 at 10 44 49 PM" src="https://github.com/user-attachments/assets/42cd2a64-658f-41bc-b9ba-9ffb878f3455">
<img width="1512" alt="Screenshot 2024-10-16 at 10 44 56 PM" src="https://github.com/user-attachments/assets/571d56f1-cea7-425c-a4f0-bb4058ee4bff">
<img width="1512" alt="Screenshot 2024-10-16 at 10 45 04 PM" src="https://github.com/user-attachments/assets/99c720b8-efa8-402c-94f2-ea4fb1a4afa6">





### Create and Run the Pod using CLI for the same from terminal 

Create a pod and run the FastAPI and Neo4j containers within it:

# Create a Pod

` podman pod create --name fastapi-pod -p 8000:8000 -p 7687:7687 `

# Run the Neo4j container

` podman run -d --pod fastapi-pod --name neo4j-container -e NEO4J_AUTH=neo4j/password neo4j `

# Run the FastAPI container

` podman run -d --pod fastapi-pod --name fastapi-container fastapi-neo4j-app `



Step 3: Access the API

The API will be accessible at http://localhost:8000.

## API Endpoints and Testing

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

### Get Patient Data - GET /get_data/{patient_id}

Retrieves data for a specific patient by their PatientID.


` curl -X GET "http://localhost:8000/get_data/71054xfdsar" -H "Content-Type: application/json" `

### Get All Patients Data - GET /get_all_patients

Retrieves data for all patients.

` curl -X GET "http://localhost:8000/get_all_patients" -H "Content-Type: application/json" `


### Delete Patient Data - DELETE /delete_data/{patient_id}

Deletes a specific patient's data.


` curl -X DELETE "http://localhost:8000/delete_data/71054xfdsar" -H "Content-Type: application/json" `

### Health Check - GET /health_check

Checks the health of the API and database connection.

` curl -X GET "http://localhost:8000/health_check" -H "Content-Type: application/json" `



## Summary of API Endpoints

* POST /add_data: Add a new patient record.
* PUT /update_data/{patient_id}: Update a specific patient's data.
* GET /get_data/{patient_id}: Retrieve the data for a specific patient.
* GET /get_all_patients: Retrieve the data for all patients.
* DELETE /delete_data/{patient_id}: Delete a specific patient's data.
* GET /health_check: Health check for the API and database.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

### Contact

For questions or support, please reach out to the project maintainer.
