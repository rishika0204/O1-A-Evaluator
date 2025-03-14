# O1A Insight
**O1A Insight** is an AI-driven application designed to assist individuals and attorneys in assessing qualifications for the O-1A visa, intended for individuals with extraordinary abilities in the sciences, arts, education, business, or athletics. The application evaluates CVs against the specific evidentiary criteria required for the O-1A visa classification using advanced ML and NLP techniques.

## Features
- **CV Processing:** Extracts text from uploaded CV files (PDF and text formats supported).
- **Criteria Assessment:** Uses NLP and ML to evaluate CV text against the eight O-1A criteria.
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
   **Note:** For interactive API documentation, navigate to `http://127.0.0.1:8000/docs`.

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

## Technical Details

### ML and NLP in O1A Insight
**O1A Insight** leverages ML and NLP to automate the evaluation of complex legal immigration criteria:

- **Text Extraction (`cv_processor.py`):** Utilizes PyPDF2 for extracting text from PDF files, ensuring all content from a CV is accessible for analysis.
- **NLP Processing (`nlp_extractor.py`):**
  - **spaCy:** Employs spaCy for text preprocessing, including tokenization and sentence boundary detection, which structures CV text into analyzable segments.
  - **Transformers:** Uses the `distilbert-base-uncased-mnli` model to perform semantic similarity and entailment checks between extracted text and predefined criteria templates. This process assesses how well each sentence aligns with specific criteria (e.g., receiving awards, membership in elite organizations).
- **Evidence Evaluation (`evaluator.py`):** Applies a heuristic based on the strength of evidence detected by the NLP analysis. It aggregates scores across multiple criteria to generate an overall qualification rating (High, Medium, Low).

### Criteria Assessment Mechanism
The application assesses each criterion by:
- Identifying key phrases and concepts that match the O-1A requirements using advanced NLP techniques.
- Scoring each criterion based on the presence and relevance of evidence within the CV.
- Aggregating these scores to render an overall assessment of the applicant’s potential eligibility for the O-1A visa.

## Contributions
Contributions are welcome! Please fork the repository and submit pull requests with your suggested changes.
