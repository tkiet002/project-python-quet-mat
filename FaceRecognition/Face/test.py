# import os.path

import face_recognition
# from typing import Annotated
from fastapi import FastAPI, File, UploadFile,Request #, Response
import pyodbc
from PIL import Image
import numpy as np
from pydantic import BaseModel
# from io import BytesIO
#from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware


from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import face_recognition
# import numpy as np
# from PIL import Image
# import pyodbc
import base64
from io import BytesIO


app = FastAPI()
SERVER = "localhost\\SQLEXPRESS"
DATABASE = 'EventDatabase'
USERNAME = 'sa'
PASSWORD = '123'

drivers = [driver for driver in pyodbc.drivers()]
print("Các driver ODBC đã cài đặt:")
for driver in drivers:
    print(driver)



connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4200",  # Thêm URL của ứng dụng Angular
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)








# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile = File(...)):
#     try:
#         # Đọc file ảnh từ UploadFile (file.file là một đối tượng file-like)
#         image_data = await file.read()  # Đọc toàn bộ dữ liệu từ file vào bộ nhớ
#         image = Image.open(BytesIO(image_data))  # Mở ảnh từ dữ liệu đọc được bằng PIL
#
#         # Chuyển ảnh từ PIL thành NumPy array để sử dụng với face_recognition
#         image_np = np.array(image)
#
#         # Nhận diện khuôn mặt từ ảnh tải lên
#         face_encodings1 = face_recognition.face_encodings(image_np)
#
#         if len(face_encodings1) == 0:
#             return {"Error": "Không tìm thấy khuôn mặt trong ảnh tải lên"}
#
#         image1_encoding = face_encodings1[0]
#
#         # Kết nối SQL Server
#         connection = pyodbc.connect(connectionString)
#         cursor = connection.cursor()
#
#         # Kiểm tra kết nối
#         cursor.execute("SELECT @@version;")
#         row = cursor.fetchone()
#         print("Kết nối thành công! Phiên bản SQL Server:", row[0])
#
#         # Query danh sách các ảnh từ database
#         cursor.execute("SELECT IMAGE_NAME FROM Users")
#         imagesFromDatabase = [row[0] for row in cursor.fetchall()]
#         print(imagesFromDatabase)
#
#         # Thiết lập ngưỡng để so sánh
#         threshold = 0.4
#
#         # So sánh với từng ảnh trong database
#         for image in imagesFromDatabase:
#             try:
#                 # Load ảnh từ database
#                 image2 = face_recognition.load_image_file(str(image))
#
#                 # Nhận diện khuôn mặt từ ảnh
#                 face_encodings2 = face_recognition.face_encodings(image2)
#
#                 if len(face_encodings2) == 0:
#                     print(f"Không tìm thấy khuôn mặt trong ảnh {image}")
#                     continue  # Bỏ qua ảnh này nếu không tìm thấy khuôn mặt
#
#                 image2_encoding = face_encodings2[0]
#
#                 # Tính khoảng cách giữa hai khuôn mặt
#                 face_distance = face_recognition.face_distance([image1_encoding], image2_encoding)[0]
#
#                 # So sánh khoảng cách với ngưỡng
#                 if face_distance <= threshold:
#                     cursor.execute(f"SELECT * FROM Users WHERE IMAGE_NAME = '{image}'")
#                     user = cursor.fetchone()
#                     if user:
#                         # Lấy tên cột từ cursor.description
#                         columns = [column[0] for column in cursor.description]
#
#                         # Chuyển đổi user (tuple) thành dictionary
#                         user_dict = dict(zip(columns, user))
#                         print(user_dict)
#
#                         # Trả về thông tin người dùng dưới dạng JSON
#                         return {"ID": user_dict["ID"], "LASTNAME": user_dict["LASTNAME"],
#                                 "FIRSTNAME": user_dict["FIRSTNAME"]}
#                     else:
#                         return {"Error": "Không tìm thấy người dùng"}
#                 else:
#                     print(f"Khoảng cách giữa các khuôn mặt là {face_distance:.2f}, không khớp.")
#             except Exception as e:
#                 print(f"Lỗi khi xử lý ảnh {image}: {e}")
#
#         cursor.close()
#         connection.close()
#
#     except Exception as e:
#         print("Lỗi kết nối:", e)
#         return {"Error": "Lỗi kết nối đến cơ sở dữ liệu"}
#
#     return {"Error": "Không tìm thấy người dùng"}






@app.post("/upload-face/")
async def create_upload_file(request: Request):
    try:
        # Nhận dữ liệu JSON từ request body
        body = await request.json()
        image_base64 = body.get("image")

        if not image_base64:
            return {"Error": "Không có ảnh được gửi trong yêu cầu"}

        # Loại bỏ header base64 nếu có (ví dụ: "data:image/png;base64,")
        if "base64," in image_base64:
            image_base64 = image_base64.split("base64,")[1]

        # Giải mã chuỗi base64 về dữ liệu nhị phân
        image_data = base64.b64decode(image_base64)

        # Mở ảnh từ dữ liệu đã giải mã bằng PIL
        image = Image.open(BytesIO(image_data))

        # Chuyển ảnh về định dạng RGB
        image = image.convert("RGB")

        # Chuyển ảnh từ PIL thành NumPy array để sử dụng với face_recognition
        image_np = np.array(image)

        # Nhận diện khuôn mặt từ ảnh tải lên
        face_encodings1 = face_recognition.face_encodings(image_np)

        if len(face_encodings1) == 0:
            return {"Error": "Không tìm thấy khuôn mặt trong ảnh tải lên"}

        image1_encoding = face_encodings1[0]

        # Kết nối SQL Server
        connection = pyodbc.connect(connectionString)
        cursor = connection.cursor()

        # Kiểm tra kết nối
        cursor.execute("SELECT @@version;")
        row = cursor.fetchone()
        print("Kết nối thành công! Phiên bản SQL Server:", row[0])

        # Query danh sách các ảnh từ database
        cursor.execute("SELECT IMAGE_NAME FROM Users")
        imagesFromDatabase = [row[0] for row in cursor.fetchall()]

        # Thiết lập ngưỡng để so sánh
        threshold = 0.4

        # So sánh với từng ảnh trong database
        for image in imagesFromDatabase:
            try:
                # Load ảnh từ database
                image2 = face_recognition.load_image_file(str(image))

                # Nhận diện khuôn mặt từ ảnh
                face_encodings2 = face_recognition.face_encodings(image2)

                if len(face_encodings2) == 0:
                    continue  # Bỏ qua ảnh này nếu không tìm thấy khuôn mặt

                image2_encoding = face_encodings2[0]

                # Tính khoảng cách giữa hai khuôn mặt
                face_distance = face_recognition.face_distance([image1_encoding], image2_encoding)[0]

                # So sánh khoảng cách với ngưỡng
                if face_distance <= threshold:
                    cursor.execute(f"SELECT * FROM Users WHERE IMAGE_NAME = '{image}'")
                    user = cursor.fetchone()
                    if user:
                        columns = [column[0] for column in cursor.description]
                        user_dict = dict(zip(columns, user))
                        return {"ID": user_dict["ID"], "LASTNAME": user_dict["LASTNAME"], "FIRSTNAME": user_dict["FIRSTNAME"]}
                    else:
                        return {"Error": "Không tồn tại User"}

            except Exception as e:
                print(f"Lỗi khi xử lý ảnh {image}: {e}")

        cursor.close()
        connection.close()

    except Exception as e:
        print("Lỗi kết nối:", e)
        return {"Error": "Lỗi kết nối đến cơ sở dữ liệu"}

    return {"Error": "Không tìm thấy người dùng"}