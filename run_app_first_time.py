import subprocess
import time
import load
import sys

def ensure_postgres_running():
    # Service name varies by PostgreSQL version (check yours in services.msc)
    service_name = "postgresql-x64-16"
    
    try:
        # Check service status or attempt to start it
        result = subprocess.run(
            ["net", "start", service_name],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 or "already been started" in result.stdout:
            print("✅ PostgreSQL service is running.")
        else:
            print(f"❌ Failed to start service: {result.stderr}")
            
    except Exception as e:
        print(f"Error starting PostgreSQL: {e}")


if __name__ == "__main__":
    print("connecting to Postgres: ")
    ensure_postgres_running()
    print("Starting FastAPI Backend: ")
    api_process = subprocess.Popen(["uvicorn", "api:app", "--port", "8000", "--reload"])
    print("Loading default data: ")
    load.main()
    time.sleep(5)
    print("Starting Streamlit Frontend")
    try:
        subprocess.run(["streamlit", "run", "app.py"])
    finally:
        print("Shutting down FastAPI Backend...")
        api_process.terminate()