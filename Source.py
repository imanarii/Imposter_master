# offsets 0x28, 0x5C, 0x0, 0x34, 0x28,
# cool down offsets 0x44, 0x1C, 0x28, 0x5C, 0x0, 0x44

import subprocess
import pymem
import pymem.process
import keyboard
import time

pm = pymem.Pymem('Among Us.exe')
client = pymem.process.module_from_name(pm.process_handle, "GameAssembly.dll").lpBaseOfDll

imposter = (0x01468910)
i_offset_1 = (0x5C)
i_offset_2 = (0x0)
i_offset_3 = (0x34)
i_offset_4 = (0x28)
#i_offset_5 = (0x28)

i_base = pm.read_int(client + imposter)
i_off_1 = pm.read_int(i_base + i_offset_1)
i_off_2 = pm.read_int(i_off_1 + i_offset_2)
i_off_3 = pm.read_int(i_off_2 + i_offset_3)
i_off_4 = pm.read_int(i_off_3 + i_offset_4)
#i_off_5 = pm.read_int(i_off_4 + i_offset_5)
imposter_val = i_off_3 + i_offset_4

kill = (0x01472280)
k_offset_1 = (0x5C)
k_offset_2 = (0x20)
k_offset_3 = (0x44)
#k_offset_4 = (0x5C)
#k_offset_5 = (0x0)
#k_offset_6 = (0x44)

k_base = pm.read_int(client + kill)
k_off_1 = pm.read_int(k_base + k_offset_1)
k_off_2 = pm.read_int(k_off_1 + k_offset_2)
k_off_3 = pm.read_int(k_off_2 + k_offset_3)
#k_off_4 = pm.read_int(k_off_3 + k_offset_4)
#k_off_5 = pm.read_int(k_off_4 + k_offset_5)
#k_off_6 = pm.read_int(k_off_5 + k_offset_6)
kill_val = k_off_2 + k_offset_3
#kill_countdown = pm.read_int(kill_val)

def menu():
    subprocess.call('cls', shell=True)
    print('###############################################################################################################')
    print('#                                                                                                             #')
    print('#                                               WARNING !!!!!!!                                               #')
    print('#       IF YOU WERE NOT THE ORIGINAL IMPOSTER AND HAVE IT TOGGLED DURING THE VOTE IT CAN CRASH THE GAME       #')
    print('#                                                                                                             #')
    print('#                                                                                                             #')
    print('###############################################################################################################')
    print('\nopen and close map to get kill option after you toggle imposter\nPress "ins" to toggle imposter.\nPress "q" to exit')
    print(imposter_val)
    print(i_off_1)
    print(i_off_2)
    print(i_off_3)
    print(i_off_4)

menu()


while keyboard.is_pressed('q') == False:
    imposter_status = pm.read_int(imposter_val)
    kill_countdown = pm.read_int(kill_val)


    if kill_countdown != 0:
        pm.write_int(kill_val, 0)

    if keyboard.is_pressed('ins'):
        time.sleep(.15)

        if imposter_status == 1:
            pm.write_int(imposter_val , 0)
            menu()
            print('You are not the imposter')
        else:
            pm.write_int(imposter_val , 1)
            menu()
            print('You are the imposter')
