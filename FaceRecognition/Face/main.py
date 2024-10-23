# try:
#     image1 = face_recognition.load_image_file("namf2tech.png")
#     image1_encoding = face_recognition.face_encodings(image1)[0]
#     connection = pyodbc.connect(connectionString)
#     cursor = connection.cursor()
#
#     # Kiểm tra kết nối: Thực hiện một câu lệnh đơn giản
#     cursor.execute("SELECT @@version;")
#     row = cursor.fetchone()
#     print("Kết nối thành công! Phiên bản SQL Server:", row[0])
#
#     cursor.execute("SELECT IMAGE_NAME FROM Users")
#     imagesFromDatabase = [row[0] for row in cursor.fetchall()]
#     print(imagesFromDatabase)
#     index = 0
#     for image in imagesFromDatabase:
#         print(image)
#         image2 = face_recognition.load_image_file("kietf2tech.png")
#         image2_encoding = face_recognition.face_encodings(image2)[0]
#
#         results = face_recognition.compare_faces([image1_encoding], image2_encoding)
#
#
#         if results[index]:
#             # cursor.execute(f"SELECT * FROM Users where IMAGE_NAME = '{image}'")
#             # user = cursor.fetchone()
#             print(results)
#         else:
#             print("Không tìm thấy")
#     # Đóng kết nối sau khi sử dụng
#     cursor.close()
#     connection.close()
#
# except Exception as e:
#     print("Lỗi kết nối:", e)





# # Load the first image and get the face encodings
# image1 = face_recognition.load_image_file("namf2tech.png")
# image1_encoding = face_recognition.face_encodings(image1)[0]
#
# # Load the second image and get the face encodings
# image2 = face_recognition.load_image_file("kietf2tech.png")
# image2_encoding = face_recognition.face_encodings(image2)[0]
#
# # Thiết lập ngưỡng để so sánh
#
# # Compare the two faces
# results = face_recognition.compare_faces([image1_encoding], image2_encoding)
#
# if results[0]:
#     print("Matched")
# else:
#     print("Not Matched")



# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile = File(...)):
#     image_temp = await file.read()
#     image_temp_open = Image.open(BytesIO(image_temp))
#
#     image_np = np.array(image_temp_open)
#     # image2 = face_recognition.load_image_file("Messi_Compare.png")
#     # image2_encoding = face_recognition.face_encodings(image2)[0]
#
#     try:
#
#         # image1 = face_recognition.load_image_file(image_np)
#         image1_encoding = face_recognition.face_encodings(image_np)
#         connection = pyodbc.connect(connectionString)
#         cursor = connection.cursor()
#
#         # Kiểm tra kết nối: Thực hiện một câu lệnh đơn giản
#         cursor.execute("SELECT @@version;")
#         row = cursor.fetchone()
#         print("Kết nối thành công! Phiên bản SQL Server:", row[0])
#
#         cursor.execute("SELECT IMAGE_NAME FROM Users")
#         imagesFromDatabase = [row[0] for row in cursor.fetchall()]
#         print(imagesFromDatabase)
#         for image in imagesFromDatabase:
#             print(image)
#             image2 = face_recognition.load_image_file(str(image))
#             image2_encoding = face_recognition.face_encodings(image2)[0]
#             results = face_recognition.compare_faces([image1_encoding], image2_encoding)
#             if results[0]:
#                 cursor.execute(f"SELECT * FROM Users where IMAGE_NAME = '{image}'")
#                 user = cursor.fetchone()
#                 if user:
#                     # Lấy tên cột từ cursor.description
#                     columns = [column[0] for column in cursor.description]
#
#                     # Chuyển đổi user (tuple) thành dictionary
#                     user_dict = dict(zip(columns, user))
#                     print(user_dict)
#                     # Trả về thông tin người dùng dưới dạng JSON
#                     return {"ID": user_dict["ID"], "LASTNAME": user_dict["LASTNAME"], "FIRSTNAME": user_dict["FIRSTNAME"]}
#                 else:
#                     return {"Error": "Không tìm thấy người dùng"}
#                 # return {"username" : user}
#             else:
#                 print("Không tìm thấy")
#         # Đóng kết nối sau khi sử dụng
#         cursor.close()
#         connection.close()
#
#     except Exception as e:
#         print("Lỗi kết nối:", e)

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
#                 # So sánh hai khuôn mặt
#                 results = face_recognition.compare_faces([image1_encoding], image2_encoding)
#                 print(results)
#                 if results[0]:
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
#                     print(f"Không tìm thấy khuôn mặt khớp với ảnh {image}")
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


import face_recognition
from fastapi import FastAPI, File, UploadFile
import pyodbc
from PIL import Image
import numpy as np
from io import BytesIO
from starlette.middleware.cors import CORSMiddleware
import cv2

app = FastAPI()
SERVER = "localhost\\SQLEXPRESS"
DATABASE = 'EventDatabase'
USERNAME = 'sa'
PASSWORD = '123'

connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def enhance_image(image_np):
    """Cải thiện chất lượng ảnh trước khi nhận diện"""
    # Chuyển sang ảnh xám
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

    # Cân bằng histogram
    equalized = cv2.equalizeHist(gray)

    # Áp dụng Gaussian blur để giảm nhiễu
    blurred = cv2.GaussianBlur(equalized, (5, 5), 0)

    # Chuyển lại về RGB
    enhanced = cv2.cvtColor(blurred, cv2.COLOR_GRAY2RGB)
    return enhanced


def get_face_encoding(image_np, retry_count=3):
    """Lấy face encoding với nhiều lần thử và các phương pháp khác nhau"""
    for i in range(retry_count):
        # Thử với các tham số khác nhau
        face_locations = face_recognition.face_locations(
            image_np,
            number_of_times_to_upsample=i + 1,
            model="cnn" if i == retry_count - 1 else "hog"
        )

        if face_locations:
            return face_recognition.face_encodings(image_np, face_locations)

    # Thử với ảnh đã được cải thiện
    enhanced_image = enhance_image(image_np)
    face_locations = face_recognition.face_locations(
        enhanced_image,
        number_of_times_to_upsample=2
    )

    if face_locations:
        return face_recognition.face_encodings(enhanced_image, face_locations)

    return []


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        # Đọc và xử lý ảnh
        image_data = await file.read()
        image = Image.open(BytesIO(image_data))
        image_np = np.array(image)

        # Lấy face encoding với nhiều lần thử
        face_encodings1 = get_face_encoding(image_np)

        if len(face_encodings1) == 0:
            return {
                "Error": "Không tìm thấy khuôn mặt trong ảnh tải lên",
                "Suggestion": "Vui lòng thử lại với ảnh rõ nét hơn và đảm bảo khuôn mặt nhìn thẳng vào camera"
            }

        image1_encoding = face_encodings1[0]

        # Kết nối database với xử lý lỗi tốt hơn
        try:
            connection = pyodbc.connect(connectionString)
            cursor = connection.cursor()
        except pyodbc.Error as e:
            return {"Error": f"Lỗi kết nối database: {str(e)}"}

        # Thiết lập các ngưỡng so sánh
        thresholds = [0.4, 0.45, 0.5]  # Thử với nhiều ngưỡng khác nhau

        try:
            cursor.execute("SELECT IMAGE_NAME, ID, LASTNAME, FIRSTNAME FROM Users")
            users_data = cursor.fetchall()

            for threshold in thresholds:
                for user_data in users_data:
                    image_path, user_id, lastname, firstname = user_data

                    try:
                        # Load và xử lý ảnh từ database
                        image2 = face_recognition.load_image_file(str(image_path))
                        face_encodings2 = get_face_encoding(image2)

                        if face_encodings2:
                            image2_encoding = face_encodings2[0]

                            # Tính khoảng cách và so sánh
                            face_distance = face_recognition.face_distance(
                                [image1_encoding],
                                image2_encoding
                            )[0]

                            if face_distance <= threshold:
                                return {
                                    "ID": user_id,
                                    "LASTNAME": lastname,
                                    "FIRSTNAME": firstname,
                                    "Confidence": f"{(1 - face_distance) * 100:.2f}%"
                                }
                    except Exception as e:
                        print(f"Lỗi khi xử lý ảnh {image_path}: {str(e)}")
                        continue

        finally:
            cursor.close()
            connection.close()

        return {
            "Error": "Không tìm thấy người dùng phù hợp",
            "Suggestion": "Vui lòng đảm bảo người dùng đã được đăng ký trong hệ thống"
        }

    except Exception as e:
        return {
            "Error": f"Lỗi hệ thống: {str(e)}",
            "Suggestion": "Vui lòng thử lại sau hoặc liên hệ admin"
        }