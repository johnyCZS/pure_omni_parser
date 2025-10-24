import time
import runpod
from src.auth.validator import validate_api_key
from src.exceptions import InvalidImageError
from util.omniparser import Omniparser


def handler(job):
    """
    Single handler with multiple actions:
    - warmup: Keep container alive, no processing
    - parse: Full image parsing with OmniParser

    All actions require API key authentication.
    """
    try:
        job_input = job["input"]
        action = job_input.get("action", "parse")

        validate_api_key(job_input.get("api_key", ""))

        if action == "warmup":
            return warmup()

        elif action == "parse":
            image_data = job_input.get("image", "")

            if not image_data:
                raise InvalidImageError("Image data is required")
            return parse_image(image_data)

        else:
            return {"error": f"Unknown action:{action}"}
    except Exception as e:
        return {"error": str(e)}


def load_models():
    """ "Load necessary models for OmniParser"""
    global omniparser_instance

    print("⏱️  Starting model loading...")
    start_total = time.time()

    config = {
        "som_model_path": "weights/icon_detect/model.pt",
        "caption_model_name": "florence2",
        "caption_model_path": "weights/icon_caption_florence",
        "BOX_TRESHOLD": 0.05,  # Detection confidence threshold
    }

    start_omni = time.time()
    omniparser_instance = Omniparser(config)
    end_omni = time.time()

    end_total = time.time()

    print("Models loaded successfully!")
    print(f"⏱️  Omniparser init: {end_omni - start_omni:.2f}s")
    print(f"⏱️  Total load time: {end_total - start_total:.2f}s")


def warmup():
    """
    Lightweight warmup to keep container alive.
    No heavy processing, just confirms models are loaded.
    """

    return {"status": "warm", "models_loaded": True, "message": "Container is ready"}


def parse_image(image_data: str):
    """Parse image after validating API key and image data"""
    global omniparser_instance

    try:
        labeled_image, parsed_content_list = omniparser_instance.parse(image_data)

        print(parsed_content_list)
        print("Type:", type(parsed_content_list))
        print("Length:", len(parsed_content_list))
        return {"success": True, "parsed_content": parsed_content_list}

    except Exception as e:
        import traceback

        print("Error during parsing:", str(e))
        traceback.print_exc()
        raise InvalidImageError("Invalid base64 image data", {str(e)})


if __name__ == "__main__":
    load_models()
    runpod.serverless.start({"handler": handler})
