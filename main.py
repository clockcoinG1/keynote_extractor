import zipfile
import os
import xml.etree.ElementTree as ET
from PIL import Image
import io
import csv

# File path
file_path = '/mnt/data/Chem 6 Unit 3 (2) 2.key'

# Function to extract and analyze the content of a Keynote file
def analyze_keynote(file_path):
    # Check if the file is a valid zipfile (Keynote files are essentially zip files)
    if not zipfile.is_zipfile(file_path):
        return "The file does not appear to be a valid Keynote (zip) file."
    
    extracted_data = {
        'metadata': [],
        'comments': [],
        'slide_content': [],
        'diagrams': []
    }

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        # Extracting the zipfile contents to a temporary directory
        temp_dir = '/mnt/data/temp_keynote_extraction'
        zip_ref.extractall(temp_dir)

        # Parse metadata
        metadata_file = os.path.join(temp_dir, 'docProps/app.xml')
        if os.path.exists(metadata_file):
            tree = ET.parse(metadata_file)
            root = tree.getroot()
            for child in root:
                extracted_data['metadata'].append((child.tag, child.text))

        # Parse comments (this is not straightforward in Keynote files and may not be accurate)
        # ...

        # Parse slide content and diagrams
        slides_dir = os.path.join(temp_dir, 'slides')
        if os.path.exists(slides_dir):
            for slide_file in os.listdir(slides_dir):
                slide_path = os.path.join(slides_dir, slide_file)
                if slide_file.endswith('.xml'):
                    # Parsing slide content
                    tree = ET.parse(slide_path)
                    root = tree.getroot()
                    slide_text = []
                    for elem in tree.iter():
                        if 'text' in elem.tag.lower():
                            slide_text.append(elem.text)
                    extracted_data['slide_content'].append(' '.join(slide_text))

                elif slide_file.endswith(('.png', '.jpg', '.jpeg')):
                    # Extracting diagram images
                    with open(slide_path, 'rb') as img_file:
                        img_data = img_file.read()
                        extracted_data['diagrams'].append(img_data)

    # Cleanup temporary extraction directory
    os.rmdir(temp_dir)

    return extracted_data

# Extract and analyze the Keynote file
keynote_data = analyze_keynote(file_path)
keynote_data
