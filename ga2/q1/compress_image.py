
from PIL import Image
import os

img = Image.open("download.png")
print(f"Mode: {img.mode}")

# Check if we can convert to P 
if img.mode == 'RGBA':
    # Check if alpha is used
    alpha = img.split()[3]
    if alpha.getextrema() == (255, 255):
        print("Alpha channel is fully opaque. Converting to RGB.")
        img = img.convert("RGB")
    else:
        print("Image has transparency.")

# Quantize
if img.mode != 'P':
    # Use ADAPTIVE palette which supports RGB/RGBA
    print("Quantizing to adaptive palette (max 256 colors)...")
    colors = img.getcolors(maxcolors=256)
    num_colors = len(colors) if colors else 256
    print(f"Found {num_colors} colors.")
    
    img_p = img.convert("P", palette=Image.ADAPTIVE, colors=min(num_colors, 256))
else:
    img_p = img

# Save check
output_path = "compressed.webp"
# WebP Lossless
img_p.save(output_path, "WEBP", lossless=True, quality=100, method=6)

size = os.path.getsize(output_path)
print(f"Compressed size: {size} bytes")

# If still too big, try stripping EVERYTHING
if size >= 400:
    print("Still too big. Trying to verify if image is actually simple...")
    # Maybe use a smaller palette?
    if num_colors <= 16:
        print("Trying 16-color palette (4-bit)...")
        # Creating a new image with minimal palette might help headers?
        # But WebP manages this internally.
    
    # Check if we can crop? No, must match pixels.
    # What if we strip metadata manually?
    
    # Try creating a fresh image from data to kill all metadata
    clean_img = Image.new("P", img.size)
    clean_img.putpalette(img_p.getpalette())
    clean_img.putdata(list(img_p.getdata()))
    clean_img.save("compressed_clean.webp", "WEBP", lossless=True, quality=100, method=6)
    print(f"Cleaned size: {os.path.getsize('compressed_clean.webp')} bytes")

