import fitz  # PyMuPDF
from PIL import Image

def pdf_to_png_and_crop(pdf_path, x_pixels, y_pixels, output_folder, zoom_factor=2):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Iterate through each page
    for page_number in range(len(pdf_document)):
        # Select page
        page = pdf_document.load_page(page_number)
        
        # Set zoom matrix for higher resolution
        matrix = fitz.Matrix(zoom_factor, zoom_factor)
        pix = page.get_pixmap(matrix=matrix)
        
        # Convert to PIL image
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Calculate crop box
        center_x = image.width // 2
        center_y = image.height // 2
        left = center_x - x_pixels
        right = center_x + x_pixels
        top = center_y - y_pixels
        bottom = center_y + y_pixels
        
        # Crop the image
        cropped_image = image.crop((left, top, right, bottom))
        
        # Save the cropped image as PNG
        output_path = f"{output_folder}/page_{page_number + 1}.png"
        cropped_image.save(output_path, format="PNG")

    print(f"PDF has been processed and saved to {output_folder}")

# Example usage:
pdf_path = "poscomp2023.pdf"
output_folder = "out-putpdf"
x_pixels = 512 # Number of pixels to the left and right from the center
y_pixels = 900  # Number of pixels to the top and bottom from the center
zoom_factor = 2  # Adjust this factor to control resolution (1 is original size, 2 is double the size, etc.)

pdf_to_png_and_crop(pdf_path, x_pixels, y_pixels, output_folder, zoom_factor)
