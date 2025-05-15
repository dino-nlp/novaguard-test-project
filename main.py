# novaguard-test-project/main.py

import os 
import sys 
import json 
import datetime # Unused import
import collections # Unused import

# Global variable that might be flagged as unused or for naming convention
GLOBAL_API_ENDPOINT = "https://api.example.com/data/hihi"

class OldStyleClass: # No explicit inheritance from object (for Python 2 style, Pylint might flag in Py3)
    pass

def processUserData(user_id, data_payload, transaction_id): # Naming convention & unused param
    """
    Processes user data.
    """
    TEMP_STATUS_VAR = "PROCESSING" # Naming convention & potentially unused if logic changes
    
    if user_id > 0 : # Inconsistent spacing
        user_info = {"id": user_id, "status": "active"}
    else:
        user_info = {"id": user_id, "status": "guest"}

    # Potential None dereference if data_payload is None or not a dict
    # and 'details' key is expected.
    try:
        details = data_payload['details']
        value = details['value']
        # Potential ZeroDivisionError
        if transaction_id != 0:
            processed_value = value / transaction_id 
        else:
            # This handling might be okay, but the division by zero is a risk.
            processed_value = -1 
            print("Transaction ID is zero, cannot process value normally.!!")
        
        # Inefficient string building in a loop
        log_message = ""
        for i in range(5): # Small loop, but demonstrates pattern
            log_message += f"Log entry {i}; "
        # logger.debug(log_message) # NameError: logger not defined

    except TypeError: # Broad exception, but okay for this example
        print(f"Error processing data for user {user_id}: Invalid data payload structure.")
        return None
    except KeyError:
        print(f"Error processing data for user {user_id}: Missing 'details' or 'value' in payload.")
        return None
    
    # Unused local variable
    final_check_passed = True
    
    return user_info, processed_value

def fetch_resource(resource_name, user_role="guest"):
    """
    Fetches a resource based on its name.
    Intended to have security vulnerabilities.
    """
    # Hardcoded secret/token
    SECRET_TOKEN = "super_secret_demo_token_123!@#zzz"
    
    # Path Traversal: resource_name is directly used.
    # The application should validate resource_name and ensure it's within an allowed directory.
    file_path = "/srv/resources/" + resource_name 
    
    # Insecure check (can be bypassed if resource_name contains ".." cleverly)
    if not os.path.normpath(file_path).startswith("/srv/resources/"):
        # This check is good, but the initial concatenation is the problem.
        # print(f"Access denied for resource: {resource_name}")
        return "Error: Access Denied."

    if user_role == "admin" : # Inconsistent spacing
        # Admin might have access to more, but token still exposed if used insecurely.
        print(f"Admin access for {resource_name} with token {SECRET_TOKEN}")
    
    try:
        # Create dummy resource if it doesn't exist for demo
        if not os.path.exists(file_path) and "public_info.txt" in resource_name :
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f_tmp:
                f_tmp.write(f"This is public resource: {resource_name}")

        with open(file_path, "r") as f:
            content = f.read(1024) # Reading a fixed amount might be an issue or fine
            # Sensitive information in exception
            # json.loads(content) # Potential TypeError/JSONDecodeError if content not JSON
            return content
    except FileNotFoundError:
        return f"Resource '{resource_name}' not found."
    except Exception as e: # Catching too broad exception
        # Sensitive information in exception (full path, error details)
        error_message = f"Failed to fetch resource {file_path}. Error: {str(e)}"
        # print(error_message) # Logging this directly could be an issue
        return "Error: Could not fetch resource."


def calculate_sums(number_sets):
    """
    Calculates sums, with potential for optimization and minor bugs.
    """
    grand_total = 0
    # Inefficient: multiple passes or complex single pass
    for i in range(len(number_sets)): # Could use "for current_set in number_sets:"
        current_set_total = 0
        # Potential TypeError if elements in number_sets[i] are not numbers
        for j in range(len(number_sets[i])): # Could use "for num in number_sets[i]:"
            current_set_total += number_sets[i][j]
        
        if current_set_total > 100: # Arbitrary logic
            grand_total += (current_set_total * 0.9) # Applying a "discount"
        else:
            grand_total += current_set_total
            
    # Unnecessary list creation if only sum is needed for this part
    squared_roots = []
    for k_set in number_sets:
        for val in k_set:
            if val > 0 : # Inconsistent spacing
                squared_roots.append(val**0.5) # Square root
    # print(f"Intermediate squared roots count: {len(squared_roots)}")
    return grand_total

# Function with many arguments (Pylint might flag)
def complex_configuration(p1,p2,p3,p4,p5,p6,p7,p8=None):
    # Multiple statements on one line
    x=p1+p2; y=p3-p4; z=p5*p6
    if p7 is None: p7 = 1
    
    result = (x * y) / p7 + (p8 if p8 is not None else 0)
    # print(f"Complex config result: {result}")
    return result

def main_application_logic():
    """Main logic for the application."""
    # logger.info("Application starting...") # NameError: logger

    user1_data, user1_val = processUserData(1, {"details": {"value": 100}}, 10)
    user2_data, user2_val = processUserData(0, {"details": {"value": 50}}, 0) # Test zero division
    user3_data, user3_val = processUserData(3, None, 5) # Test None payload

    print("\n--- Resources ---")
    public_resource = fetch_resource("public_info.txt")
    print(f"Public Resource: {public_resource[:60]}...")
    
    admin_resource = fetch_resource("admin_only/secret_data.txt", user_role="admin")
    # Create dummy admin resource if it doesn't exist for demo
    admin_file_path = "/srv/resources/admin_only/secret_data.txt"
    if not os.path.exists(admin_file_path) and "secret_data.txt" in admin_resource:
        os.makedirs(os.path.dirname(admin_file_path), exist_ok=True)
        with open(admin_file_path, "w") as f_tmp:
            f_tmp.write("This is admin secret data.")
        admin_resource = fetch_resource("admin_only/secret_data.txt", user_role="admin") # Re-fetch
    print(f"Admin Resource: {admin_resource[:60]}...")

    # Attempt Path Traversal
    malicious_request = "../../../etc/hostname" # Example
    print(f"Attempting to fetch '{malicious_request}': {fetch_resource(malicious_request)}")

    print("\n--- Calculations ---")
    sets_of_numbers = [[10, 20, 30], [50, 60, -10, 25], [5, 5, 5, 90]]
    # sets_of_numbers_type_error = [[10, "error", 30]] # Uncomment to test TypeError in calculate_sums
    total = calculate_sums(sets_of_numbers)
    print(f"Grand total from sets: {total}")

    complex_config_val = complex_configuration(1,2,3,4,5,6,7,p8=10)
    # print(f"Result of complex_configuration: {complex_config_val}")

    # Logic error: this condition will always be false
    if 1 == 0 :
        print("This should not print.")

    # Example of eval, if not caught by other means
    # eval_string = "os.system('ls -la /')" # Highly dangerous
    # print(f"Running eval (dangerous): {eval(eval_string)}")

    print("Application finished.")

if __name__ == "__main__":
    main_application_logic()