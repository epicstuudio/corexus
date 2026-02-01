from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="Corexus Backend",
    description="The FastAPI backend for the Corexus intelligent assistant.",
    version="0.1.0",
)

@app.get("/")
async def root():
    return {"message": "Welcome to Corexus Backend!"}

@app.get("/status")
async def get_status():
    return {"status": "operational", "version": app.version}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
# Initial comment
# Another comment to trigger deployment
