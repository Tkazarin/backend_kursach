import uvicorn

if __name__ == "__main__":
    uvicorn.run("users.api:users", host="0.0.0.0", port=8081, reload=True)