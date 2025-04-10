from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from Hybrid_Rag_Ui_Table import query_rag_system

app = FastAPI()

# Allow all CORS origins (for Streamlit frontend if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check route
@app.get("/health")
def health():
    return {"status": "ok"}

# Request model
class QueryRequest(BaseModel):
    query: str

# Recommend route
@app.post("/recommend")
def recommend_assessments(query_request: QueryRequest):
    query = query_request.query
    results, _ = query_rag_system(query)

    # Convert to plain list of dicts
    recommendations = []
    for _, row in results.iterrows():
        recommendations.append({
            "url": row["Download URL"] if "Download URL" in row else row["URL"],
            "adaptive_support": "Yes" if row["Adaptive/IRT"] == "✅" else "No",
            "remote_support": "Yes" if row["Remote"] == "✅" else "No",
            "duration": int(float(row["Duration (min)"])) if pd.notna(row["Duration (min)"]) else 0,

            "description": row.get("Test Type", ""),
            "test_type": [s.strip() for s in row.get("Test Type", "").split(",") if s.strip()]
        })

    return {"recommended_assessments": recommendations}
