"""
The first of hopefully a couple approaches to identifying four points on a map.

This simply finds text on the map that it will use to look up.
"""

from PIL import Image
import pytesseract
from pathlib import Path

# NOTE: Avoid doing any sort of preprocessing to the image to make it
# "easier" to read. It seems that the straight ocr calls do the best job.

# General scan with no position data
def scan(file: Path) -> str:
    img = Image.open(file)
    text = pytesseract.image_to_string(img)
    return text

if __name__ == "__main__":
    print(scan(Path("data/test/tunnels.png")))