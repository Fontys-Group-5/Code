from flask import Flask, render_template, request, redirect, url_for
import boto3
from botocore.exceptions import NoCredentialsError
import os

app = Flask(__name__)

# AWS S3 Configuration
S3_BUCKET = 'himartest'

S3_REGION = 'eu-central-1'

s3_client = boto3.client('s3',
                         aws_access_key_id=S3_ACCESS_KEY,
                         aws_secret_access_key=S3_SECRET_KEY,
                         region_name=S3_REGION)


@app.route('/file_upload')
def upload():
    return render_template('upload.html')


@app.route('/file_upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file selected."
    
    file = request.files['file']

    if file.filename == '':
        return "No file selected."

    if file:
        try:
            s3_client.upload_fileobj(file, S3_BUCKET, file.filename)
            return f"File {file.filename} uploaded successfully to S3."
        except NoCredentialsError:
            return "AWS credentials are not available."
        except Exception as e:
            return f"Error uploading file to S3 bucket: {str(e)}"

@app.route('/download/<filename>')
def download_file(filename):
    try:
        # Generate a pre-signed URL for downloading
        url = s3_client.generate_presigned_url('get_object',
                                                Params={'Bucket': S3_BUCKET, 'Key': filename},
                                                ExpiresIn=3600)  # Link expires in 1 hour
        return redirect(url)
    except Exception as e:
        return f"Error generating download link: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
