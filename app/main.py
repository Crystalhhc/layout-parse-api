from fastapi import FastAPI
from app.api.api_v1.api import router as api_router
from PIL import Image
#from mangum import Mangum

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(api_router, prefix="/api/v1")
#handler = Mangum(app)

#image = Image.open("data/paper-image.jpg")
#image = image[..., ::-1]
