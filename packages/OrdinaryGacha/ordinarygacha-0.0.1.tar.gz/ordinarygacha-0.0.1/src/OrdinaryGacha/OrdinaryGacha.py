import random

class Gacha:
    def __init__(self):
        self.items = {}

    def show(self):
        [print(f'ชื่อไอเทม: {name}, อัตราการดรอป: {rate}') for name, rate in self.items.items()]

    def add(self, item_name, drop_rate):
        self.items[item_name] = drop_rate

    def remove(self, item_name):
        if item_name in self.items:
            del self.items[item_name]
            print(f'ลบ {item_name} สำเร็จ')
            return True
        else:
            print(f'ไม่มีไอเทม {item_name} ในกาชา')
            return False

    def random(self):
        if not self.items:
            return None
        item_names, drop_rates = zip(*self.items.items())
        return random.choices(item_names, weights=drop_rates, k=1)[0]
