import psycopg2
from psycopg2 import sql


def create_table(conn):
    cur = conn.cursor()
    table_name = "video_data"
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
            sql.Identifier(table_name),
            sql.SQL(", ").join(sql.SQL("{} {}").format(sql.Identifier(k), sql.SQL(v)) for k, v in fields.items())
        )
    )
    conn.commit()



if __name__ == "__main__":
    # Establishing a connection to the PostgreSQL database
    conn = psycopg2.connect(database="apexdb", user="postgres", host="127.0.0.1", port="5432")
    create_table(conn)
