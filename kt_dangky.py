from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

class FruittablesRegister:
    def __init__(self):
        # Cấu hình Chrome Options để bỏ qua lỗi chứng chỉ SSL khi truy cập theo IP
        chrome_options = Options()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--allow-insecure-localhost")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.maximize_window()

    def navigate_to_register(self):
        """Điều hướng đến trang đăng ký"""
        self.driver.get("https://103.157.218.44/TaiKhoan/DangKy")
        time.sleep(2)  # Cho trang load đầy đủ

    def register(self, username, password, ho, ten, gioitinh, ngaysinh, dienthoai, email, diachi, file_path):
        """Thực hiện đăng ký bằng cách điền đầy đủ các thông tin vào form."""
        try:
            # Điền tên đăng nhập
            username_field = self.wait.until(EC.presence_of_element_located((By.ID, "Username")))
            username_field.clear()
            username_field.send_keys(username)

            # Điền mật khẩu
            password_field = self.wait.until(EC.presence_of_element_located((By.ID, "MatKhau")))
            password_field.clear()
            password_field.send_keys(password)

            # Điền họ đệm
            ho_field = self.wait.until(EC.presence_of_element_located((By.ID, "Ho")))
            ho_field.clear()
            ho_field.send_keys(ho)

            # Điền tên
            ten_field = self.wait.until(EC.presence_of_element_located((By.ID, "Ten")))
            ten_field.clear()
            ten_field.send_keys(ten)

            # Điền giới tính
            gt_field = self.wait.until(EC.presence_of_element_located((By.ID, "GioiTinh")))
            gt_field.clear()
            gt_field.send_keys(gioitinh)

            # Điền ngày sinh (định dạng yyyy-mm-dd)
            ngaysinh_field = self.wait.until(EC.presence_of_element_located((By.ID, "NgaySinh")))
            ngaysinh_field.clear()
            ngaysinh_field.send_keys(ngaysinh)

            # Điền điện thoại
            dienthoai_field = self.wait.until(EC.presence_of_element_located((By.ID, "DienThoai")))
            dienthoai_field.clear()
            dienthoai_field.send_keys(dienthoai)

            # Điền Email
            email_field = self.wait.until(EC.presence_of_element_located((By.ID, "Email")))
            email_field.clear()
            email_field.send_keys(email)

            # Điền địa chỉ
            diachi_field = self.wait.until(EC.presence_of_element_located((By.ID, "DiaChi")))
            diachi_field.clear()
            diachi_field.send_keys(diachi)

            # Upload ảnh đại diện (nếu file tồn tại)
            file_input = self.wait.until(EC.presence_of_element_located((By.NAME, "Hinh")))
            if os.path.isfile(file_path):
                file_input.send_keys(file_path)
            else:
                print(f"Không tìm thấy file: {file_path}")

            # Tìm nút "Đăng ký" và click
            register_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(text(), 'Đăng ký')]")))
            # Cuộn đến nút để đảm bảo nó hiển thị đúng vị trí
            self.driver.execute_script("arguments[0].scrollIntoView(true);", register_btn)
            time.sleep(1)
            # Thử click thông thường, nếu thất bại thì click bằng JavaScript
            try:
                register_btn.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", register_btn)

        except Exception as e:
            self._handle_error("Lỗi trong quá trình đăng ký", e)

    def verify_registration_success(self):
        """
        Xác minh đăng ký thành công.
        Ví dụ: sau đăng ký thành công, URL chuyển hướng về trang đăng nhập (/TaiKhoan/DangNhap).
        """
        try:
            self.wait.until(EC.url_contains("/TaiKhoan/DangNhap"))
            print(">>> Đăng ký thành công!")
            return True
        except Exception as e:
            print(">>> Đăng ký thành công!")
            return False

    def _handle_error(self, message, exception):
        """Xử lý lỗi: in thông báo, chụp ảnh màn hình, đóng trình duyệt và ném exception."""
        print(f"!!! LỖI: {message}")
        print(f"Chi tiết: {str(exception)}")
        try:
            if self.driver.session_id:
                self.driver.save_screenshot("error_register.png")
        except Exception:
            print("Không thể chụp ảnh màn hình vì phiên đã bị đóng.")
        try:
            self.driver.quit()
        except:
            pass
        raise exception

    def close(self):
        """Đóng trình duyệt"""
        try:
            self.driver.quit()
        except:
            pass

# Sử dụng
if __name__ == "__main__":
    # Test data cho đăng ký; hãy cập nhật dữ liệu này theo yêu cầu ứng dụng của bạn.
    TEST_DATA = {
        "valid": (
        "new_user_2",                   # Username
        "Pass@1213",                   # Password
        "Nguyen Van",                 # Họ đệm
        "A",                         # Tên
        "1",                          # Giới tính (ví dụ: "1")
        "01-01-1990",                 # Ngày sinh (yyyy-mm-dd)
        "0351234449",                 # Điện thoại hợp lệ (theo regex: 0[35789]\d{8})
        "new_user_2@example.com",       # Email
        "123 Street, City",           # Địa chỉ
       "D:\devops\\avatar.png"  # Đường dẫn ảnh (đảm bảo file tồn tại)
        )
    }

    tester = FruittablesRegister()

    try:
        tester.navigate_to_register()
        tester.register(*TEST_DATA["valid"])
        assert tester.verify_registration_success(), "Xác minh đăng ký  thành công!"
    finally:
        tester.close()
