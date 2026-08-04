#initializes everything
#when repo is downloaded to start the program
#terminal -> python run_app.py

#should load the default data provided in /raw

import subprocess
import time
import load
if __name__ == "__main__":
    print("Starting FastAPI Backend: ")
    api_process = subprocess.Popen(["uvicorn", "api:app", "--port", "8000", "--reload"])
    print("Loading default data: ")
    time.sleep(5)
    load.main()
    print("Starting Streamlit Frontend")
    try:
        subprocess.run(["streamlit", "run", "app.py"])
    finally:
        print("Shutting down FastAPI Backend...")
        api_process.terminate()