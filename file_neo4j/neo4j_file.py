import pandas as pd
from neo4j import GraphDatabase

# Load the CSV file
file_path = r"C:\Users\SUPER\Downloads\Smart Slab Panel Formwork System.csv"
df = pd.read_csv(file_path)

# Connection parameters
uri = "bolt://localhost:7687"  # Replace with your Neo4j instance URI
username = "neo4j"  # Replace with your Neo4j username
password = "Bappa@143"  # Replace with your Neo4j password

# Create a driver instance
driver = GraphDatabase.driver(uri, auth=(username, password))

# Function to run a list of Cypher queries
def execute_queries(queries):
    with driver.session() as session:
        for query in queries:
            try:
                session.run(query)
                print(f"Executed: {query}")
            except Exception as e:
                print(f"Failed to execute: {query}\nError: {e}")

# Prepare Cypher queries
queries = []

# Create nodes for each task and its associated resources
for index, row in df.iterrows():
    task_id = row['WBS'].replace('.', '_')  # Replace '.' with '_'
    task_name = row['Name'].replace("'", "\\'")
    resources = str(row['Resource_Names']).split(',') if pd.notna(row['Resource_Names']) else []

    # Create task node
    queries.append(f"CREATE (t{task_id}:Task {{id: '{row['WBS']}', name: '{task_name}'}});")

    # Create resource nodes and relationships
    for resource in resources:
        resource = resource.strip()
        if resource:  # Ensure the resource is not an empty string
            queries.append(f"MERGE (r:Resource {{name: '{resource}'}});")
            queries.append(f"CREATE (r)-[:ASSIGNED_TO]->(t{task_id});")

# Create relationships based on Predecessors
for index, row in df.iterrows():
    task_id = row['WBS'].replace('.', '_')  # Replace '.' with '_'
    predecessors = str(row['Predecessors']).split(',') if pd.notna(row['Predecessors']) else []

    for predecessor in predecessors:
        predecessor = predecessor.strip().replace('.', '_')  # Replace '.' with '_'
        if predecessor and predecessor != 'nan':  # Ensure predecessor is valid
            queries.append(f"MATCH (t1:Task {{id: '{predecessor}'}}), (t2:Task {{id: '{row['WBS']}'}})")
            queries.append(f"CREATE (t1)-[:PRECEDES]->(t2);")

# Execute the queries
if __name__ == "__main__":
    execute_queries(queries)

# Close the driver after use
driver.close()
