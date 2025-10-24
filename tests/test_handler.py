import base64
from PIL import Image, ImageDraw, ImageFont
import io
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# Import your handler
from src.handler import handler, load_models  # Assuming your file is named handler.py


def test_warmup():
    """Test the warmup action"""

    job = {
        "input": {
            "action": "warmup",
            "api_key": "temp-dev-key-12345",  # Use one of your valid API keys
        }
    }

    result = handler(job)
    print("Warmup result:", result)


def create_test_ui_image():
    """Create a simple UI mockup with buttons and text"""

    # Create white background
    img = Image.new("RGB", (800, 600), color="white")
    draw = ImageDraw.Draw(img)

    # Try to use a default font, fallback to basic if not available
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except Exception:
        font = ImageFont.load_default()

    # Draw 3 boxes with text
    # Box 1: Button at top
    draw.rectangle([100, 100, 300, 150], outline="black", width=2, fill="lightblue")
    draw.text((150, 115), "Click Me", fill="black", font=font)

    # Box 2: Button in middle
    draw.rectangle([100, 250, 300, 300], outline="black", width=2, fill="lightgreen")
    draw.text((150, 265), "Submit", fill="black", font=font)

    # Box 3: Text box at bottom
    draw.rectangle([100, 400, 500, 450], outline="black", width=2, fill="lightyellow")
    draw.text((150, 415), "Enter your name here", fill="gray", font=font)

    return img


def test_parse_with_image():
    """Test the parse action with a real image"""

    # Create the test image
    test_img = create_test_ui_image()

    # Save it so you can see what we created (optional)
    test_img.save("test_ui_image.png")
    print("📸 Test image saved as test_ui_image.png")

    # Convert to base64
    buffered = io.BytesIO()
    test_img.save(buffered, format="PNG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    job = {
        "input": {
            "action": "parse",
            "api_key": "temp-dev-key-12345",
            "image": image_base64,
        }
    }

    print("🔍 Parsing image...")
    result = handler(job)
    print("✅ Parse result:", result)


if __name__ == "__main__":
    print("🧪 Loading models...")
    load_models()

    print("\n--- Test 1: Warmup ---")
    test_warmup()

    print("\n--- Test 2: Parse ---")
    test_parse_with_image()
