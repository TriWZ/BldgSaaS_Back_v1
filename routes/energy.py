
from fastapi import APIRouter, UploadFile, File, HTTPException
from models.energy_model import EnergyRecord
from database import SessionLocal
import pandas as pd
import sqlite3
import io

router = APIRouter()

@router.get("/")
def health_check():
    return {"message": "Energy route active"}

@router.get("/data")
def get_energy_data():
    try:
        conn = sqlite3.connect("triphorium.db")
        df = pd.read_sql("SELECT * FROM building_data", conn)
        conn.close()
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
def upload_energy_csv(file: UploadFile = File(...)):
    try:
        content = file.file.read().decode("utf-8")
        df = pd.read_csv(io.StringIO(content))
        expected_cols = {"building_id", "timestamp", "electricity_kwh", "water_tons", "gas_m3", "co2_tons"}
        if not expected_cols.issubset(set(df.columns)):
            raise HTTPException(status_code=400, detail="Missing required columns.")
        conn = sqlite3.connect("triphorium.db")
        for _, row in df.iterrows():
            conn.execute("""
                INSERT INTO building_data (building_id, timestamp, electricity_kwh, water_tons, gas_m3, co2_tons)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                int(row["building_id"]), row["timestamp"], float(row["electricity_kwh"]),
                float(row["water_tons"]), float(row["gas_m3"]), float(row["co2_tons"])
            ))
        conn.commit()
        conn.close()
        return {"status": "success", "inserted": len(df)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
