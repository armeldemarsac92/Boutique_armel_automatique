import subprocess
import sys
# Add these lines to your script where you want to execute the subprocess calls
subprocess_list = [
    "../Utilitaries/get_vinted_data_for_raindrops.py",
    "../Utilitaries/delete_sold_items_from_raindrop.py",
    "../Utilitaries/get_collections_and_item_data_from_raindrop.py",
    "../Utilitaries/restocking_app_headless.py"
]

for script in subprocess_list:
    print(f"Executing {script}")
    process = subprocess.Popen([sys.executable, script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(f"{script} completed.")
    print(f"stdout: {stdout}")
    print(f"stderr: {stderr}")
