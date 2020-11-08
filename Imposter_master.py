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


imposter_address = Module(pm,"GameAssembly.dll",0x0144BB70,[0x5C, 0x0, 0x34,])
kill_address = Module(pm,"GameAssembly.dll",0x0144BB70,[0x5C, 0x0,])
speed_address = Module(pm,"GameAssembly.dll",0x0144BB70,[0x5C, 0x4,])
kill_distance = Module(pm,"GameAssembly.dll",0x0144BB70,[0x5C, 0x4,])
imposter_vision_add = Module(pm,"GameAssembly.dll",0x0144A9D0,[0x5C, 0x14,])
crew_vision_add = Module(pm,"GameAssembly.dll",0x01455658,[0x5C, 0x24,])

kill_countdown = pm.read_int(kill_address + 0x44)
current_speed = pm.read_float(speed_address + 0x14)
crew_vision = pm.read_float(crew_vision_add + 0x18)
imposter_vision = pm.read_float(imposter_vision_add + 0x1C)
imposter_status = pm.read_int(imposter_address + 0x28)
kill_dist = pm.read_int(kill_distance + 0x40)



#def Main():

speed_change = 1.0
kill_bot = False
Menu()



while True:
    if keyboard.is_pressed('end'):
        quit()

    kill_countdown = pm.read_int(kill_address + 0x44)
    current_speed = pm.read_float(speed_address + 0x14)
    crew_vision = pm.read_float(crew_vision_add + 0x18)
    imposter_vision = pm.read_float(imposter_vision_add + 0x1C)
    imposter_status = pm.read_int(imposter_address + 0x28)
    kill_dist = pm.read_int(kill_distance + 0x40)

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
        pm.write_float(crew_vision_add + 0x18, 99.9)

    if imposter_vision != 99.9:
        pm.write_float(imposter_vision_add + 0x1C, 99.9)

    if kill_countdown != 0:
        pm.write_int(kill_address + 0x44, 0)

    if kill_dist != 2:
        pm.write_int(kill_distance + 0x40, 2)

    if keyboard.is_pressed('Ctrl') and keyboard.is_pressed('g'):
        time.sleep(.15)

        if imposter_status == 256:
            pm.write_int(imposter_address + 0x28, 0)
            imposter_status = pm.read_int(imposter_address + 0x28)
            Menu()
        elif imposter_status == 0 :
            pm.write_int(imposter_address + 0x28, 256)
            imposter_status = pm.read_int(imposter_address + 0x28)
            Menu()
        elif imposter_status == 1 :
            pm.write_int(imposter_address + 0x28, 257)
            imposter_status = pm.read_int(imposter_address + 0x28)
            Menu()
        else:
            pm.write_int(imposter_address + 0x28, 1)
            imposter_status = pm.read_int(imposter_address + 0x28)
            Menu()

    # ins toggles imposter
    if keyboard.is_pressed('ins'):
        time.sleep(.15)

        if imposter_status == 1:
            pm.write_int(imposter_address + 0x28 , 0)
            imposter_status = pm.read_int(imposter_address + 0x28)
            pm.write_float(imposter_vision_add + 0x1C, 99.9)
            FlashMap()
            Menu()
            #print('You are not the imposter')

        else:
            pm.write_int(imposter_address + 0x28 , 1)
            imposter_status = pm.read_int(imposter_address + 0x28)
            FlashMap()
            Menu()

    if current_speed != speed_change:
        pm.write_float(speed_address + 0x14, speed_change)

    if keyboard.is_pressed('PgUP'):
        time.sleep(.15)
        speed_change += 0.5
        pm.write_float(speed_address + 0x14, speed_change)
        current_speed = pm.read_float(speed_address + 0x14)
        Menu()
    elif keyboard.is_pressed('pagedown'):
        time.sleep(.15)
        speed_change -= 0.5
        pm.write_float(speed_address + 0x14, speed_change)
        current_speed = pm.read_float(speed_address + 0x14)
        Menu()

#if __name__ == "__main__":
#    Main()
#    Menu()
