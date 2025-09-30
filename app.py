from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow

app = FastAPI(title="Gmail API OAuth", description="Professional OAuth interface for Gmail API access")

# 1. Define the scopes you need
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# 2. Create the OAuth flow
flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json',
    scopes=SCOPES,
    redirect_uri='http://localhost:8000/oauth2callback'  # FastAPI route
)

@app.get("/", response_class=HTMLResponse)
def index():
    # Serve the professional HTML interface
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Error: index.html not found</h1>", status_code=404)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading page: {str(e)}</h1>", status_code=500)

@app.get("/oauth2callback")
def oauth2callback(request: Request):
    code = request.query_params.get("code")
    error = request.query_params.get("error")

    if error:
        # Redirect back to main page with error
        return RedirectResponse(url=f"/?error={error}")

    if code:
        try:
            # Fetch token using the code from redirect
            flow.fetch_token(code=code)
            credentials = flow.credentials
            return RedirectResponse(url=f"/?success=true&access_token={credentials.token}&refresh_token={credentials.refresh_token}")
        except Exception as e:
            return RedirectResponse(url=f"/?error=token_exchange_failed&message={str(e)}")

    return RedirectResponse(url="/?error=no_code")

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Gmail OAuth API"}
