import subprocess, pymem, keyboard, time

def dmaAddr(base, offsets): # CREDITS: BLUE
  addr = pm.read_int(base)
  for i in offsets:
    addr = pm.read_int(addr + i)
  return addr

def Module(handle, name, base, offsets): #CREDITS: JokinAce
    first = pymem.process.module_from_name(handle.process_handle, name).lpBaseOfDll + base
    last = dmaAddr(first,offsets)
    return last

def FlashMap():
    keyboard.press('tab')
    keyboard.release('tab')
    time.sleep(0.035)
    keyboard.press('tab')
    keyboard.release('tab')

def Menu():
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
    if not kill_bot:
        print('\nauto kill: off')
    else:
        print('\nauto kill: on')

pm = pymem.Pymem('Among Us.exe')
client = pymem.process.module_from_name(pm.process_handle, "GameAssembly.dll").lpBaseOfDll

imposter_address = Module(pm,"GameAssembly.dll",0x0144BB70,[0x5C, 0x0, 0x34, 0x28])
kill_address = Module(pm,"GameAssembly.dll",0x0144BB70,[0x5C, 0x0, 0x44])
speed_address = Module(pm,"GameAssembly.dll",0x0144BB70,[0x5C, 0x4, 0x14])
kill_distance = Module(pm,"GameAssembly.dll",0x0144BB70,[0x5C, 0x4, 0x40])
imposter_vision_add = Module(pm,"GameAssembly.dll",0x0144A9D0,[0x5C, 0x14, 0x1C])
crew_vision_add = Module(pm,"GameAssembly.dll",0x01455658,[0x5C, 0x24, 0x18])

current_speed_ = pm.read_int(speed_address)
crew_vision = pm.read_float(crew_vision_add)
imposter_vision = pm.read_float(imposter_vision_add)
current_speed = pm.read_float(speed_address)
imposter_status = pm.read_int(imposter_address)

kill_bot = False

def Main():
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
            if kill_bot:
                kill_bot = False
                Menu()
            else:
                kill_bot = True
                Menu()

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
                Menu()
            elif imposter_status == 0 :
                pm.write_int(imposter_address, 256)
                imposter_status = pm.read_int(imposter_address)
                Menu()
            elif imposter_status == 1 :
                pm.write_int(imposter_address, 257)
                imposter_status = pm.read_int(imposter_address)
                Menu()
            else:
                pm.write_int(imposter_address, 1)
                imposter_status = pm.read_int(imposter_address)
                Menu()

        # ins toggles imposter
        if keyboard.is_pressed('ins'):
            time.sleep(.15)

            if imposter_status == 1:
                pm.write_int(imposter_address , 0)
                imposter_status = pm.read_int(imposter_address)
                pm.write_float(imposter_vision_add, 99.9)
                FlashMap()
                Menu()
                #print('You are not the imposter')

            else:
                pm.write_int(imposter_address , 1)
                imposter_status = pm.read_int(imposter_address)
                FlashMap()
                Menu()

        if current_speed != speed_change:
            pm.write_float(speed_address, speed_change)

        if keyboard.is_pressed('PgUP'):
            time.sleep(.15)
            speed_change += 0.5
            pm.write_float(speed_address, speed_change)
            Menu()
        elif keyboard.is_pressed('pagedown'):
            time.sleep(.15)
            speed_change -= 0.5
            pm.write_float(speed_address, speed_change)
            current_speed = pm.read_float(speed_address)
            Menu()

if __name__ == "__main__":
    Menu()
    Main()
