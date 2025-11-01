"""
FastAPI backend for the AI compliance MVP.

This module defines a simple API with two primary endpoints:

* **/upload** – accepts file uploads and stores them in memory.
* **/analyze** – performs a rudimentary analysis on an uploaded file and returns
  a dummy compliance report.  Replace the analysis logic with calls to your
  language model and vector database for real‑world use.

The backend stores uploaded files in memory for demonstration purposes and
should not be used in production.  Add persistent storage and proper
authentication for a real deployment.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Tuple, Any

# Additional imports for basic document parsing
import io
import re
import statistics
try:
    # PyPDF2 is used for PDF text extraction. It's optional and will only
    # be available if installed in the backend virtualenv. If it's not
    # present, PDF extraction will fall back to returning an empty string.
    import PyPDF2  # type: ignore
except ImportError:
    PyPDF2 = None  # type: ignore

app = FastAPI(title="AI Compliance MVP", version="0.1.0")

# Allow all CORS origins for development; restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    """Model for analysis requests."""

    file_id: str

class AnalysisResult(BaseModel):
    """Model for analysis results.

    The `details` field can contain arbitrary JSON‑serialisable
    data such as lists (e.g., flagged terms) and strings (e.g., recommendations).
    """

    file_id: str
    summary: str
    risk_score: float
    details: Dict[str, any]


def extract_text_from_pdf(data: bytes) -> str:
    """Extract text from a PDF file using PyPDF2 if available.

    Args:
        data: The raw bytes of a PDF document.

    Returns:
        A string containing the extracted text or an empty string if extraction
        fails.
    """
    if not PyPDF2:
        return ""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(data))
        text = []
        for page in reader.pages:
            try:
                page_text = page.extract_text() or ""
            except Exception:
                page_text = ""
            text.append(page_text)
        return "\n".join(text)
    except Exception:
        return ""


def simple_text_analysis(text: str) -> Dict[str, any]:
    """Perform a naive risk analysis on the given text.

    This function looks for predefined risk keywords and computes a basic
    risk score based on their frequency. It also extracts flagged sections
    around each occurrence of a risk keyword.

    Args:
        text: The input text to analyse.

    Returns:
        A dictionary with a summary, risk score and details including
        flagged sections and recommendations.
    """
    # Define a list of risk-related keywords to search for. These terms can
    # be expanded based on domain expertise and the types of risks you want
    # to surface (e.g., sanctions, corruption, bribery, legal violation).
    risk_keywords: List[str] = [
        "risk", "fraud", "penalty", "sanction", "compliance", "violation",
        "fine", "investigation", "legal", "lawsuit", "breach", "corruption",
        "bribery", "scandal", "regulatory", "audit", "failure", "misconduct",
        "whistleblower", "dispute", "conflict", "violate", "punish"
    ]

    # Normalize text for analysis
    lower_text = text.lower()
    words = re.findall(r"\b\w+\b", lower_text)
    total_words = len(words) if words else 1

    # Count occurrences of risk keywords
    occurrences: List[Tuple[int, int]] = []
    for kw in risk_keywords:
        for match in re.finditer(rf"\b{re.escape(kw)}\b", lower_text):
            occurrences.append(match.span())

    risk_count = len(occurrences)
    risk_score = min(risk_count / total_words * 10.0, 1.0)  # scale to 0–1

    # Extract flagged sections: capture 50 characters before and after each match
    flagged_sections: List[str] = []
    for start, end in occurrences[:10]:  # limit to first 10 sections to keep response concise
        snippet_start = max(0, start - 50)
        snippet_end = min(len(text), end + 50)
        snippet = text[snippet_start:snippet_end].strip()
        flagged_sections.append(snippet)

    # Create a simple summary: take the first 3 sentences
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    summary_sentences = sentences[:3]
    summary = " ".join(summary_sentences) if summary_sentences else text[:200]

    # Prepare details with flagged sections and simple recommendations
    details: Dict[str, str] = {
        "flagged_sections": "\n\n".join(flagged_sections) if flagged_sections else "None",
        "recommendations": (
            "Review the flagged sections for potential legal or compliance issues. "
            "Consider engaging a compliance specialist to evaluate identified risks."
            if flagged_sections else
            "No obvious risk keywords detected. Continue with standard due diligence checks."
        ),
    }

    return {
        "summary": summary,
        "risk_score": float(risk_score),
        "details": details,
    }

# -----------------------------------------------------------------------------
# Enhanced risk scoring logic
#
# This section embeds an improved risk scoring function similar to the one in
# `risk_scoring_v2.py`. It applies weights to different risk terms and
# generates a summary highlighting sentences containing those terms.
# -----------------------------------------------------------------------------
RISK_WEIGHTS: Dict[str, int] = {
    'fraud': 20,
    'bribery': 15,
    'sanctions': 25,
    'bankruptcy': 10,
    'money laundering': 30,
    'litigation': 10,
    'regulatory fines': 20,
    'tax evasion': 15,
    'data breach': 20,
    'antitrust': 15,
}

def enhanced_risk_analysis(text: str) -> Dict[str, any]:
    """Perform an enhanced risk analysis using weighted terms.

    Args:
        text: The input text to analyse.

    Returns:
        A dictionary with summary, risk_score (0‑1), and details including
        flagged terms and a summary of sentences containing them.
    """
    lower = text.lower()
    flagged: List[str] = []
    score = 0
    for term, weight in RISK_WEIGHTS.items():
        if term in lower:
            flagged.append(term)
            score += weight
    # normalise score (cap at 100 and scale to 0‑1)
    risk_score = min(score / 100.0, 1.0)
    # generate summary: select sentences with flagged terms
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    summary_sentences: List[str] = []
    for s in sentences:
        if any(term in s.lower() for term in flagged):
            summary_sentences.append(s)
    if not summary_sentences and sentences:
        summary_sentences.append(sentences[0])
    summary = '. '.join(summary_sentences) + ('.' if summary_sentences else '')
    details: Dict[str, any] = {
        'flagged_terms': flagged,
        'recommendations': (
            'Review the highlighted sentences for potential compliance issues.'
            if flagged else
            'No high‑severity risk terms detected; continue standard due diligence.'
        ),
    }
    return {
        'summary': summary,
        'risk_score': float(risk_score),
        'details': details,
    }

# In‑memory store for uploaded files and analyses
FILES: Dict[str, bytes] = {}
ANALYSES: Dict[str, AnalysisResult] = {}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> Dict[str, str]:
    """Upload a file for analysis.  Returns a file identifier."""
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Empty file")
    file_id = f"file_{len(FILES) + 1}"
    FILES[file_id] = contents
    return {"file_id": file_id, "filename": file.filename}


@app.post("/analyze")
async def analyze(req: AnalysisRequest) -> AnalysisResult:
    """Perform an analysis on a previously uploaded file.

    This implementation performs a basic compliance check without calling
    external services. It extracts text from the uploaded document
    (supporting PDF files via PyPDF2 if installed) and looks for
    predefined risk keywords. The risk score is computed based on the
    frequency of risk terms relative to the total word count. A simple
    summary and flagged sections are returned.
    """
    file_id = req.file_id
    if file_id not in FILES:
        raise HTTPException(status_code=404, detail="File not found")

    data = FILES[file_id]

    # Determine if the file is a PDF by checking its header
    if data[:4] == b"%PDF":
        text = extract_text_from_pdf(data)
    else:
        # Assume the file is plain text or a text‑based document
        try:
            text = data.decode("utf-8", errors="ignore")
        except Exception:
            text = ""

    # If extraction failed, fallback to using a short preview
    if not text:
        text = data[:500].decode(errors="ignore")

    # Use enhanced risk analysis for more nuanced scoring and summaries
    analysis = enhanced_risk_analysis(text)

    result = AnalysisResult(
        file_id=file_id,
        summary=analysis["summary"],
        risk_score=analysis["risk_score"],
        details=analysis["details"],
    )
    ANALYSES[file_id] = result
    return result


@app.get("/analysis/{file_id}")
async def get_analysis(file_id: str) -> AnalysisResult:
    """Retrieve a previously computed analysis."""
    if file_id not in ANALYSES:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return ANALYSES[file_id]