import fitz  
from PIL import Image

def convert_pdf_to_png(pdf_file, output_folder, target_width=1280, target_height=720):
   
    pdf_document = fitz.open(pdf_file)

 
    for page_number in range(pdf_document.page_count):
        
        page = pdf_document[page_number]

        
        image = page.get_pixmap()

        
        resized_image = Image.frombytes("RGB", [image.width, image.height], image.samples)
        resized_image = resized_image.resize((target_width, target_height))

        
        image_path = f"{output_folder}/page_{page_number + 1}.png"
        resized_image.save(image_path)

    
    pdf_document.close()

    print(f"Conversion completed. PNG images saved to {output_folder}")

