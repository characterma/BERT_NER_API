from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.api.routers import router
from src.base.configs import get_conf
from src.base.exceptions import add_exception_handler
from src.base.logger import LoggingRoute
from src.base.router import FastAPI


app_conf = get_conf("APP")

app = FastAPI(
    title="Named Entity Recognition API for BOCHK", 
    description="This is an NER API for BOCHK project. Target entities include Company and Person."
)
app.router.route_class = LoggingRoute
app.include_router(router.router)
add_exception_handler(app)

# Health check =====
# If alived, return status code 200 and message "I'm"


@app.get("/healthz")
async def health_check():
    """Check the server is alived."""
    return JSONResponse(status_code=200, content={"status": "OK"})


# Test example =====
@app.post("/test")
def post_(json_dict: dict):
    """Test endpoint for loadtest."""
    resp = JSONResponse(content=json_dict, media_type="application/json", status_code=200)
    return resp


if __name__ == "__main__":
    import asyncio

    import uvloop
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = ["0.0.0.0:8080"]

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(serve(app, config))
