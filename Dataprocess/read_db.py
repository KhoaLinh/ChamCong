from pymongo.mongo_client import MongoClient
from bson.binary import Binary
from PIL import Image
import io
import matplotlib.pyplot as plt

# Create a new client and connect to the server
uri = "mongodb+srv://nguyenlinhanhkhoa3:zTT1NGJzkyoL5VGH@cluster0.to3lvrc.mongodb.net/"
client = MongoClient(uri)

# Connect to the database
mydb = client["CHAMCONG"]
mycol1 = mydb["HinhAnhNhanVien"]
mycol2 = mydb["HinhAnhNhanVienDaChamCong"]
mycol3 = mydb["HinhAnhNhanVienChuaChamCong"]
mycol4 = mydb["ThongTinNhanVien"]

# Retrieve the image data from the collection


# Hiển thị tất cả ảnh trong collection
# images = mycol1.find({})

# for image in images:
#     pil_img = Image.open(io.BytesIO(image['data']))
#     plt.imshow(pil_img)
#     plt.show()

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