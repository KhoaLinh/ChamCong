from flask import Flask, render_template, request
from pymongo import MongoClient
from bson.binary import Binary
from PIL import Image
import io
import base64
from datetime import datetime
import os

app = Flask(__name__)

# Connect to MongoDB
uri = "mongodb+srv://nguyenlinhanhkhoa3:zTT1NGJzkyoL5VGH@cluster0.to3lvrc.mongodb.net/"
client = MongoClient(uri)
mydb = client["CHAMCONG"]
mycol1 = mydb["HinhAnhNhanVien"]
mycol2 = mydb["HinhAnhNhanVienMoi"]

# Route to serve HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch and display images
@app.route('/api/image/<employee_id>')
def display_image(employee_id):
    image_data = mycol1.find_one({'id_Nhanvien': int(employee_id)})
    
    if image_data is not None:
        timestamp_str = image_data['timestamp']
        formatted_timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%f")
        formatted_timestamp_str = formatted_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        image_binary = image_data['data']
        img = Image.open(io.BytesIO(image_binary))
        img_io = io.BytesIO()
        img.save(img_io, 'JPEG')
        img_io.seek(0)
        
        # Convert image to base64
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

        # Prepare additional info
        additional_info = {
            'id_Nhanvien': image_data['id_Nhanvien'],
            'ten_Nhanvien': image_data['ten_Nhanvien'],
            'timestamp': formatted_timestamp_str,  # Use formatted_timestamp_str here
            'tongsogiocong': image_data['tongsogiocong'],
            'tienluong': image_data['tienluong']
        }
        
        return render_template('image.html', img_data=img_base64, info=additional_info, formatted_timestamp=formatted_timestamp_str)
    else:
        return 'Information not found'
    
# Route to add new employee information
@app.route('/add/employee', methods=['POST'])
def insert_new_employee():
    employee_data = request.form  # Get form data
    image_file = request.files['image']  # Get uploaded file
    image_video = request.files['video']  # Get uploaded file

    # Extract employee information from JSON data
    new_employee_id = employee_data['id']
    new_employee_name = employee_data['name']
    new_employee_gender = employee_data['gender']
    new_employee_dob = employee_data['dob']
    new_employee_address = employee_data['address']
    new_employee_phone = employee_data['phone']
    new_employee_position = employee_data['position']

        # Create a dictionary for employee information
    employee_info = {
        'id_Nhanvien': int(new_employee_id),
        'ten_Nhanvien': new_employee_name,
        'gioitinh': new_employee_gender,
        'ngaysinh': new_employee_dob,
        'diachi': new_employee_address,
        'sodienthoai': new_employee_phone,
        'vitri': new_employee_position,
        'timestamp': datetime.now(),
        'tongsogiocong': 0,
        'tienluong': 0,
        'data': Binary(image_file.read()),
        'video': Binary(image_video.read())
    }

    mycol2.insert_one(employee_info)  # Insert employee information to the database
    mycol1.insert_one(employee_info)  # Insert employee information to the database
        
    return 'New employee added successfully'
    
if __name__ == '__main__':
    app.run(debug=True)
