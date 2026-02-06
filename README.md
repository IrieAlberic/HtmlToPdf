# HTML to PDF Service

A FastAPI backend to convert HTML content (including JavaScript/Plotly charts) into PDF using Playwright.

## 🚀 Deployment

Since you are using **n8n Cloud**, this service must be hosted on a public server or a cloud platform like Render, Railway, or Fly.io.

### Option A: Deploy to Render (Recommended)
1. Push this directory to a GitHub repository.
2. Create a new **Web Service** on Render.
3. Connect your repository.
4. Render should automatically detect the `Dockerfile`.
5. Deploy.
6. Use the provided URL (e.g., `https://my-pdf-service.onrender.com`).

### Option B: Run with Docker
If you have a VPS or local server with a tunnel:
```bash
docker build -t html-to-pdf .
docker run -p 8000:8000 html-to-pdf
```

## 🔌 API Usage

**Endpoint:** `POST /generate-pdf`

**Headers:** `Content-Type: application/json`

**Body:**
```json
{
  "html": "<!DOCTYPE html><html>...</html>",
  "filename": "my-report.pdf"
}
```

### Integration with n8n
1. Use the **HTTP Request** node.
2. Method: `POST`.
3. URL: `YOUR_SERVICE_URL/generate-pdf`.
4. Body Content Type: `JSON`.
5. Body Parameters:
   - `html`: `{{ $json.html_report }}` (Connect from your Code node).
   - `filename`: `{{ $json.job_id }}_report.pdf`.
6. **Important**: In the HTTP Request node, set "Response Format" to **File**. All the binary data will be handled automatically.

## 🛠️ Local Development
1. `pip install -r requirements.txt`
2. `playwright install chromium`
3. `uvicorn main:app --reload`
