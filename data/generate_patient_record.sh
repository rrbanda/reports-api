#!/bin/bash

# Generate a vector with 768 elements, each being 0.1
VECTOR=$(printf ",%s" $(seq 1 768 | awk '{print 0.1}'))
VECTOR=${VECTOR:1}  # Remove the leading comma

# Create the JSON payload using jq
jq -n \
  --arg study_id "61928-1.2.250.1.118.3.1305.235.1.8008.46.1727122139" \
  --arg PatientID "71054xfdsar" \
  --arg PatientName "SMITH^JANE" \
  --arg PatientAge "012Y" \
  --arg StudyDate "20240923" \
  --arg Right_femur "41.8 cm" \
  --arg Left_femur "42.0 cm" \
  --arg Difference_femur "00.2 cm, left longer 0.5%" \
  --arg Right_tibia "34.5 cm" \
  --arg Left_tibia "34.3 cm" \
  --arg Difference_tibia "00.2 cm, right longer 0.6%" \
  --arg Total_right "76.3 cm" \
  --arg Total_left "76.3 cm" \
  --arg Difference_total "00.0 cm, equal 0.0%" \
  --argjson Left_femur_distance 1892 \
  --argjson Left_tibia_distance 1544 \
  --argjson Right_femur_distance 1886 \
  --argjson Right_tibia_distance 1555 \
  --arg AccessionNumber "100876169" \
  --arg StudyDescription "XR HIPS TO ANKLES LEG MEASUREMENTS" \
  --arg SeriesDescription "Lower limbs" \
  --arg BodyPartExamined "LEG" \
  --arg FieldOfViewDimensions "[975, 391]" \
  --arg StationName "EOSRM7" \
  --argjson vector "[${VECTOR}]" \
  '{
    study_id: $study_id,
    info: {
      PatientID: $PatientID,
      PatientName: $PatientName,
      PatientAge: $PatientAge,
      StudyDate: $StudyDate
    },
    femur: {
      "Right femur": $Right_femur,
      "Left femur": $Left_femur,
      Difference: $Difference_femur
    },
    tibia: {
      "Right tibia": $Right_tibia,
      "Left tibia": $Left_tibia,
      Difference: $Difference_tibia
    },
    total: {
      "Total right": $Total_right,
      "Total left": $Total_left,
      Difference: $Difference_total
    },
    pixel_distance: {
      "Left femur": $Left_femur_distance,
      "Left tibia": $Left_tibia_distance,
      "Right femur": $Right_femur_distance,
      "Right tibia": $Right_tibia_distance
    },
    details: {
      AccessionNumber: $AccessionNumber,
      StudyDescription: $StudyDescription,
      SeriesDescription: $SeriesDescription,
      BodyPartExamined: $BodyPartExamined,
      FieldOfViewDimensions: $FieldOfViewDimensions,
      StationName: $StationName
    },
    vector: $vector
  }' > patient_record.json
