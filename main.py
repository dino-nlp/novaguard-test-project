# main.py (trong novaguard-test-project)
import os # Lỗi: Unused import (StyleGuardian / Pylint)
import sys # Lỗi: Unused import (StyleGuardian / Pylint)

# Lỗi: Thiếu docstring cho function (StyleGuardian / Pylint)
def process_data(data, factor ): # Lỗi: Khoảng trắng thừa trước dấu hai chấm, thừa sau factor (StyleGuardian / Pylint)
    # Lỗi: Biến không được sử dụng (StyleGuardian / Pylint)
    unused_var = 123

    # Lỗi tiềm ẩn: Nếu data là None thì sao? (BugHunter)
    if data is not None:
         # Lỗi tiềm ẩn: Chia cho zero nếu factor = 0 (BugHunter)
         # Sửa lại để chắc chắn có lỗi chia cho zero nếu factor = 0
         try:
             processed_value = len(data) / factor 
         except ZeroDivisionError:
             print("Cannot divide by zero!") # Xử lý lỗi, nhưng vẫn là một logic cần xem xét
             processed_value = float('inf')

         # Lỗi tiềm ẩn: Có thể không hiệu quả nếu data rất lớn (OptiTune)
         result_list = []
         for item in data:
             result_list.append(str(item) * factor) # Có thể tối ưu?

         return processed_value, result_list
    return 0, [] # Trả về giá trị mặc định nếu data là None

def insecure_function(user_input):
    # Lỗi bảo mật: Sử dụng user_input trực tiếp trong đường dẫn file (Path Traversal - SecuriSense / Semgrep)
    # Lưu ý: Cần Semgrep rules phù hợp để phát hiện lỗi này
    try:
        with open("/tmp/user_files/" + user_input, 'r') as f:
            return f.read()
    except FileNotFoundError:
         return "File not found."
    except Exception as e:
         print(f"Error reading file: {e}") # Log lỗi có thể lộ thông tin (SecuriSense?)
         return "Error reading file."


# Lỗi: Thiếu docstring (StyleGuardian / Pylint)
def main():
    # Giả lập data đầu vào
    my_data = ["apple", "banana", "cherry"]
    factor_zero = 0
    factor_two = 2

    print("Processing with factor zero:")
    val0, list0 = process_data(my_data, factor_zero)
    print(f"Value: {val0}, List length: {len(list0)}")

    print("\nProcessing with factor two:")
    val2, list2 = process_data(my_data, factor_two)
    print(f"Value: {val2}, List length: {len(list2)}")

    # Giả lập input không an toàn
    # user_file = "../../etc/passwd" # Ví dụ Path Traversal
    user_file = "safe_file.txt" # Giả lập trường hợp an toàn
    # Tạo file tạm để test
    try:
         os.makedirs("/tmp/user_files", exist_ok=True)
         with open("/tmp/user_files/safe_file.txt", "w") as f:
              f.write("This is a safe file.")
    except OSError as e:
         print(f"Could not create test file setup: {e}")

    print(f"\nReading file: {user_file}")
    content = insecure_function(user_file)
    print(f"Content:\n{content}")


if __name__ == "__main__":
    main() # Lỗi: Thiếu docstring (StyleGuardian / Pylint)

# Thêm một comment không cần thiết vào cuối file
# Unnecessary comment