import psycopg2
from psycopg2 import sql

# Definition of a function to create a table in a PostgreSQL database
def create_table(conn):
    cur = conn.cursor()

    # Name of the table to be created
    table_name = "video_data"
    # Dictionary to define the fields for the table to be created.
    fields = {
        "clip_name": "TEXT",
        "clip_file_extension": "TEXT",
        "clip_duration": "FLOAT",
        "clip_location": "TEXT",
        "insert_timestamp": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    }

    # Executing the SQL command to create the table
    cur.execute(
        sql.SQL("CREATE TABLE {} ({})").format(
            # Using the table name as an SQL Identifier for safety
            sql.Identifier(table_name),
            # Joining the field names and types together, separated by commas
            sql.SQL(", ").join(sql.SQL("{} {}").format(sql.Identifier(k), sql.SQL(v)) for k, v in fields.items())
        )
    )
    # Committing the transaction to the database
    conn.commit()



if __name__ == "__main__":
    # Establishing a connection to the PostgreSQL database
    conn = psycopg2.connect(database="apexdb", user="postgres", password="your_password", host="127.0.0.1", port="5432")
    create_table(conn)
