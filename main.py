import os
import sys

def process_data(data, factor ):
    unused_var = 1234

    if data is not None:
        try:
            processed_value = len(data) / factor 
        except ZeroDivisionError:
            print("Cannot divide by zero!") 
            processed_value = float('inf')

        result_list = []
        for item in data:
             result_list.append(str(item) * factor) 

        return processed_value, result_list
    return 0, [] 

def insecure_function(user_input):
    try:
        with open("/tmp/user_files/" + user_input, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        print(f"Error reading file: {e}") # Log lỗi có thể lộ thông tin (SecuriSense?)
        return "Error reading file."


def main():
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
    user_file = "../../etc/passwd" # Ví dụ Path Traversal
    # user_file = "safe_file.txt" # trường hợp an toàn
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
    main()

