import asyncio
import json
import urllib.parse
from fastapi.params import Header
from fastapi.responses import JSONResponse, PlainTextResponse
import requests
import fastapi

app = fastapi.FastAPI()

# Define the root endpoint
@app.get("/")
def read_root():
    return {"status": "ok"}

# Define the proxy endpoint -> https://hostname/proxy?url=stream_url&headers=headers&output=json/text
@app.get("/proxy")
async def proxy(
    url: str = fastapi.Query(..., description="The target URL to fetch"),
    headers: str = fastapi.Query(..., description="URL-encoded JSON headers"),
    output: str = fastapi.Query("text", description="Output format: json or text"),
    x_app_id: str = Header(None, convert_underscores=False)  # read "X-App-ID"
):
    # Validate App ID
    if x_app_id != "eu.org.nayankasturi.streamora":
        return JSONResponse({"error": "Unauthorized app"}, status_code=403)

    try:
        url = urllib.parse.unquote(url)
        decoded_headers = urllib.parse.unquote(headers)
        final_headers = json.loads(decoded_headers)
        response = await asyncio.to_thread(requests.get, url, headers=final_headers)
        if response.status_code == 200:
            if output.lower() == "json":
                try:
                    return JSONResponse(response.json())
                except json.JSONDecodeError:
                    return JSONResponse({"error": "Response is not valid JSON"}, status_code=502)
            return PlainTextResponse(response.text)
        else:
            return JSONResponse(
                {"error": f"{response.status_code} - {response.reason}"},
                status_code=response.status_code
            )
    except json.JSONDecodeError:
        return JSONResponse({"error": "Invalid JSON format for headers."}, status_code=400)
    except requests.RequestException as e:
        return JSONResponse({"error": str(e)}, status_code=502)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="localhost", port=8000)
