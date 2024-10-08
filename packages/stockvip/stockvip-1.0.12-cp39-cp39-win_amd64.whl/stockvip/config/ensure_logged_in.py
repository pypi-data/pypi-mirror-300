from functools import wraps
from stockvip.process_client.login import Client

def ensure_logged_in(func):
    """
    Decorator để đảm bảo rằng Client đã đăng nhập trước khi thực hiện function.
    Nếu chưa đăng nhập, raise Exception.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Lấy instance của Client (Singleton)
        client = Client()

        # Kiểm tra xem đã có token chưa (tức là đã đăng nhập thành công)
        if client.token is None:
            raise Exception("Chưa đăng nhập. Vui lòng đăng nhập trước.")

        # Nếu đã đăng nhập, gọi function thực tế
        return func(*args, **kwargs)

    return wrapper
