import json
import base64
import hashlib
import hmac
from datetime import datetime, timedelta
import qrcode
from PIL import Image

SECRET_KEY = "admin"  # 用于签名验证的密钥
QR_VALIDITY_PERIOD = 7 * 24 * 60 * 60  # 7天，单位：秒


def generate_qr_code_data(admin_id, validity_days=7):
    """
    生成管理员二维码内容
    Args:
        admin_id: 管理员ID
        validity_days: QR码的有效天数（默认7天）
    Returns:
        dict: 包含管理员信息、有效期和签名的数据字典
    
        管理者用QRコードコンテンツの生成
    引数
        admin_id: 管理者ID
        validity_days: QRコードの有効日数（デフォルト7日）
    戻り値
        dict: 管理者情報、有効期限、署名を含むデータの辞書
    """
    current_time = datetime.now()
    expiry_time = current_time + timedelta(days=int(validity_days))

    # 构造数据
    data = {
        # "admin_id": admin_id,
        # "session_token": f"admin-{admin_id}-{int(current_time.timestamp())}",
        "created_at": current_time.strftime("%Y-%m-%d %H:%M:%S"),  # 转换为字符串存储 # 文字列ストレージに変換
        "validity_days": validity_days,
        "timestamp": int(current_time.timestamp())
    }

    # 将数据转换为 JSON 字符串 # データをJSON文字列に変換する
    data_string = json.dumps(data)

    # Base64编码 # Base64 エンコーディング
    encoded_data = base64.b64encode(data_string.encode()).decode()

    # 生成签名 # 署名生成
    signature = hmac.new(SECRET_KEY.encode(), encoded_data.encode(), hashlib.sha256).hexdigest()[:16]
    # signature = hmac.new(SECRET_KEY.encode(), encoded_data.encode(), lambda: hashlib.blake2b(digest_size=8)).hexdigest()  # digest_sizeで出力長を指定

    # 返回最终的数据结构 # 最終的なデータ構造を返す
    final_data = {
        "data": encoded_data,
        "signature": signature
    }

    return final_data


def generate_qr_code_image(qr_data) -> Image:
    """
    生成QR码图片
    Args:
        qr_data: 要编码到QR码中的数据（字典格式）
    Returns:
        Image: PIL Image对象

        QRコード画像の生成
    引数
        qr_data: QRコードにエンコードするデータ (辞書形式)
    戻り値
        Image: PIL Imageオブジェクト
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # 将整个数据结构（包含加密数据和签名）转换为JSON字符串
    # 暗号化されたデータと署名を含む）データ構造全体をJSON文字列に変換する。
    qr.add_data(json.dumps(qr_data))
    qr.make(fit=True)

    return qr.make_image(fill_color="black", back_color="white")


def validate_qr_code(encoded_data):
    """
    验证二维码内容，包括时限验证
    時間制限の検証を含むQRコード・コンテンツの検証
    """
    try:
        # 检查输入数据类型
        # 入力データ型のチェック
        if isinstance(encoded_data, str):
            qr_code = json.loads(encoded_data)
        elif isinstance(encoded_data, dict):
            qr_code = encoded_data
        else:
            return False, "invalid data type"

        # 获取加密数据和签名
        # 暗号化されたデータと署名を入手する
        data = qr_code.get("data", "")
        received_signature = qr_code.get("signature", "")

        # 验证签名
        # 署名を検証する
        expected_signature = hmac.new(SECRET_KEY.encode(), data.encode(), hashlib.sha256).hexdigest()[:16]
        # expected_signature = hmac.new(SECRET_KEY.encode(), encoded_data.encode(), lambda: hashlib.blake2b(digest_size=8)).hexdigest()
        if received_signature != expected_signature:
            return False, "signature mismatch"

        # Base64解码数据
        # Base64デコードされたデータ
        try:
            decoded_data = base64.b64decode(data).decode()
            qr_data = json.loads(decoded_data)
        except Exception:
            return False, "invalid data format"

        # 验证时间是否过期
        # 時間が経過していないことを確認する。
        created_at = datetime.strptime(qr_data.get("created_at"), "%Y-%m-%d %H:%M:%S")
        validity_days = int(qr_data.get("validity_days"))
        expires_at = created_at + timedelta(days=validity_days)

        current_time = datetime.now()

        if current_time > expires_at:
            return False, "QR Code expired"

        return True, "validation successful"
    except Exception as e:
        return False, f"validation error: {str(e)}"


# 示例测试代码
# テストコード例
if __name__ == "__main__":
    # 生成 QR 码数据
    # QRコードデータを生成する
    qr_data = generate_qr_code_data(admin_id=1)
    print("Generated QR Data:", qr_data)

    # 生成 QR 码图片
    # QR コード画像を生成する
    qr_image = generate_qr_code_image(qr_data)
    qr_image.save("admin_qr_code.png")
    print("QR Code image saved as 'admin_qr_code.png'")

    # 验证 QR 码数据
    # QRコードのデータを検証する
    validation_result, validation_message = validate_qr_code(qr_data)
    print("Validation Result:", validation_result)
    print("Validation Message:", validation_message)
