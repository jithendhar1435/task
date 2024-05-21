VITAVISUALS - Health Care Chatbot with OCR Functionality


Overview:

VITAVISUALS is a health care chatbot designed to assist users in diagnosing symptoms and providing health-related advice. The chatbot also includes functionality to extract and process text from PDF documents using Optical Character Recognition (OCR) technology. This project leverages machine learning techniques to analyze symptoms and provides a user-friendly interface for interaction.

Project Structure
The project is organized into the following files and directories:


VITAVISUALS/
│
├── app.py               # Main Flask application
├── ocr.py               # OCR functionality for reading PDF files
├── chatbot.py           # Chatbot logic and symptom processing
├── templates/
│   └── index.html       # HTML file for the web interface
├── static/
│   └── css/
│       └── styles.css   # CSS styles for the web interface
├── uploads/             # Directory to store uploaded files
├── README.md            # Project documentation
└── requirements.txt     # Required packages for the project


Required Packages
The project requires the following packages:

Flask
PyMuPDF
Scikit-learn
Pandas
Numpy
Werkzeug
seaborn
You can install these packages using the requirements.txt file with the following command:

Code:
pip install -r requirements.txt


Procedure to Execute the Project
1. Clone the Repository
First, clone the repository to your local machine:

Code
git clone https://github.com/Vamsi-Agnihotram-18/VITAVISUALS.git

cd VITAVISUALS
2. Set Up a Virtual Environment
 You can set up a virtual environment using venv:

Code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Required Packages
Install the required packages using the requirements.txt file:

Code:
pip install -r requirements.txt
4. Prepare the uploads Directory
Ensure the uploads directory exists to store the uploaded files:

Code:
mkdir uploads
5. Run the Flask Application
Run the Flask application using the following command:

Code:
python app.py
The application will start, and you can access it at http://127.0.0.1:5000.

6. Use the Application
Chatbot Functionality
Open your web browser and go to http://127.0.0.1:5000.

Enter your symptoms in the chatbot interface.
The chatbot will process your symptoms and provide advice based on the machine learning model.
OCR Functionality
Use the file upload form to upload a PDF document.
The application will extract text from the PDF and display it on the web page.

Detailed Explanation of Files

app.py
The main Flask application. It handles the routing, file uploads, and integrates the chatbot and OCR functionalities.

ocr.py
Contains the read_pdf function which uses PyMuPDF to extract text from PDF documents.

code:
import fitz  # PyMuPDF

def read_pdf(file_path):
    """
    Reads a PDF file and extracts text from it.

    Parameters:
    file_path (str): Path to the PDF file.

    Returns:
    str: Extracted text from the PDF.
    """
    try:
        doc = fitz.open(file_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return ""

chatbot.py
Contains the logic for processing symptoms and interacting with the machine learning model.

templates/index.html
The HTML file for the web interface. It includes the chatbot interface and the file upload form.

static/css/styles.css
Contains the CSS styles for the web interface.

uploads/
Directory to store uploaded PDF files.

requirements.txt
Lists the required packages for the project.

Conclusion
VITAVISUALS is a comprehensive health care chatbot that not only assists users in diagnosing symptoms but also includes OCR functionality to process PDF documents.

