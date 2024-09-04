import json
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import scrape_router, post_sources_router,message_router 
from app.routers import get_sources_router, delete_sources_router,delete_Id_VS_router,get_slide_router, upload_router, files_router,extract_text_router
from db import chroma_setup
from app.helper.websocket_connections import active_websockets

# Use an async context manager for the lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run your startup code here
    await chroma_setup.setup_chroma(is_reset=True)

    # Yield control to the application to start handling requests
    yield

    # Run your shutdown code here (if any)

# Initialize the FastAPI application with the lifespan context manager
app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins (you can restrict this to specific origins)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Allow these HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(scrape_router.router)
app.include_router(post_sources_router.router)
app.include_router(get_sources_router.router)
app.include_router(delete_sources_router.router)
app.include_router(upload_router.router)
app.include_router(message_router.router)
app.include_router(files_router.router)
app.include_router(get_slide_router.router)
app.include_router(extract_text_router.router)
app.include_router(delete_Id_VS_router.router)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_websockets.add(websocket)
    try:
        while True:
            # Receive text (JSON) message from the client
            data = await websocket.receive_text()

            # Deserialize the JSON data from the client
            json_data = json.loads(data)
            print("Message received from client:", json_data)

            # Process the data (this is just an example)
            json_data["response"] = "Processed by server"

            # Serialize the JSON response to a string
            response_data = json.dumps(json_data)

            # Send the JSON data back to the client
            await websocket.send_text(response_data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        active_websockets.remove(websocket)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI modular app!"}
