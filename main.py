from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import our modules
from cv_processor import extract_text_from_file
from nlp_extractor import extract_evidence
from evaluator import evaluate_evidence

app = FastAPI(
    title="O-1A Visa Qualification Assessor",
    description="Assess CVs against O-1A evidentiary criteria using NLP and ML, and provide a probabilistic qualification rating.",
    version="2.0"
)

# Enable CORS for all origins (for development only; restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/assess-cv/")
async def assess_cv(file: UploadFile = File(...)):
    """
    Endpoint to upload a CV file. Processes the file to:
      - Extract text from the CV.
      - Use spaCy and a transformer model to assign probabilistic scores for each O-1A criterion.
      - Extract evidence (sentences/accomplishments) corresponding to each criterion.
      - Compute an overall qualification rating.
    Returns a JSON response with the criteria scores, evidence for each criterion, and overall rating.
    """
    try:
        # Extract text from the uploaded file.
        cv_text = extract_text_from_file(file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Extract evidence (probabilistic scores and evidence sentences) using our NLP module.
    extraction_results = extract_evidence(cv_text)
    criteria_scores = extraction_results["criteria_scores"]
    criteria_evidence = extraction_results["criteria_evidence"]
    
    # Evaluate the overall rating based on criteria scores.
    qualification_rating = evaluate_evidence(criteria_scores)
    
    return {
        "criteria_scores": criteria_scores,
        "criteria_evidence": criteria_evidence,
        "qualification_rating": qualification_rating
    }
