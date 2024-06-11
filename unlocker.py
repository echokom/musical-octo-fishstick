#if you are reading this, i am not the creator of the method of unlocking, i just made it automatic, plz dont bully me (пожалуйста)
#discord: tualkom     /   and please dont steal the code, i will be really sad :(       (ну пожалуйста)
#version 1.0, 11 july 2024


import os
import shutil
print("WARNING: MAKE A BACKUP OF YOUR CAR IN CASE OF AN ERROR!")
print("WARNING: UNPACK THE DATA.ACD BEFORE USE, AFTER COMPLETING THE OPERATION, PACK THE DATA.ACD BACK")
print("discord: tualkom")
import ctypes
ctypes.windll.kernel32.SetConsoleTitleW("by.tualkom fast-unlocker")
def create_folder(folder_name):
    current_directory = os.getcwd()
    new_folder_path = os.path.join(current_directory, folder_name)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    return new_folder_path

def delete_script_lua(data_folder):
    script_file = os.path.join(data_folder, "script.lua")
    if os.path.exists(script_file):
        os.remove(script_file)

def move_data_acd(current_directory, new_folder_path):
    data_acd_file = os.path.join(current_directory, "data.acd")
    if os.path.exists(data_acd_file):
        shutil.move(data_acd_file, os.path.join(new_folder_path, "data.acd"))

def find_and_copy_kn5_files(current_directory, folder_name, new_folder_path):
    kn5_files = [f for f in os.listdir(current_directory) if f.endswith(".kn5")]
    if kn5_files:
        similar_file = max(kn5_files, key=lambda x: len(set(x).intersection(set(folder_name))))
        if similar_file:
            similar_file_path = os.path.join(current_directory, similar_file)
            shutil.copy(similar_file_path, os.path.join(new_folder_path, similar_file))
            return similar_file, kn5_files
    return None, kn5_files

def update_lods_ini(data_folder, folder_name, similar_file, kn5_files, copy_lods_files=False):
    lods_ini_path = os.path.join(data_folder, "lods.ini")
    if os.path.exists(lods_ini_path):
        with open(lods_ini_path, "r") as f:
            lines = f.readlines()
    else:
        lines = []
    # Обновляем или добавляем основное имя файла
    lines = [line for line in lines if similar_file not in line]
    lines.append(f"{folder_name}/{similar_file}\n")
    if copy_lods_files:
        updated_lines = []
        for line in lines:
            if any(kn5_file in line for kn5_file in kn5_files if "lods" in kn5_file):
                line = f"{folder_name}/{line.strip()}\n"
            updated_lines.append(line)
        lines = updated_lines
    with open(lods_ini_path, "w") as f:
        f.writelines(lines)

def modify_aero_ini(data_folder):
    aero_ini_path = os.path.join(data_folder, "aero.ini")
    if os.path.exists(aero_ini_path):
        with open(aero_ini_path, "r") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith("CL_GAIN"):
                lines[i] = "CL_GAIN = 1.0\n"
            elif line.startswith("CD_GAIN"):
                lines[i] = "CD_GAIN = 1.08\n"
        with open(aero_ini_path, "w") as f:
            f.writelines(lines)

def create_folder_classic():
    try:
        current_directory = os.getcwd()
        folder_name = os.path.basename(current_directory)
        new_folder_path = create_folder(folder_name)
        data_folder = os.path.join(current_directory, "data")
        delete_script_lua(data_folder)
        move_data_acd(current_directory, new_folder_path)
        similar_file, kn5_files = find_and_copy_kn5_files(current_directory, folder_name, new_folder_path)
        if similar_file:
            update_lods_ini(data_folder, folder_name, similar_file, kn5_files)
    except Exception as e:
        print(f"An error occurred: {e}")

def create_folder_non_classic():
    try:
        current_directory = os.getcwd()
        folder_name = os.path.basename(current_directory)
        new_folder_path = create_folder(folder_name)
        data_folder = os.path.join(current_directory, "data")
        delete_script_lua(data_folder)
        move_data_acd(current_directory, new_folder_path)
        similar_file, kn5_files = find_and_copy_kn5_files(current_directory, folder_name, new_folder_path)
        if similar_file:
            update_lods_ini(data_folder, folder_name, similar_file, kn5_files, copy_lods_files=True)
        for kn5_file in kn5_files:
            if "lods" in kn5_file and not os.path.exists(os.path.join(new_folder_path, kn5_file)):
                kn5_file_path = os.path.join(current_directory, kn5_file)
                shutil.copy(kn5_file_path, os.path.join(new_folder_path, kn5_file))
        modify_aero_ini(data_folder)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Choose the method to use:")
    print("1. Classic method")
    print("2. Non-classic method (used for nohesi carpack)")

    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        create_folder_classic()
    elif choice == "2":
        create_folder_non_classic()
    else:
        print("Invalid choice. Please enter either '1' or '2'.")

    input("Press Enter to exit...")  # Wait for the user to press Enter before exiting
