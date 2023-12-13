import os
import io
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from PIL import Image
import matplotlib.pyplot as plt
from bson import ObjectId

current_time = datetime.now().strftime("%H:%M:%S")

# Create a new client and connect to the server
uri = "mongodb+srv://nguyenlinhanhkhoa3:zTT1NGJzkyoL5VGH@cluster0.to3lvrc.mongodb.net/"
client = MongoClient(uri, server_api=ServerApi('1'))

# Connect to the database
mydb = client["CHAMCONG"]
mycol1 = mydb["HinhAnhNhanVien"]
mycol2 = mydb["HinhAnhNhanVienDaChamCong"]
mycol3 = mydb["HinhAnhNhanVienChuaChamCong"]
mycol4 = mydb["ThongTinNhanVien"]

# #insert image
# def insert_image():
#     # Open the image file
#     im = Image.open("Dataprocess/6.jpg")

#     # Convert the image to a bytearray
#     image_bytes = io.BytesIO()
#     im.save(image_bytes, format='JPEG')

#     # Prepare data for MongoDB
#     image_data = {
#         'id_Nhanvien': 1,  # Replace 'your_specific_id' with your desired ID
#         'ten_Nhanvien': 'Le Hoang Thinh',  # Replace 'your_specific_name' with your desired name
#         'gioitinh': 'Nam',
#         'ngaysinh': '2000-01-01',
#         'diachi':   'Quang Nam',
#         'sodienthoai':  '0123456789',
#         'vitri':    'Fresher',
#         'data': image_bytes.getvalue(),
#         'timestamp': datetime.now(),
#         'tongsogiocong': 0,
#         'tienluong': 0
#     }

#     # Insert the image data into the collection
#     mycol1.insert_one(image_data)
#     print('Image inserted successfully.')

def display_image_by_id(collection, employee_id):
    images = mycol1  # Change to your desired collection
    image = images.find_one()
    image = collection.find_one({'id_Nhanvien': employee_id})
    if image is not None:
        pil_img = Image.open(io.BytesIO(image['data']))
        plt.imshow(pil_img)
        plt.show()
    else:
        print(f"No image found with ID {employee_id}.")

# Display an image by its ID (change 'your_image_id' to the desired ID)
display_image_by_id(mycol1, 1)  # Change the ID to the desired image ID

#update tống số giờ công
def update_tongsogiocong(employee_id):
    
    # Input the gio_vao (entry time) from the user
    gio_vao = datetime.now().strftime("%H:%M:%S")

    # Split the input string to get hour part
    gio_vao_hour = int(gio_vao.split(':')[0])

    # Calculate additional working hours if entry time is before 8:00 AM
    additional_hours = 8 if gio_vao_hour < 9 else 0

    # Get the existing tongsogiocong for the employee
    existing_tongsogiocong = mycol1.find_one({'id_Nhanvien': employee_id})['tongsogiocong']

    # Update tongsogiocong field for the specified employee ID with additional hours
    updated_tongsogiocong = existing_tongsogiocong + additional_hours

    # Update the 'tongsogiocong' field for the specified employee ID
    mycol1.update_one({'id_Nhanvien': employee_id}, {'$set': {'tongsogiocong': updated_tongsogiocong}})
    print('Tong so gio cong updated successfully.')

update_tongsogiocong(employee_id=1)

def update_tienluong(employee_id):
    # Get the existing tongsogiocong for the employee
    existing_tongsogiocong = mycol1.find_one({'id_Nhanvien': employee_id})['tongsogiocong']
    existing_vitri = mycol1.find_one({'id_Nhanvien': employee_id})['vitri']
    tienluong_per_hour = 0 

    if existing_vitri == 'Fresher':
        tienluong_per_hour = 25000
    elif existing_vitri == 'Senior':
        tienluong_per_hour = 30000
    elif existing_vitri == 'Junior':
        tienluong_per_hour = 40000

    # Calculate the salary for the employee
    salary = existing_tongsogiocong * tienluong_per_hour

    # Update the 'tienluong' field for the specified employee ID
    mycol1.update_one({'id_Nhanvien': employee_id}, {'$set': {'tienluong': salary}})
    print('Tien luong updated successfully.')
# #main

update_tienluong(employee_id=1)

