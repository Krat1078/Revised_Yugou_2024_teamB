import json
import time
import hashlib
import hmac
import base64
import json
import time
import hashlib
import hmac

SECRET_KEY = "admin"  # 用于签名验证的密钥 # 署名検証用キー
QR_VALIDITY_PERIOD = 7 * 24 * 60 * 60  # 7天，单位：秒 # 7日間を秒単位で

def generate_qr_code_data(admin_id):
    """
    生成管理员二维码内容，有效期为一周
    1週間有効の管理者用QRコードコンテンツを生成する
    """
    timestamp = int(time.time())  # 当前时间戳 # 現在のタイムスタンプ
    data = {
        "admin_id": admin_id,
        "session_token": f"admin-{admin_id}-{timestamp}",  # 唯一token # ユニークトークン
        "timestamp": timestamp  # 二维码生成的时间戳 # QRコード生成のタイムスタンプ
    }
    # 使用签名进行验证 # 署名による認証
    data_string = json.dumps(data)
    signature = hmac.new(SECRET_KEY.encode(), data_string.encode(), hashlib.sha256).hexdigest()
    data["signature"] = signature
    return data

def validate_qr_code(data):
    """
    验证二维码内容，包括时限验证
    時間制限の検証を含むQRコード・コンテンツの検証
    """
    # SECRET_KEY = "your_secret_key"
    # QR_VALIDITY_PERIOD = 7 * 24 * 60 * 60  # 7天，单位：秒 # 7日間を秒単位で

    try:
        if isinstance(data, str):
            # 将单引号替换为双引号，转换为标准 JSON 格式
            # シングルクォートをダブルクォートに置き換え、標準的なJSONフォーマットに変換する。
            if data.startswith("{") and data.endswith("}"):
                qr_data = data.replace("'", '"')  # 替换单引号为双引号 # シングルクォートをダブルクォートに置き換える
            qr_code = json.loads(data)  # 尝试解析为字典 # 辞書へのパースを試みる
        else:
            qr_code = data  # 已经是字典，直接使用 # dataはすでに辞書なので、それを直接使う
        # 解析二维码数据 # QRコードデータの解析
        signature = qr_code.pop("signature", "")

        # 重建签名 # 署名の再構築
        data_string = json.dumps(qr_code)
        expected_signature = hmac.new(SECRET_KEY.encode(), data_string.encode(), hashlib.sha256).hexdigest()

        # 验证签名 # 署名を検証する
        if signature != expected_signature:
            return False, "signature mismatch"

        # 验证时间戳是否过期 # タイムスタンプが期限切れでないことを確認する。
        timestamp = qr_code.get("timestamp")
        current_time = int(time.time())
        if current_time - int(timestamp) > QR_VALIDITY_PERIOD:
            return False, "QR Code Expired"

        return True, "validation successful"
    except Exception as e:
        return False, f"validation error: {str(e)}"
