import fitz  # PyMuPDF
from PIL import Image

def convert_pdf_to_png(pdf_file, output_folder, target_width=1280, target_height=720):
    # Open the PDF file
    pdf_document = fitz.open(pdf_file)

    # Iterate through pages and convert to PNG
    for page_number in range(pdf_document.page_count):
        # Get the page
        page = pdf_document[page_number]

        # Convert the page to an image
        image = page.get_pixmap()

        # Resize the image to the specified dimensions
        resized_image = Image.frombytes("RGB", [image.width, image.height], image.samples)
        resized_image = resized_image.resize((target_width, target_height))

        # Save the resized image
        image_path = f"{output_folder}/page_{page_number + 1}.png"
        resized_image.save(image_path)

    # Close the PDF document
    pdf_document.close()

    print(f"Conversion completed. PNG images saved to {output_folder}")

# Example usage

