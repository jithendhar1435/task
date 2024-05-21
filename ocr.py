import pdfplumber
import re

def read_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text

def format_text(text):
    # Splitting the text into lines
    lines = text.split('\n')
    
    # Initialize formatted text variable
    formatted_text = ''
    
    # Define regex patterns for different sections
    section_patterns = {
        'patient_particulars': r'SECTION 1: PATIENT’S PARTICULARS',
        'doctor_particulars': r'SECTION 2: DOCTOR’S PARTICULARS',
        'patient_medical_info': r'SECTION 3: PATIENT’S MEDICAL INFORMATION',
        'mental_capacity_opinion': r'SECTION 4: OPINION ON PATIENT’S MENTAL CAPACITY',
        'declaration': r'SECTION 5: DECLARATION'
    }
    
    current_section = None

    # Define a function to format each line with bullets and indentation
    def format_line(line, bullet='- ', indent=0):
        return ' ' * indent + bullet + line.strip() + '\n'
    
    for line in lines:
        # Check for section headers
        for section, pattern in section_patterns.items():
            if re.search(pattern, line, re.IGNORECASE):
                current_section = section
                formatted_text += f'\n{line}\n' + '-' * len(line) + '\n'
                break
        else:
            # Format the content based on the current section
            if current_section:
                if line.strip():  # Ignore empty lines
                    if current_section == 'patient_medical_info':
                        formatted_text += format_line(line, bullet='- ', indent=2)
                    elif current_section == 'mental_capacity_opinion':
                        formatted_text += format_line(line, bullet='- ', indent=2)
                    elif current_section == 'declaration':
                        formatted_text += format_line(line, bullet='- ', indent=2)
                    else:
                        formatted_text += format_line(line)
            else:
                formatted_text += line + '\n'
    
    return formatted_text


