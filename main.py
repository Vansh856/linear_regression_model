from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app=FastAPI()

conn=sqlite3.connect("STUDENT.db",check_same_thread=False)
conn.execute("CREATE TABLE IF NOT EXISTS names(name TEXT)")
conn.commit()
conn.close()

class student(BaseModel):
    name : str

@app.post("/save")
def save_name(data: student):
    conn=sqlite3.connect("STUDENT.db")
    print("Connecting to database")
    conn.execute("INSERT INTO names VALUES (?)",(data.name,))
    conn.commit()
    conn.close()
    return{"status":"Success"}

@app.get("/get_all")
def get_names():
    conn=sqlite3.connect("STUDENT.db")
    corser=conn.cursor()

    corser.execute("SELECT name FROM names")
    rows=corser.fetchall()
    conn.close()

    name_list=[row[0] for row in rows]
    return {"students":name_list}

@app.delete("/delete_it")
def reset():
    conn=sqlite3.connect("STUDENT.db")
    corser=conn.cursor()
    corser.execute("DELETE FROM names")
    conn.commit()
    conn.close()
    return {"status":"SUCCESS","Message":"Dataabase Restored"}
    