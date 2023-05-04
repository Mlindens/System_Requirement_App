import tkinter as tk
import pyodbc
import psutil
import pynvml
import colorama
import os
from dotenv import load_dotenv

load_dotenv()

colorama.init(autoreset=True)

DRIVER = os.getenv('DB_DRIVER')
SERVER = os.getenv('DB_SERVER')
DATABASE = os.getenv('DB_DATABASE')
USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASSWORD')


class MinSpec:
    """
    Compares the user's system information to the minimum
    specifications required to run a selected application or game.

    Attributes:
        DRIVER (str): Retrieves the value of the 'DB_DRIVER' environment variable and assigns it to the variable DRIVER.
        SERVER (str): Retrieves the value of the 'DB_SERVER' environment variable and assigns it to the variable SERVER.
        DATABASE (str): Retrieves the value of the 'DB_DATABASE' environment variable and assigns it to the
        variable DATABASE.
        USERNAME (str): Retrieves the value of the 'DB_USERNAME' environment variable and assigns it to the
        variable USERNAME.
        PASSWORD (str):  Retrieves the value of the 'DB_PASSWORD' environment variable and assigns it to the
        variable PASSWORD.
        selection_to_app_id (dict): A dictionary mapping the selection names to application IDs.

    Methods:
        update_minspec(select_games, result_text): Fetches minimum specifications from a database and
        compares them to the user's system information, then updates the text widget with the results.
    """
    def __init__(self, selection_to_app_id):
        self.selection_to_app_id = selection_to_app_id

    def update_minspec(self, select_games, result_text):
        """
        Retrieves the minimum specifications for the selected application or game from the database,
        compares them to the user's system information, and updates the text widget with the results.

        Args:
            select_games (str): The selected game or application's name.
            result_text (tk.Text): The text widget that displays the comparison results.

        Returns:
            None
        """
        app_id = self.selection_to_app_id[select_games]
        with pyodbc.connect(
                'DRIVER=' + DRIVER + ';SERVER=tcp:' + SERVER + ';PORT=1433;DATABASE=' + DATABASE + ';UID=' + USERNAME +
                ';PWD=' + PASSWORD) as conn:
            with conn.cursor() as cursor:
                # Execute queries to fetch the minspec values for the selected application
                cursor.execute("SELECT minCPU FROM specsMin WHERE minspecID = ?", app_id)
                min_cpu_cores = cursor.fetchone()[0]
                cursor.execute("SELECT minSpeed FROM specsMin WHERE minspecID = ?", app_id)
                cpu_speed = cursor.fetchone()[0]
                cursor.execute("SELECT minMem FROM specsMin WHERE minspecID = ?", app_id)
                min_ram = cursor.fetchone()[0]
                cursor.execute("SELECT minStorage FROM specsMin WHERE minspecID = ?", app_id)
                min_storage = cursor.fetchone()[0]
                cursor.execute("SELECT minVRAM FROM specsMin WHERE minspecID = ?", app_id)
                min_vram = cursor.fetchone()[0]

                # Get user system information
                current_cpu_cores = psutil.cpu_count(logical=False)
                current_cpu_speed = psutil.cpu_freq().current / 1000
                current_ram = round(psutil.virtual_memory().total / (1024 ** 3))
                storage_size = psutil.disk_usage('/').free / (1024 ** 3)
                pynvml.nvmlInit()
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                device_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                vram = round(device_info.total / (1024 ** 2) / 1000)
                pynvml.nvmlShutdown()

                # Compare CPU cores
                cpu_string = f"Minimum CPU cores: {min_cpu_cores}\n"
                cpu_string += f"Current CPU cores: {current_cpu_cores}\n"
                cpu_string += f"Minimum CPU speed: {cpu_speed:.2f} GHz\n"
                cpu_string += f"Current CPU speed: {current_cpu_speed} GHz\n"
                if current_cpu_cores < min_cpu_cores:
                    cpu_1_check = False
                    cpu_2_check = False
                    cpu_result_string = f"Your CPU is below the minimum specs. Here are some products to consider: " \
                                        f"https://www.newegg.com/p/pl?d={min_vram:.0f}+core+{cpu_speed:.2f}ghz+cpu\n\n"
                elif current_cpu_cores == min_cpu_cores:
                    # Compare CPU speed
                    if current_cpu_speed < cpu_speed:
                        cpu_1_check = True
                        cpu_2_check = False
                        cpu_result_string = f"Your CPU speed is below the minimum specs. Here are some products to " \
                                            f"consider: https://www.newegg.com/p/pl?d={min_vram:.0f}" \
                                            f"+core+{cpu_speed:.2f}ghz+cpu\n\n"
                    else:
                        cpu_1_check = True
                        cpu_2_check = True
                        cpu_result_string = "Your CPU meets the minimum specs.\n\n"
                else:
                    cpu_1_check = True
                    cpu_2_check = True
                    cpu_result_string = "Your CPU meets the minimum specs.\n\n"

                # Compare RAM
                ram_string = f"Minimum RAM: {min_ram:.2f} GB\n"
                ram_string += f"Current RAM: {current_ram:.2f} GB\n"
                if current_ram < min_ram:
                    ram_check = False
                    ram_result_string = f"Your RAM is below the minimum specs. Here are some products to consider: " \
                                        f"https://www.newegg.com/p/pl?d={min_ram:.0f}gb+ram+card\n\n"
                else:
                    ram_check = True
                    ram_result_string = "Your RAM meets the minimum specs.\n\n"

                # Compare VRAM
                vram_string = f"Minimum VRAM: {min_vram:.2f} GB \n"
                vram_string += f"Current VRAM: {vram} GB \n"
                if vram < min_vram:
                    vram_check = False
                    vram_result_string = f"Your VRAM is below the minimum specs. Here are some products to consider: " \
                                         f"https://www.newegg.com/p/pl?d={min_vram:.0f}gb+graphics+card\n\n"
                else:
                    vram_check = True
                    vram_result_string = "Your VRAM meets the minimum specs.\n\n"

                # Compare free storage
                size_string = f"Minimum free storage required: {min_storage:.2f}\n"
                size_string += f"Current free storage: {storage_size:.2f} GB\n"
                if storage_size < min_storage:
                    size_check = False
                    size_result_string = f"You do not have enough storage. Here are some products to consider: " \
                                         f"https://www.newegg.com/p/pl?d={min_storage:.0f}gb+ssd\n\n"
                else:
                    size_check = True
                    size_result_string = "You have enough free storage."

                # Enable result text and delete current content to clear
                result_text.configure(state='normal')
                result_text.delete('1.0', tk.END)
                # Insert result strings
                result_text.insert('1.0', size_result_string)
                result_text.insert('1.0', size_string)
                result_text.insert('1.0', vram_result_string)
                result_text.insert('1.0', vram_string)
                result_text.insert('1.0', ram_result_string)
                result_text.insert('1.0', ram_string)
                result_text.insert('1.0', cpu_result_string)
                result_text.insert('1.0', cpu_string)

                # Set CPU core color
                if cpu_1_check:
                    result_text.tag_add('cpu_1_pass', '2.0', '2.100')
                    result_text.tag_configure('cpu_1_pass', background='green', foreground='white')
                else:
                    result_text.tag_add('cpu_1_fail', '2.0', '2.100')
                    result_text.tag_configure('cpu_1_fail', background='red', foreground='white')
                # Set CPU speed color
                if cpu_2_check:
                    result_text.tag_add('cpu_2_pass', '4.0', '4.100')
                    result_text.tag_configure('cpu_2_pass', background='green', foreground='white')
                else:
                    result_text.tag_add('cpu_2_fail', '4.0', '4.100')
                    result_text.tag_configure('cpu_2_fail', background='red', foreground='white')
                # Set RAM color
                if ram_check:
                    result_text.tag_add('ram_pass', '8.0', '8.100')
                    result_text.tag_configure('ram_pass', background='green', foreground='white')
                else:
                    result_text.tag_add('ram_fail', '8.0', '8.100')
                    result_text.tag_configure('ram_fail', background='red', foreground='white')
                # Set VRAM color
                if vram_check:
                    result_text.tag_add('vram_pass', '12.0', '12.100')
                    result_text.tag_configure('vram_pass', background='green', foreground='white')
                else:
                    result_text.tag_add('vram_fail', '12.0', '12.100')
                    result_text.tag_configure('vram_fail', background='red', foreground='white')
                # Set free disk space color
                if size_check:
                    result_text.tag_add('size_pass', '16.0', '16.100')
                    result_text.tag_configure('size_pass', background='green', foreground='white')
                else:
                    result_text.tag_add('size_fail', '16.0', '16.100')
                    result_text.tag_configure('size_fail', background='red', foreground='white')
                # Disable the result text to prevent the user from editing it
                result_text.configure(state='disabled')
