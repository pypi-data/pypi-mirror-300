import multiprocessing
import pygame
from shared_memory_dict import SharedMemoryDict



import pickle
import os


path = os.path.realpath(__file__)
path = path.replace('functions.py', '')


def put_rgbcolor(color):
    file = open((os.path.join(path, "hmrgb")), 'wb')
    pickle.dump(color, file)
    file.close()


def get_rgbcolor():
    try:
        file = open((os.path.join(path, "hmrgb")), 'rb')
        q = pickle.load(file)
        file.close()
        if q != False:
            clear_pickle("hmrgb", False)
            return q
        else:
            return False
    except:
        return False


def get_path():
    return path


def screenshot_refresh():
    try:
        file = open((os.path.join(path, "hmscreen")), 'rb')
        q = pickle.load(file)
        file.close()
        if q != False:
            clear_pickle("hmscreen", False)
            return True
        else:
            return False
    except:
        return False


def take_screenshot_parallel(screen):
    def create_screenshot(screen):
        try:
            os.remove(os.path.join(path, "screencapture.jpg"))
        except:
            pass
        pygame.image.save(screen, os.path.join(path, "screencapture.jpg"))
        file = open((os.path.join(path, "hmscreen")), 'wb')
        pickle.dump(True, file)
        file.close()

    t = multiprocessing.Process(target=create_screenshot, args=(screen,))
    t.start()
    # t.join()


def take_screenshot(screen):
    try:
        os.remove(os.path.join(path, "screencapture.jpg"))
    except:
        True
    pygame.image.save(screen, os.path.join(path, "screencapture.jpg"))
    file = open((os.path.join(path, "hmscreen")), 'wb')
    pickle.dump(True, file)
    file.close()


# def game_isactive():
#     try:
#         file = open((os.path.join(path, "hmsys")), 'rb')
#         q = pickle.load(file)
#         file.close()
#         if q != True:
#             clear_pickle("hmsys", True)
#             return False
#         else:
#             return True
#     except:
#         return True
#
#
# def close_pygame():
#     file = open((os.path.join(path, "hmsys")), 'wb')
#     pickle.dump(False, file)
#     file.close()





def create_shared_memory():
    smd = SharedMemoryDict(name='data', size=1024)
    smd["Active"] = False
    smd["Hit"]= False
    smd["Pos"] = False
    smd["Players"] = False
    smd["Screen"] = False
    smd["RGB"] = False
    smd["Temp"] = False
    smd["Action"] = False
    smd["Buttons"] = False



def game_isactive():
    smd = SharedMemoryDict(name='data', size=1024)
    try:
        return smd["Active"]
    except:
        return True



def close_game():
    smd = SharedMemoryDict(name='data', size=1024)
    smd["Active"]=False

def open_game():
    smd = SharedMemoryDict(name='data', size=1024)
    smd["Active"] = True

def check_ifdebug():
    import io
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return False
    except Exception: pass
    return True



def clear_pickle(filename, val):
    file = open((os.path.join(path, filename)), 'wb')
    pickle.dump(val, file)
    file.close()





def put_pos(pos):
    smd = SharedMemoryDict(name='data', size=1024)
    smd["Pos"]=pos


def get_size():
    return (1360, 768)


def get_pos():
    smd = SharedMemoryDict(name='data', size=1024)
    return smd["Pos"]


def put_temp(temp):
    smd = SharedMemoryDict(name='data', size=1024)
    smd["Temp"]=temp


def get_temp():
    smd = SharedMemoryDict(name='data', size=1024)
    return smd["Temp"]


def put_button_names(names):
    smd = SharedMemoryDict(name='data', size=1024)
    smd["Buttons"]=names


def get_button_names():
    smd = SharedMemoryDict(name='data', size=1024)
    return smd["Buttons"]


def put_hit():
    smd = SharedMemoryDict(name='data', size=1024)
    smd["Hit"]=True


def hit_detected():
    smd = SharedMemoryDict(name='data', size=1024)
    try:
        if smd["Hit"]==True:
            smd["Hit"] = False
            return True
        else:
            return False
    except:
        return False


def get_action():
    smd = SharedMemoryDict(name='data', size=1024)
    try:
        action=smd["Action"]
        smd["Action"]=False
        return action
    except:
        return False


def put_action(number):
    smd = SharedMemoryDict(name='data', size=1024)
    smd["Action"]=number

def put_playernames(playernames):
    file = open((os.path.join(path, "hmplayers")), 'wb')
    pickle.dump(playernames, file)
    file.close()


def get_playerstatus():
    try:
        file = open((os.path.join(path, "hmplayers")), 'rb')
        q = pickle.load(file)
        file.close()
        if q != False:
            return q
        else:
            return False
    except:
        return False

def get_playernames():
    try:
        file = open((os.path.join(path, "hmplayers")), 'rb')
        q = pickle.load(file)
        file.close()
        if q != False:
            w = []
            for i in range(0, len(q)):
                if q[i][1] == True:
                    w.append(q[i][0])
            return w
        else:
            return False
    except:
        return False


def clear_all():
    clear_pickle("hmplayers", False)
    clear_pickle("hmscreen", False)
    clear_pickle("hmrgb", False)


