# AI Compliance MVP

This repository contains a bare‑bones **Minimum Viable Product (MVP)** for an AI‑powered compliance and due‑diligence tool.  It is intentionally lightweight to allow rapid prototyping and is **not** production ready.  Use this as a starting point to build a vertically focused AI SaaS for legal/compliance workflows.

## Overview

The MVP consists of:

* **Backend (Python/FastAPI)** – Provides endpoints for file upload and rudimentary document analysis.  The analysis endpoint currently returns dummy data; integrate an LLM and vector database here to implement real due‑diligence checks.
* **Frontend (React/Vite)** – A simple React single‑page application with a file upload form and results view.  It uses Tailwind CSS for styling and demonstrates how to interact with the backend API.
* **Lead Scraper** – A proof‑of‑concept Python script that scrapes company web pages to find email addresses.  It can be extended to build outreach lists for sales.

## Running the Backend

1. Navigate to the `backend` directory.
2. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Start the server:

   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`.  You can test file uploads and analysis using a tool like `curl` or Postman.

## Running the Frontend

This project uses [Vite](https://vitejs.dev/) for local development.  To run the frontend:

1. Navigate to the `frontend` directory.
2. Install Node dependencies:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm run dev
   ```

The app will run at `http://localhost:5173` by default.  Update the API base URL in `src/api.js` if your backend runs on a different port.

## Lead Scraper

The script in `scripts/lead_scraper.py` demonstrates how to extract email addresses from a list of company URLs using `requests` and `BeautifulSoup`.  In production, you should replace this with a more robust solution that handles JavaScript‑rendered sites (e.g. using Playwright or Selenium) and enriches contacts via third‑party APIs.

To run:

```bash
python scripts/lead_scraper.py
```

## Notes

* **LLM integration:** The `backend/main.py` file includes a placeholder `analyze_document` function.  Replace its content with calls to your chosen language model and vector database to perform actual compliance checks.  Ensure the model outputs verifiable citations to mitigate hallucinations.
* **Security:** Do not deploy this MVP to production as‑is.  Add authentication, input validation, rate limiting, and logging.
* **Compliance:** When processing sensitive data, follow GDPR and other relevant regulations.  Provide clear privacy notices and implement proper data handling.
