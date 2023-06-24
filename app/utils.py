import re
import math
import skimage.metrics as metrics
from skimage.io import imread
from skimage.color import rgb2gray
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from docx import Document


def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        execution_time = math.round(end_time - start_time, 5)
        print(f"Execution time of {func.__name__}: {execution_time} seconds")
        return result
    return wrapper


def extract_link_from_message(text):
    url_pattern = re.compile(r'https?://\S+')

    match = re.search(url_pattern, text)

    if match:
        link = match.group(0)
        return link

    return None

def get_video_id(video_link):
    parsed_url = urlparse(video_link)
    query_params = parse_qs(parsed_url.query)
    video_id = query_params.get('v', [''])[0]
    return video_id

   
def compare_images_ssim(image1_path, image2_path):
    # Load the images
    image1 = imread(image1_path)
    image2 = imread(image2_path)
    
    # Convert the images to grayscale if needed
    if image1.ndim == 3:
        image1 = rgb2gray(image1)
    if image2.ndim == 3:
        image2 = rgb2gray(image2)
    
    # Compute the SSIM value
    ssim_value = metrics.structural_similarity(image1, image2)
    
    return ssim_value

def read_srt_and_write_to_docx(file_path):
    # Create a new Word document
    doc = Document()

    # Read the contents of the .srt file
    with open(file_path, 'r', encoding='utf-8') as srt_file:
        lines = srt_file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line)

    return file_path
    # Process each line of the .srt file
    for line in lines:
        line = line.strip()

        # Skip empty lines and subtitle index lines
        if line and not line.isdigit():
            # Add the subtitle text as a new paragraph in the document
            doc.add_paragraph(line)

    # Save the document to the specified .docx file
    doc.save(file_path)

    return f'{file_path}.docx'

if __name__ == '__main__':
    # compare_images_ssim('1.jpg', '2.jpg')
    read_srt_and_write_to_docx('result/test.srt')
