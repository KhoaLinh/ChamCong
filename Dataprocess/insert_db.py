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
mycol2 = mydb["HinhAnhNhanVienMoi"]

# Update checkin time
def update_thoigianchamcong(employee_id):
    gio_vao = datetime.now().isoformat()
    mycol1.update_one({'id_Nhanvien': employee_id}, {'$set': {'timestamp': gio_vao}})
    print('Time checkin updated successfully.')

# Update total working hours
def update_tongsogiocong(employee_id):
    gio_vao = datetime.now().strftime("%H:%M:%S")
    gio_vao_hour = int(gio_vao.split(':')[0])
    additional_hours = 8 if gio_vao_hour < 9 else 0
    existing_tongsogiocong = mycol1.find_one({'id_Nhanvien': employee_id})['tongsogiocong']
    updated_tongsogiocong = existing_tongsogiocong + additional_hours
    mycol1.update_one({'id_Nhanvien': employee_id}, {'$set': {'tongsogiocong': updated_tongsogiocong}})
    print('Total working hours updated successfully.')

# Update salary
def update_tienluong(employee_id):
    existing_tongsogiocong = mycol1.find_one({'id_Nhanvien': employee_id})['tongsogiocong']
    existing_vitri = mycol1.find_one({'id_Nhanvien': employee_id})['vitri']
    tienluong_per_hour = 0

    if existing_vitri == 'Fresher':
        tienluong_per_hour = 25000
    elif existing_vitri == 'Senior':
        tienluong_per_hour = 30000
    elif existing_vitri == 'Junior':
        tienluong_per_hour = 40000

    salary = existing_tongsogiocong * tienluong_per_hour
    mycol1.update_one({'id_Nhanvien': employee_id}, {'$set': {'tienluong': salary}})
    print('Salary updated successfully.')

# Check if name exists in the database
def check_name(employee_name):
    existing_employee = mycol1.find_one({'ten_Nhanvien': employee_name})
    return existing_employee is not None

# Create a dictionary with name as key and id as value
def create_dict(employee_name):
    result = mycol1.find_one({'ten_Nhanvien': employee_name})
    
    if result:
        name_id_dict = {result['ten_Nhanvien']: result['id_Nhanvien']}
        return name_id_dict
    else:
        print("Employee not found in the database.")
        return {}


# Main
name = 'Thong'
arg = ['Nguyen Linh Anh Khoa', 'Phan Duy Thong', 'Le Hoang Thinh', 'Truong Huu Khang', 'Truong Trong Hieu', 'Ha Vinh Kien']

employee_name = None

for item in arg:
    if name in item:
        employee_name = item
        break

if check_name(employee_name):
    name_id_dict = create_dict(employee_name)
    employee_id = list(name_id_dict.values())[0]
    update_tongsogiocong(employee_id)
    update_tienluong(employee_id)
    update_thoigianchamcong(employee_id)
else:
    print(f'Employee with name {employee_name} not found in the database.')
