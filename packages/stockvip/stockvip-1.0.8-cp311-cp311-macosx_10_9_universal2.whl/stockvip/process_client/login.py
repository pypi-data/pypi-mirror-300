from stockvip.config.config import base_url
import requests
class Client:
    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Client, cls).__new__(cls)
            cls._instance.base_url = base_url
            cls._instance.token = None
            cls._instance.phone_number = None
            cls._instance.password = None
        return cls._instance

    def login(self, phone_number: str, password: str) -> bool:
        """
        Đăng nhập vào hệ thống và lưu trữ token xác thực.

        Args:
            phone_number (str): Số điện thoại của bạn.
            password (str): Mật khẩu.

        Returns:
            bool: True nếu đăng nhập thành công, False nếu thất bại.
        """
        url = f"{self.base_url}/api/login"
        payload = {"phone_number": phone_number, "password": password}
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            print("🎉 Đăng nhập thành công!")
            self.token = response.json().get("access_token")
            self.phone_number = phone_number
            self.password = password
            return True
        else:
            print(f"⛔️ Đăng nhập thất bại: {response.status_code} - {response.text}")
            return False

    def _get_headers(self) -> dict:
        if self.token:
            return {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
        else:
            raise Exception("⚠️ Chưa đăng nhập. Vui lòng gọi hàm login trước.")

    def _refresh_token(self) -> bool:
        if self.phone_number and self.password:
            print("⚠️ Token đã hết hạn. Đang thực hiện đăng nhập lại...")
            return self.login(self.phone_number, self.password)
        return False
