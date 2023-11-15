import threading
import json
import time

def bot_clerk(items):

    inventory = read_inventory()
    cart = []
    lock = threading.Lock()


    robot_fetcher_lists = [[], 
                           [],
                           []]      #list 1-3


    for i, item in enumerate(items):
        robot_fetcher_lists[i % 3].append([item, inventory[item][0], inventory[item][1]])

    threads = [threading.Thread(target=bot_fetcher, args=(fetcher_list, cart, lock)) for fetcher_list in robot_fetcher_lists]


    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return cart



def bot_fetcher(item_list, cart, lock):
    for item in item_list:
        _, item_name, seconds = item
        time.sleep(seconds)
        
        with lock:
            cart.append([item[0], item_name])



def read_inventory(file_path='inventory.dat'):
    with open(file_path, 'r') as file:
        inventory_data = json.load(file)
    return inventory_data