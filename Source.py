
import subprocess
import pymem
import pymem.process
import keyboard
import time

pm = pymem.Pymem('Among Us.exe')
client = pymem.process.module_from_name(pm.process_handle, "GameAssembly.dll").lpBaseOfDll

# FindAddress  WORKS FOR UP TO 6 OFFSETS but can be easily updated
# format for passing the offsets:
# first give it the base address without the client
# then the amount of offsets you're about to give it
# then the offsets in order but you have to tell the func what offset it is
# e.g 0x01472280, 4, offset1 = 0x6f, offset2 = 0x66, offset3 = 0x66

# 72 69 63 6b 20 72 6f 6c 6c 65 64 20 0d 0a  <<< Convert to ascii

def FindAddress(base, amount, **offsets, ):

    print(offsets, base, amount)
    base = pm.read_int(client + base)
    off1 = pm.read_int(base + offsets["offset1"])
    if amount == 1:
        address = base + offsets["offset1"]
        return address


    else:
        off2 = pm.read_int(off1 + offsets["offset2"])
        if amount == 2:
            address = off1 + offsets["offset2"]
            return address
        else:
            off3 = pm.read_int(off2 + offsets["offset3"])
            if amount == 3:
                address = off2 + offsets["offset3"]
                return address
            else:
                off4 = pm.read_int(off3 + offsets["offset4"])
                if amount == 4:
                    address = off3 + offsets["offset4"]
                    return address
                else:
                    offsets["offset5"] = pm.read_int(offsets["offset4"] + offsets["offset5"])
                    if amount == 5:
                        address = off4 + offsets["offset5"]
                        return address
                    else:
                        offsets["offset6"] = pm.read_int(offsets["offset5"] + offsets["offset6"])
                        address = off5 + offsets["offset6"]
                        return address

imposter_address = FindAddress(0x0144BB70, 4, offset1 = 0x5C, offset2 = 0x0, offset3 = 0x34, offset4 = 0x28 , )
kill_address = FindAddress(0x0144BB70, 3, offset1 = 0x5C, offset2 = 0x0, offset3 = 0x44, )
speed_address = FindAddress(0x0144BB70, 3, offset1 = 0x5C, offset2 = 0x4, offset3 = 0x14, )
kill_distance = FindAddress(0x0144BB70, 3, offset1 = 0x5C, offset2 = 0x4, offset3 = 0x40,)
imposter_vision_add = FindAddress(0x0144A9D0, 3, offset1 = 0x5C, offset2 = 0x14, offset3 = 0x1C,)
crew_vision_add = FindAddress(0x01455658, 3, offset1 = 0x5C, offset2 = 0x24, offset3 = 0x18,)
current_speed_ = pm.read_int(speed_address)
crew_vision = pm.read_float(crew_vision_add)
imposter_vision = pm.read_float(imposter_vision_add)

current_speed = pm.read_float(speed_address)
imposter_status = pm.read_int(imposter_address)

kill_bot = False


def FlashMap():
    keyboard.press('tab')
    keyboard.release('tab')
    time.sleep(0.035)
    keyboard.press('tab')
    keyboard.release('tab')

def menu():
    subprocess.call('color 0A', shell=True)
    subprocess.call('cls', shell=True)
    print('###############################################################################################################')
    print('#                                                                                                             #')
    print('#                                               WARNING !!!!!!!                                               #')
    print('#       IF YOU WERE NOT THE ORIGINAL IMPOSTER AND HAVE IT TOGGLED DURING THE VOTE IT CAN CRASH THE GAME       #')
    print('#                                                                                                             #')
    print('#                                                                                                             #')
    print('###############################################################################################################')
    print('\nPress "ctrl" and "q" to toggle auto kill\nPress "ins" to toggle imposter.\nPage up and page down to increase or decrease speed\nPress "Ctrl" and "g" to become a ghost\nPress "end" to exit')
    print(f'\n\nCurrent speed: {current_speed}\n')
    if imposter_status == 0:
        print('Current status: Crew ')
    elif imposter_status == 1:
        print('Current status: Imposter ')
    elif imposter_status == 256:
        print('Current status: g..g..g..ghosttt (crew)')
    else:
        print('Current status: g..g..g..ghosttt (imposter)')
    if kill_bot == False:
        print('\nauto kill: off')
    else:
        print('\nauto kill: on')


# keyboard.press('a')
# keyboard.release('a')


menu()

speed_change = 1.0

while True:

    if keyboard.is_pressed('end'):
        quit()

    kill_countdown = pm.read_int(kill_address)
    imposter_status = pm.read_int(imposter_address)
    current_speed = pm.read_float(speed_address)
    kill_dist = pm.read_int(kill_distance)
    crew_vision = pm.read_float(crew_vision_add)
    imposter_vision = pm.read_float(imposter_vision_add)

    if keyboard.is_pressed('ctrl') and keyboard.is_pressed('q'):
        if kill_bot == True:
            kill_bot = False
            menu()
        else:
            kill_bot = True
            menu()


    if kill_bot:
        keyboard.press('q')
        time.sleep(0.01)
        keyboard.release('q')




    if crew_vision != 99.9:
        pm.write_float(crew_vision_add, 99.9)


    if imposter_vision != 99.9:
        pm.write_float(imposter_vision_add, 99.9)

    if kill_countdown != 0:
        pm.write_int(kill_address, 0)

    if kill_dist != 2:
        pm.write_int(kill_distance, 2)

    if keyboard.is_pressed('Ctrl') and keyboard.is_pressed('g'):
        time.sleep(.15)

        if imposter_status == 256:
            pm.write_int(imposter_address, 0)
            imposter_status = pm.read_int(imposter_address)
            menu()
        elif imposter_status == 0 :
            pm.write_int(imposter_address, 256)
            imposter_status = pm.read_int(imposter_address)
            menu()
        elif imposter_status == 1 :
            pm.write_int(imposter_address, 257)
            imposter_status = pm.read_int(imposter_address)
            menu()
        else:
            pm.write_int(imposter_address, 1)
            imposter_status = pm.read_int(imposter_address)
            menu()

    # ins toggles imposter
    if keyboard.is_pressed('ins'):
        time.sleep(.15)

        if imposter_status == 1:
            pm.write_int(imposter_address , 0)
            imposter_status = pm.read_int(imposter_address)
            pm.write_float(imposter_vision_add, 99.9)
            FlashMap()
            menu()
            #print('You are not the imposter')

        else:
            pm.write_int(imposter_address , 1)
            imposter_status = pm.read_int(imposter_address)
            FlashMap()
            menu()


    if current_speed != speed_change:
        pm.write_float(speed_address, speed_change)


    if keyboard.is_pressed('PgUP'):
        time.sleep(.15)
        speed_change += 0.5
        pm.write_float(speed_address, speed_change)
        menu()


    elif keyboard.is_pressed('pagedown'):
        time.sleep(.15)
        speed_change -= 0.5
        pm.write_float(speed_address, speed_change)
        current_speed = pm.read_float(speed_address)
        menu()
