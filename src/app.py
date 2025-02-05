import os
import re
import subprocess
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()

def get_ip_address():
    try:
        result = subprocess.run(["ip", "a"], capture_output=True, text=True, check=True)
        ip_pattern = re.findall(r"inet (\d+\.\d+\.\d+\.\d+)", result.stdout)
        for ip in ip_pattern:
            if not ip.startswith("127."):
                return ip
    except Exception as erro:
        return f"Erro ao procurar o IP: {erro}"

@app.get("/", response_class=HTMLResponse)
async def read_root():
    app_id = os.getenv("HOSTNAME", "App não identificado!!!")
    app_ip = get_ip_address()
    
    html_path = Path(__file__).parent / "templates/index.html"
    html_content = html_path.read_text()
    html_content = html_content.replace("{{APP_ID}}", app_id)
    html_content = html_content.replace("{{APP_IP}}", app_ip)
    
    return HTMLResponse(content=html_content)
