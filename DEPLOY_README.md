# Deployment Instructions

This document provides step‑by‑step instructions to deploy the AI Compliance Assistant without purchasing a domain.  You may choose one of the following options depending on your preferences.  Each option yields a public HTTPS link for your demo.

## Prerequisites

* Have a GitHub account.  Push this repository (or the `mvp_project/` directory) to a new repository.  
* Have accounts on the chosen platform (Render, Fly.io, Railway) if using those services.  
* For local demos with `ngrok`, install the `ngrok` CLI.

## Option A – Render (Free tier)

Render can host Python and static sites easily.  You will create two services: one for the backend API and one for the front‑end.

1. Create a new private GitHub repository and push the contents of the `mvp_project` directory.  Ensure the `backend` and `frontend` subdirectories are included.
2. Log into [Render](https://dashboard.render.com) and click **New → Web Service**.
3. Connect your GitHub account and select the repository.
4. Configure the **backend service**:
   * Environment: **Python**
   * Build Command: `pip install --no-cache-dir -r requirements.txt`
   * Start Command: `uvicorn main:app --host 0.0.0.0 --port 8000`
   * Root Directory: `backend`
   * Free plan is sufficient for demo.
5. Create a **second web service** for the **frontend**:
   * Environment: **Static**
   * Build Command: `npm ci --legacy-peer-deps && npm run build`
   * Static Publish Path: `dist`
   * Root Directory: `frontend`
6. After deployment, Render will provide two public URLs.  Update your frontend’s API endpoint (`src/api.js`) to point to the backend URL if needed.

## Option B – Fly.io (Docker)

Fly.io can run Docker images with a simple command.  Use the provided `fly.toml` files.

1. Install the Fly CLI: `curl -L https://fly.io/install.sh | sh` and run `fly auth signup`.
2. Navigate to the `mvp_project/backend` directory and run:
   ```
   fly launch --copy-config --now --config ../fly.toml
   ```
   This creates and deploys the backend.  Replace `your-backend-app-name` in `fly.toml` with a unique name.
3. Deploy the frontend from `mvp_project/frontend`:
   ```
   fly launch --copy-config --now --config ../fly-frontend.toml
   ```
4. Fly will assign `https://<app>.fly.dev` URLs for each service.

## Option C – Railway

Railway offers simple deployment from a repository.

1. After pushing the repository to GitHub, log in to [Railway](https://railway.app) and click **New Project → Deploy from GitHub**.
2. Select the repository and choose the `railway.backend.json` blueprint for the backend service.  The CLI will build and run the backend.
3. Repeat for the frontend using `railway.frontend.json`.  Railway will provide subdomain URLs for each.

## Option D – Local Demo with ngrok

If you prefer not to use any cloud provider, you can run the application locally and expose it via `ngrok`.

1. Install dependencies in the backend:
   ```
   cd mvp_project/backend
   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
2. In another terminal, run the frontend locally:
   ```
   cd mvp_project/frontend
   npm ci
   npm run dev
   ```
3. Install ngrok and expose the backend (and optionally frontend) ports:
   ```
   ngrok http 8000   # Exposes backend
   ngrok http 5173   # Exposes frontend (optional)
   ```
   Copy the forwarding URLs from ngrok and update the frontend API endpoint accordingly.

## Environment Variables

For demonstration purposes the backend does not require external secrets.  If you integrate external APIs or databases, create a `.env` file and map variables into your deployment configuration.

## Next Steps

Once deployed, test the API and UI by uploading sample documents.  Use the provided `case_study.md` and `pilot_onboarding_checklist.md` when engaging pilot customers.  For production deployment, ensure TLS termination, authentication, and environment variables are properly configured.