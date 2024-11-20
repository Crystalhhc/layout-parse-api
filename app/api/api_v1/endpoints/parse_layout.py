from fastapi import APIRouter, UploadFile, File
import cv2
import numpy as np
#import layoutparser as lp
import sys

def initialize_model():
    print("Python version:", sys.version)
    #print("LayoutParser version:", lp.__version__)
    print("Attempting to initialize Detectron2LayoutModel...")
    """
    try:
        #model = lp.models.Detectron2LayoutModel(
            'lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
            extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.8],
            label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"}
        )
        print("Model initialized successfully")
        return model
    except Exception as e:
        print("Error initializing model:", str(e))
        raise
    """
# Initialize the model at module level
model = initialize_model()
router = APIRouter()

@router.post("/parse-layout")
async def parse_layout(file: UploadFile = File(...)):
    # Read the uploaded file
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert the image from BGR (cv2 default) to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect the layout
    layout = model.detect(image)

    # Convert layout to a serializable format
    serializable_layout = [
        {
            "label": block.type,
            "score": float(block.score),  # Convert to float for JSON serialization
            "x1": int(block.block.x_1),
            "y1": int(block.block.y_1),
            "x2": int(block.block.x_2),
            "y2": int(block.block.y_2)
        } for block in layout
    ]

    # Return the parsed layout information
    return {"layout": serializable_layout}