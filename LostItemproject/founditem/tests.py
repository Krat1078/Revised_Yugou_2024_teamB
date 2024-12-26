from django.db import transaction
from django.test import TestCase
from pyzbar.pyzbar import decode
import cv2
import webbrowser
# Create your tests here.
import qrcode
from utils import QR_utils


class QRTestCase(TestCase):

    def test_generate_qr_code_data(self):
        data = QR_utils.generate_qr_code_data(1)
        img = qrcode.make(data=data)
        # 将二维码保存为图片
        # QRコードを画像として保存する
        with open('test.png', 'wb') as f:
            img.save(f)

    def test_QR(self):

        # data = {
        #     "admin_id": 123,
        #     "session_token": "unique_validation_token",
        #     "timestamp": "2024-12-13T10:00:00Z"
        # }
        # # 生成二维码 # QRコードを生成する
        # # img = qrcode.make(data="http://127.0.0.1:8000/home")
        # img = qrcode.make(data=data)
        # # 将二维码保存为图片 # QRコードを画像として保存する
        # with open('test.png', 'wb') as f:
        #     img.save(f)

        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            decoded_objs = decode(frame)
            a = ''
            for obj in decoded_objs:  # 遍历检测到的二维码数据，因为有很多张图片检测到 # 検出されたQRコードデータを繰り返し処理する。
                print(f'Decoded {obj.type} data: {obj.data.decode()}')
                a = obj.data.decode()
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == ord('q') or a != '':
                break

        webbrowser.open(a)  # 打开二维码网址 # QRコードのURLを開く

        cap.release()
        cv2.destroyAllWindows()
