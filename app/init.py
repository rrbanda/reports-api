from config import get_neo4j_driver

class Neo4jConnectionManager:
    def __init__(self):
        self.driver = get_neo4j_driver()

    def close(self):
        if self.driver:
            self.driver.close()

    async def create_patient_record(self, patient_data: dict):
        query = """
        MERGE (p:Patient {PatientID: $PatientID})
        SET p += $info
        WITH p
        MERGE (f:Record {StudyDate: $StudyDate})
        SET f += $patient_data
        MERGE (p)-[:HAS_RECORD]->(f)
        RETURN p, f
        """
        async with self.driver.session() as session:
            result = await session.write_transaction(
                lambda tx: tx.run(query, **patient_data).data()
            )
        return result

    async def get_patient_record(self, patient_id: str):
        query = """
        MATCH (p:Patient {PatientID: $patient_id})-[:HAS_RECORD]->(r:Record)
        RETURN p, r
        """
        async with self.driver.session() as session:
            result = await session.run(query, patient_id=patient_id)
        return result.data()

    async def update_patient_record(self, patient_id: str, update_data: dict):
        query = """
        MATCH (p:Patient {PatientID: $patient_id})-[:HAS_RECORD]->(r:Record)
        SET r += $update_data
        RETURN p, r
        """
        async with self.driver.session() as session:
            result = await session.write_transaction(
                lambda tx: tx.run(query, patient_id=patient_id, update_data=update_data).data()
            )
        return result

    async def delete_patient_record(self, patient_id: str):
        query = """
        MATCH (p:Patient {PatientID: $patient_id})-[:HAS_RECORD]->(r:Record)
        DETACH DELETE p, r
        """
        async with self.driver.session() as session:
            await session.run(query, patient_id=patient_id)
        return {"status": "deleted"}
