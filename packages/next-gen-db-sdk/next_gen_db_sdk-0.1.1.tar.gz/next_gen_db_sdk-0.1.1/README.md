# NextGenDB SDK

Usage Example

```py

from next_gen_db_sdk import NextGenDBClient, NextGenDBError, NotFoundError

# Initialize the client with the base URL of the next-gen-db server
client = NextGenDBClient(base_url="http://localhost:8047")

# --- Document operations ---
try:
    # Create a document
    client.create_document("user_1", {"name": "John Doe", "age": 30})
    
    # Retrieve the document
    document = client.get_document("user_1")
    print("Document retrieved:", document)

    # Update the document
    client.update_document("user_1", {"name": "John Doe", "age": 31})
    
    # Delete the document
    client.delete_document("user_1")

except NotFoundError as e:
    print(f"Error: {e}")
except NextGenDBError as e:
    print(f"General error: {e}")

# --- Graph operations ---
try:
    # Add a node
    client.add_node("person_1", {"name": "Alice", "age": 25})
    
    # Add an edge (relationship)
    client.add_edge("person_1", "person_2", "friends")
    
    # Retrieve the node
    node = client.get_node("person_1")
    print("Node retrieved:", node)
    
    # Retrieve the edge
    edge = client.get_edge("person_1", "person_2")
    print("Edge retrieved:", edge)

except NextGenDBError as e:
    print(f"Graph error: {e}")

```
