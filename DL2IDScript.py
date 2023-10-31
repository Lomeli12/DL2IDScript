# MIT License
# Copyright © 2023 Lomeli
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the “Software”),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be (included in
# all) copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import shutil
import pathlib
import zipfile

BASE_DATA_NAME = "data"
DATA_PAK_EXT = ".pak"

DATA_0_FILE_NAME = BASE_DATA_NAME + "0" + DATA_PAK_EXT

SCRIPTS_DIR_NAME = "scripts"
PLAYER_DIR_NAME = "player"

PLAYER_SCRIPTS_PATH = "" + SCRIPTS_DIR_NAME + "/" + PLAYER_DIR_NAME + "/"

PLAYER_NORMAL_SCRIPT = "player_variables.scr"
PLAYER_NORMAL_SCRIPT_PATH = PLAYER_SCRIPTS_PATH + PLAYER_NORMAL_SCRIPT
PLAYER_NORMAL_DURABILITY_TEXT = "	Param(\"MeleeWpnDurabilityMulReduce\", \"1.0\");"

PLAYER_EASY_SCRIPT = "player_variables_easy.scr"
PLAYER_EASY_SCRIPT_PATH = PLAYER_SCRIPTS_PATH + PLAYER_EASY_SCRIPT
PLAYER_EASY_DURABILITY_TEXT = "    Param(\"MeleeWpnDurabilityMulReduce\", \"0.75\");"

PLAYER_NIGHTMARE_SCRIPT = "player_variables_nightmare.scr"
PLAYER_NIGHTMARE_SCRIPT_PATH = PLAYER_SCRIPTS_PATH + PLAYER_NIGHTMARE_SCRIPT
PLAYER_NIGHTMARE_DURABILITY_TEXT = "    Param(\"MeleeWpnDurabilityMulReduce\", \"1.25\");"

INFINITE_DURABILITY_PATCH_TEXT = "    Param(\"MeleeWpnDurabilityMulReduce\", \"0.0\");"

data_0_location = ""
data_0_parent_dir = ""

scripts_dir = ""
player_dir = ""

temp_folder = ""
temp_normal_path = ""
temp_easy_path = ""
temp_nightmare_path = ""


def patch_script(script_path, patch_loc, name):
    with open(script_path, 'r') as script:
        script_data = script.read()

    print("-> Patching " + name)
    script_data = script_data.replace(patch_loc, INFINITE_DURABILITY_PATCH_TEXT)

    with open(script_path, 'w') as script:
        script.write(script_data)


def patch_scripts():
    patch_script(temp_normal_path, PLAYER_NORMAL_DURABILITY_TEXT, PLAYER_NORMAL_SCRIPT)
    patch_script(temp_easy_path, PLAYER_EASY_DURABILITY_TEXT, PLAYER_EASY_SCRIPT)
    patch_script(temp_nightmare_path, PLAYER_NIGHTMARE_DURABILITY_TEXT, PLAYER_NIGHTMARE_SCRIPT)


def create_temp_folder():
    global temp_folder
    temp_folder = os.path.join(os.getcwd(), "temp_mod_folder")
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)
    os.mkdir(temp_folder)
    global scripts_dir
    scripts_dir = os.path.join(temp_folder, SCRIPTS_DIR_NAME)
    os.mkdir(scripts_dir)
    global player_dir
    player_dir = os.path.join(scripts_dir, PLAYER_DIR_NAME)
    os.mkdir(player_dir)


def find_suitable_pak_name(count):
    data_pak = os.path.join(data_0_parent_dir, BASE_DATA_NAME + str(count) + DATA_PAK_EXT)
    if os.path.exists(data_pak):
        count = count + 1
        return find_suitable_pak_name(count)
    return data_pak


def create_or_replace_mod():
    replace_pak = input("Replace data2.pak, if it exists? (Y/N): ")
    mod_data_pak = os.path.join(data_0_parent_dir, BASE_DATA_NAME + "2" + DATA_PAK_EXT)
    if replace_pak.lower() == "n":
        print("-> Looking for unused data pak number")
        mod_data_pak = find_suitable_pak_name(3)
        print("-> Using " + os.path.basename(mod_data_pak))
    elif replace_pak.lower() != "y":
        create_or_replace_mod()

    package_mod(mod_data_pak)


def package_mod(data_pak):
    print("-> Creating " + data_pak + "!")
    if os.path.exists(data_pak):
        print("-> Removing old " + os.path.basename(data_pak))
        os.remove(data_pak)

    shutil.make_archive(data_pak, 'zip', temp_folder)
    os.rename(data_pak + ".zip", data_pak)


def clean_up():
    print("-> Cleaning up temp folder")
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)


def extract_player_scripts():
    with zipfile.ZipFile(data_0_location) as data:
        global temp_normal_path
        temp_normal_path = os.path.join(player_dir, PLAYER_NORMAL_SCRIPT)
        extract_scripts(data, PLAYER_NORMAL_SCRIPT, PLAYER_NORMAL_SCRIPT_PATH, temp_normal_path)
        global temp_easy_path
        temp_easy_path = os.path.join(player_dir, PLAYER_EASY_SCRIPT)
        extract_scripts(data, PLAYER_EASY_SCRIPT, PLAYER_EASY_SCRIPT_PATH, temp_easy_path)
        global temp_nightmare_path
        temp_nightmare_path = os.path.join(player_dir, PLAYER_NIGHTMARE_SCRIPT)
        extract_scripts(data, PLAYER_NIGHTMARE_SCRIPT, PLAYER_NIGHTMARE_SCRIPT_PATH, temp_nightmare_path)


def extract_scripts(data, script_name, script_path, script_out_path):
    print("-> Extracting " + script_name)
    with open(script_out_path, 'wb') as script:
        script.write(data.read(script_path))


def handle_data_0_location(file_path):
    file_correct = False
    if os.path.isdir(file_path):
        file_path = os.path.join(file_path, DATA_0_FILE_NAME)

    if os.path.exists(file_path):
        print("data0.pak located at: " + file_path)
        correct = input("Is this correct? (Y/N/Q): ")
        if correct.lower() == "y":
            global data_0_location
            data_0_location = file_path
            global data_0_parent_dir
            data_0_parent_dir = pathlib.Path(file_path).parent
            file_correct = True
        elif correct.lower() == "q":
            exit()
    else:
        print("Could not find data0.pak at " + file_path)
        print(file_path + " does not exist!")

    if not file_correct:
        print("Could not find data0.pak location!")
        handle_data_0_location(input("Type in the path for data0.pak: "))


def create_mod():
    start_mod_creation = input("Create Infinite Durability mod using " + data_0_location + "? (Y/N): ")
    if start_mod_creation.lower() == "n":
        exit()

    if start_mod_creation.lower() != "y":
        create_mod()

    create_temp_folder()
    extract_player_scripts()
    patch_scripts()
    create_or_replace_mod()
    clean_up()


def intro_message():
    print("||==============================================||")
    print("|| Dying Light 2 Durability Mod Creation Script ||")
    print("||================= By Lomeli ==================||")


intro_message()
handle_data_0_location(os.path.join(os.getcwd(), DATA_0_FILE_NAME))
create_mod()
os.system('pause')
