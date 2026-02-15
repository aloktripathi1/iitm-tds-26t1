# Q1 Solution: Image Compression

## Objective
Compress `q-image-compression-dynamic.webp` losslessly to less than 400 bytes.

## Steps Taken

1.  **Analysis**:
    -   Downloaded the original image (`original.png`, ~29KB).
    -   Found it uses only a few unique colors (< 256).

2.  **Compression Strategy**:
    -   Converted the image to an 8-bit palette (`P` mode) using `Pillow`.
    -   Saved the image using WebP Lossless format with maximum compression (`method=6`).
    -   The conversion to a palette drastically reduced the file size because the image content was simple, even though the original file header was large.

3.  **Result**:
    -   Final file: `compressed.webp`
    -   Size: **266 bytes**
    -   Lossless: Yes (Verified pixel equality).

## Usage
Run the script to reproduce:
```bash
python compress_image.py
```

