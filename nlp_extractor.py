import os
import spacy
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Disable parallelism to avoid threading issues
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load tokenizer and model for entailment
tokenizer = AutoTokenizer.from_pretrained("typeform/distilbert-base-uncased-mnli")
model = AutoModelForSequenceClassification.from_pretrained("typeform/distilbert-base-uncased-mnli")
model.eval()

# Candidate labels for O-1A criteria
CANDIDATE_LABELS = [
    "Awards",
    "Memberships",
    "Press Mentions",
    "Judging",
    "Original Contribution",
    "Scholarly Articles",
    "Critical Employment",
    "High Remuneration"
]

# Templates for entailment
templates = {
    "Awards": [
        "This text describes receiving prestigious awards, honors, or recognitions.",
        "This text highlights winning an award or being honored for excellence.",
    ],
    "Memberships": [
        "This text mentions memberships in exclusive organizations or societies.",
        "The individual is part of elite professional associations.",
    ],
    "Press Mentions": [
        "The text discusses significant press coverage or media features.",
        "This text highlights coverage in major media outlets or interviews.",
    ],
    "Judging": [
        "The text highlights participation as a judge or evaluator in competitions or panels.",
        "This text mentions judging roles or being part of evaluation committees.",
    ],
    "Original Contribution": [
        "This text describes innovative contributions or breakthroughs.",
        "The individual pioneered new methods or technologies that disrupted the field.",
    ],
    "Scholarly Articles": [
        "This text mentions publishing scholarly articles, research papers, or studies.",
        "The text indicates contributions to academic journals or conferences.",
    ],
    "Critical Employment": [
        "The text outlines critical roles and responsibilities in leading organizations.",
        "This text describes key employment positions that drove significant success.",
    ],
    "High Remuneration": [
        "This text provides evidence of high compensation, salary, or financial rewards.",
        "The individual commands a compensation package that exceeds industry norms.",
    ]
}

# Keywords for each criterion to help filter evidence
KEYWORDS = {
    "Awards": ["award", "honor", "recognition", "excellence"],
    "Memberships": ["member", "membership", "society", "association"],
    "Press Mentions": ["press", "media", "interview", "feature"],
    "Judging": ["judge", "judged", "panel", "evaluate", "evaluator"],
    "Original Contribution": ["contribution", "innovative", "pioneer", "developed"],
    "Scholarly Articles": ["paper", "article", "published", "journal"],
    "Critical Employment": ["senior", "lead", "engineer", "developer", "manager"],
    "High Remuneration": ["salary", "compensation", "remuneration", "earn"]
}

def classify_text(premise: str, candidate_labels: list) -> list:
    """
    For each candidate label, create hypotheses using its templates and compute the entailment.
    Use the maximum score among templates.
    """
    probabilities = []

    for label in candidate_labels:
        label_scores = []
        if label in templates:
            for template in templates[label]:
                inputs = tokenizer.encode_plus(premise, template, return_tensors="pt", truncation=True)
                with torch.no_grad():
                    logits = model(**inputs).logits
                probs = torch.softmax(logits, dim=1).squeeze()
                entailment_prob = probs[2].item()  # entailment probability
                label_scores.append(entailment_prob)
        max_score = max(label_scores) if label_scores else 0
        probabilities.append(max_score)
    
    return probabilities

def sentence_contains_keyword(sentence: str, keywords: list) -> bool:
    """Check if the sentence contains any of the specified keywords (case-insensitive)."""
    sentence_lower = sentence.lower()
    return any(keyword in sentence_lower for keyword in keywords)

def extract_evidence(cv_text: str) -> dict:
    """
    Split the CV text into sentences and assess each sentence for O-1A criteria.
    For each criterion, store sentences (with their score) that meet a threshold and contain relevant keywords.
    If no valid evidence is found for a criterion, reset its score to zero.
    Finally, select the top few evidence sentences per criterion.
    """
    doc = nlp(cv_text)
    criteria_scores = {label: 0.0 for label in CANDIDATE_LABELS}
    evidence_data = {label: [] for label in CANDIDATE_LABELS}
    
    # Set a threshold for considering a sentence as valid evidence.
    threshold = 0.3

    for sent in doc.sents:
        sentence_text = sent.text.strip()
        if len(sentence_text) < 10:
            continue
        
        # Compute maximum entailment probability for each criterion
        scores = classify_text(sentence_text, CANDIDATE_LABELS)
        
        for label, score in zip(CANDIDATE_LABELS, scores):
            # Update maximum score (this is prior to filtering by keyword)
            if score > criteria_scores[label]:
                criteria_scores[label] = score
            # Add sentence as evidence if it meets threshold and contains at least one relevant keyword.
            if score >= threshold and sentence_contains_keyword(sentence_text, KEYWORDS[label]):
                evidence_data[label].append((sentence_text, score))
    
    # If no valid evidence was found for a criterion, reset its score to zero.
    for label in CANDIDATE_LABELS:
        if not evidence_data[label]:
            criteria_scores[label] = 0.0

    # For each criterion, sort and select the top evidence sentences.
    criteria_evidence = {}
    top_n = 2  # adjust as needed
    for label in CANDIDATE_LABELS:
        sorted_evidence = sorted(evidence_data[label], key=lambda x: x[1], reverse=True)
        top_evidence = [sentence for sentence, _ in sorted_evidence[:top_n]]
        criteria_evidence[label] = top_evidence

    return {
        "criteria_scores": criteria_scores,
        "criteria_evidence": criteria_evidence
    }
