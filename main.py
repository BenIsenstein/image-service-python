from flask import Flask, request
import pdfkit
import os
import io
from dotenv import load_dotenv
from google.cloud import storage

load_dotenv()

with open('credentials.json', 'w') as file:
    file.write(os.environ['ARTICLES_SERVICE_ACCOUNT_CREDENTIALS'])

app = Flask(__name__)
storage_client = storage.Client.from_service_account_json('credentials.json')
bucket = storage_client.bucket(os.environ['ARTICLES_BUCKET_NAME'])

@app.route('/health', methods=['GET'])
def confirm_health_check():
    return 'All healthy!', 200

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        body = request.get_json()
        html = body.get('html')
        file_path = body.get('filePath')
        pdf_bytes = pdfkit.from_string(html)
        pdf_file = bucket.blob(f'{file_path}.pdf')
        html_file = bucket.blob(f'{file_path}.html')
        do_files_exist = False

        try:
            do_files_exist = pdf_file.exists() and html_file.exists()
        except Exception as e:
            do_files_exist = False
        
        if do_files_exist:
            raise Exception('pdf and html files for this email already exist')
        
        pdf_file.upload_from_file(io.BytesIO(pdf_bytes))
        html_file.upload_from_string(html)

        return {
            "pdfUrl": pdf_file.public_url,
            "htmlUrl": html_file.public_url
        }
    except Exception as e:
        return f'An error occurred: {e}', 500

if __name__ == '__main__':
    app.run(debug=True)
