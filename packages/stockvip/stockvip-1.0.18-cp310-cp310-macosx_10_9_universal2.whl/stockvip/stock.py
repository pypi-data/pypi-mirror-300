from stockvip.config.ensure_logged_in import ensure_logged_in
from stockvip.process_stock.ohlcv import get_ohlcv
import pandas as pd
from datetime import datetime

class Stock:
    """
    Lớp Stock đại diện cho một mã cổ phiếu và cung cấp phương thức để lấy dữ liệu liên quan đến mã cổ phiếu.

    Attributes:
        ticker (str): Mã cổ phiếu, ví dụ như "HPG".
    """

    def __init__(self, ticker: str) -> None:
        """
        Khởi tạo đối tượng Ticker với mã cổ phiếu cụ thể.

        Args:
            ticker (str): Mã cổ phiếu (ví dụ: "HPG").
        """
        self.ticker = ticker
        self.data = None  # Có thể khởi tạo self.data là None

    @ensure_logged_in
    def ohlcv(self, fromDate: str, toDate: str, period: str = "D") -> pd.DataFrame:
        """
        Trả về dữ liệu lịch sử giao dịch của mã cổ phiếu trong khoảng thời gian cụ thể với khoảng thời gian tùy chọn.

        Phương thức này yêu cầu người dùng đã đăng nhập và lấy dữ liệu giao dịch của mã cổ phiếu 
        từ ngày `fromDate` đến ngày `toDate`. Người dùng có thể chọn khoảng thời gian (`period`) cho dữ liệu là ngày, tuần, tháng, hoặc các chu kỳ dài hơn.

        Args:
            fromDate (str): Ngày bắt đầu dưới định dạng 'YYYY-MM-DD'.
            toDate (str): Ngày kết thúc dưới định dạng 'YYYY-MM-DD'.
            period (str): Khoảng thời gian của dữ liệu. Mặc định là "D" (ngày).
                         
                         Các lựa chọn hợp lệ bao gồm:
                         
                         - "D": Hàng ngày (Daily)
                         - "W": Hàng tuần (Weekly)
                         - "1M": Hàng tháng (1 Month)
                         - "3M": 3 tháng (3 Months)
                         - "6M": 6 tháng (6 Months)
                         - "1Y": 1 năm (1 Year)
                         - "3Y": 3 năm (3 Years)

        Returns:
            pd.DataFrame: Dữ liệu giao dịch của mã cổ phiếu, bao gồm các cột như giá mở cửa, giá đóng cửa, khối lượng giao dịch, v.v.

        Raises:
            ValueError: Nếu định dạng ngày không đúng (phải là 'YYYY-MM-DD') hoặc period không hợp lệ.
            Exception: Nếu có lỗi xảy ra khi kết nối API hoặc token hết hạn.

        Example:
            >>> import stockvip as sv
            >>> sv.Connect("0123456789", "password123")
            >>> hpg = sv.Stock("HPG")
            >>> df = hpg.ohlcv(fromDate="2024-01-01", toDate="2024-09-30", period="W")
            >>> print(df.head())
        """
        # Kiểm tra tính hợp lệ của period
        valid_periods = ["D", "W", "1M", "3M", "6M", "1Y", "3Y"]
        if period not in valid_periods:
            raise ValueError(f"Period '{period}' không hợp lệ. Chỉ chấp nhận các giá trị: {', '.join(valid_periods)}")
        
        # Lấy dữ liệu giao dịch từ API với ticker và khoảng thời gian cụ thể
        data = get_ohlcv(
            ticker=self.ticker,
            fromDate=fromDate,
            toDate=toDate,
            period=period  # Thêm tham số period để điều chỉnh dữ liệu theo chu kỳ
        )
        return data

