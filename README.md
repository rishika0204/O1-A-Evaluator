# O1A Insight
**O1A Insight** is an AI-driven application designed to assist individuals and attorneys in assessing qualifications for the O-1A visa, which is intended for individuals with extraordinary abilities in the sciences, arts, education, business, or athletics. The application evaluates CVs against the specific evidentiary criteria required for the O-1A visa classification.

## Features
- **CV Processing:** Extracts text from uploaded CV files (PDF and text formats supported).
- **Criteria Assessment:** Uses NLP (Natural Language Processing) and ML (Machine Learning) to evaluate CV text against the eight O-1A criteria.
- **Qualification Rating:** Provides a probabilistic qualification rating (High, Medium, Low) based on the assessment.

## Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourgithub/o1a-insight.git
   cd o1a-insight
   ```

2. **Install Dependencies:**
   Ensure you have Python 3.8+ installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   uvicorn main:app --reload
   ```
   Access the API at: `http://127.0.0.1:8000`

## Usage
To use **O1A Insight**, follow these steps:
1. **Start the Application:** Run the application using Uvicorn as described above.
2. **Upload a CV:** Use the `/assess-cv/` endpoint to upload a CV file. The API expects a POST request with the file included in the form data.
   ```bash
   curl -X 'POST' \
     'http://127.0.0.1:8000/assess-cv/' \
     -H 'accept: application/json' \
     -H 'Content-Type: multipart/form-data' \
     -F 'file=@path_to_your_cv.pdf;type=application/pdf'
   ```

3. **Review Results:** The response will include the criteria scores, evidence extracted for each criterion, and an overall qualification rating.

## Modules Description
- **`cv_processor.py`**: Handles the extraction of text from uploaded CV files.
- **`nlp_extractor.py`**: Implements the NLP logic to assess CV text against the O-1A criteria.
- **`evaluator.py`**: Calculates the overall qualification rating based on criteria scores.
- **`main.py`**: Contains the FastAPI application setup and endpoints.

## Contributions
Contributions are welcome! Please fork the repository and submit pull requests with your suggested changes.
