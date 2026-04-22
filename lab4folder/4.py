from datetime import datetime
import random
import os
# ЗАДАЧА 3 — Класс Item (List, Set, OOP)
class Item:
    def __init__(self, id: int, name: str, power: int):
        self.id = id
        self.name = name.strip().title()
        self.power = power
    def __str__(self):
        return f"Item(id={self.id}, name='{self.name}', power={self.power})"
    def __repr__(self):
        return self.__str__()
    # Задача 3: __hash__ и __eq__ для использования в set
    def __hash__(self):
        return hash(self.id)
    def __eq__(self, other):
        if isinstance(other, Item):
            return self.id == other.id
        return False
# ЗАДАЧА 4 — Inventory (List, Dict, Set)
# ЗАДАЧА 5 — Фильтрация предметов (Lambda, Comprehension)
# ЗАДАЧА 18 — Итератор по предметам (Iterator + Comprehension)
class Inventory:
    def __init__(self):
        self._items: list[Item] = []
    # Задача 4
    def add_item(self, item: Item):
        """Добавить предмет (без дубликатов по id)."""
        if item.id not in {i.id for i in self._items}:
            self._items.append(item)
    def remove_item(self, item_id: int):
        """Удалить предмет по id."""
        self._items = [i for i in self._items if i.id != item_id]
    def get_items(self) -> list[Item]:
        return list(self._items)
    def unique_items(self) -> set[Item]:
        return set(self._items)
    def to_dict(self) -> dict[int, Item]:
        return {item.id: item for item in self._items}
    # Задача 5: list comprehension + lambda
    def get_strong_items(self, min_power: int) -> list[Item]:
        is_strong = lambda item: item.power >= min_power
        return [item for item in self._items if is_strong(item)]
    # Задача 18: итерация по инвентарю
    def __iter__(self):
        return iter(self._items)
    def __len__(self):
        return len(self._items)
    def __str__(self):
        return f"Inventory({[str(i) for i in self._items]})"
# ЗАДАЧА 6 — Класс Event (String, Dict, OOP)
VALID_EVENT_TYPES = {"ATTACK", "HEAL", "LOOT"}
class Event:
    def __init__(self, type: str, data: dict, timestamp: datetime = None):
        if type not in VALID_EVENT_TYPES:
            raise ValueError(f"Неверный тип события: {type}. Допустимые: {VALID_EVENT_TYPES}")
        self.type = type
        self.data = data
        self.timestamp = timestamp or datetime.now()
    def __str__(self):
        ts = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"Event(type='{self.type}', data={self.data}, timestamp='{ts}')"
    def __repr__(self):
        return self.__str__()
# ЗАДАЧА 1 — Класс Player (String, ООП, Инкапсуляция, Деструктор)
# ЗАДАЧА 2 — Фабричный метод Player (from_string)
# ЗАДАЧА 7 — Обработка событий (handle_event)
# ЗАДАЧА 16 — Приватные атрибуты (Инкапсуляция)
# ЗАДАЧА 17 — Деструктор объектов
class Player:
    def __init__(self, id: int, name: str, hp: int):
        self._id = id
        self._name = name.strip().title()      # Задача 1: strip + Title Case
        self._hp = max(0, hp)                   # Задача 1: hp >= 0
        self._inventory = Inventory()           # Задача 16: приватный инвентарь
    # Задача 16: @property для доступа к _hp и _inventory
    @property
    def id(self):
        return self._id
    @property
    def name(self):
        return self._name
    @property
    def hp(self):
        return self._hp
    @hp.setter
    def hp(self, value):
        self._hp = max(0, value)
    @property
    def inventory(self):
        return self._inventory
    # Задача 1: __str__
    def __str__(self):
        return f"Player(id={self._id}, name='{self._name}', hp={self._hp})"
    def __repr__(self):
        return self.__str__()
    # Задача 17: деструктор
    def __del__(self):
        print(f"Player {self._name} удалён")
    # Задача 2: фабричный метод
    @classmethod
    def from_string(cls, data: str):
        """Парсинг строки формата 'id,name,hp'."""
        try:
            parts = [p.strip() for p in data.split(",")]
            if len(parts) != 3:
                raise ValueError
            id_ = int(parts[0])
            name = parts[1]
            hp = int(parts[2])
            return cls(id_, name, hp)
        except (ValueError, IndexError):
            raise ValueError(f"Неверный формат строки: '{data}'. Ожидается 'id,name,hp'")
    # Задача 7: обработка событий
    def handle_event(self, event: Event):
        damage = self._calc_damage(event.data.get("damage", 0))
        if event.type == "ATTACK":
            self.hp -= damage
        elif event.type == "HEAL":
            heal = event.data.get("heal", 0)
            self.hp += heal
        elif event.type == "LOOT":
            item_data = event.data.get("item")
            if item_data:
                item = self._process_loot_item(item_data)
                self._inventory.add_item(item)
    def _calc_damage(self, damage: int) -> int:
        """Внутренний метод расчёта урона (переопределяется в подклассах)."""
        return damage
    def _process_loot_item(self, item: Item) -> Item:
        """Внутренний метод обработки найденного предмета (переопределяется в Mage)."""
        return item
# ЗАДАЧА 15 — Подклассы Warrior и Mage
# (также охватывает Задачу 7 для подклассов)
class Warrior(Player):
    """Warrior уменьшает входящий урон на 10%."""
    def _calc_damage(self, damage: int) -> int:
        return int(damage * 0.9)  # -10% урона
    def __str__(self):
        return f"Warrior(id={self._id}, name='{self._name}', hp={self._hp})"
class Mage(Player):
    """Mage усиливает предмет на 10% при LOOT."""
    def _process_loot_item(self, item: Item) -> Item:
        boosted = Item(item.id, item.name, int(item.power * 1.1))
        return boosted
    def __str__(self):
        return f"Mage(id={self._id}, name='{self._name}', hp={self._hp})"
# ЗАДАЧА 8 — Logger (запись в файл)
# ЗАДАЧА 9 — Чтение логов (чтение файла)
class Logger:
    # Задача 8: запись лога
    @staticmethod
    def log(event: Event, player: Player, filename: str):
        """Запись события в файл формата: timestamp;player_id;event_type;data"""
        ts = event.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        line = f"{ts};{player.id};{event.type};{event.data}\n"
        with open(filename, "a", encoding="utf-8") as f:
            f.write(line)
    # Задача 9: чтение логов
    @staticmethod
    def read_logs(filename: str) -> list[Event]:
        """Чтение файла и преобразование строк в объекты Event."""
        events = []
        if not os.path.exists(filename):
            return events
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    parts = line.split(";", 3)
                    ts_str, player_id, event_type, data_str = parts
                    timestamp = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
                    data = eval(data_str)  # данные хранятся как repr словаря
                    event = Event(event_type, data, timestamp)
                    events.append(event)
                except Exception:
                    continue  # пропустить повреждённую строку
        return events
# ЗАДАЧА 10 — Итератор событий (Iterator)
class EventIterator:
    def __init__(self, events: list[Event]):
        self._events = events
        self._index = 0
    def __iter__(self):
        return self
    def __next__(self) -> Event:
        if self._index >= len(self._events):
            raise StopIteration
        event = self._events[self._index]
        self._index += 1
        return event
# ЗАДАЧА 11 — Генератор урона (Generator)
def damage_stream(events: list[Event]):
    """Генератор: yield значения урона только из ATTACK-событий."""
    for event in events:
        if event.type == "ATTACK":
            yield event.data.get("damage", 0)
# ЗАДАЧА 12 — Симуляция событий (List, Lambda)
def generate_events(players: list[Player], items: list[Item], n: int) -> list[Event]:
    """Создаёт n случайных событий для каждого игрока."""
    event_types = ["ATTACK", "HEAL", "LOOT"]
    # Lambda выбирает тип события случайно
    pick_type = lambda: random.choice(event_types)
    events=[]
    for player in players:
        for _ in range(n):
            etype=pick_type()
            if etype == "ATTACK":
                data={"damage": random.randint(3,30), "player._id": player._id}
            elif etype=="HEAL":
                data={"heal": random.randint(4,30), "player._id": player._id}
            else:
                data={"item": random.choice(items), "player._id": player._id}
            events.append(Event(etype, data))
    return events
# ЗАДАЧА 13 — Аналитика логов (Dict, Comprehension)
def analyze_logs(events: list[Event]) -> dict:
    """
    Возвращает словарь с:
      - total_damage
      - top_player (id игрока с наибольшим уроном)
      - most_common_event
    """
    attack_events = [e for e in events if e.type == "ATTACK"]
    # total_damage через генератор урона
    total_damage = sum(damage_stream(events))
    # урон по игрокам: {player_id: total_damage}
    damage_by_player = {}
    for e in attack_events:
        pid = e.data.get("player_id")
        dmg = e.data.get("damage", 0)
        damage_by_player[pid] = damage_by_player.get(pid, 0) + dmg
    top_player = max(damage_by_player, key=lambda k: damage_by_player[k]) if damage_by_player else None
    # подсчёт частоты типов событий через comprehension
    type_counts = {t: sum(1 for e in events if e.type == t) for t in VALID_EVENT_TYPES}
    most_common_event = max(type_counts, key=lambda k: type_counts[k]) if type_counts else None
    return {
        "total_damage": total_damage,
        "top_player": top_player,
        "most_common_event": most_common_event,
        "damage_by_player": damage_by_player,
        "type_counts": type_counts,
    }
# ЗАДАЧА 14 — Lambda
decide_action = lambda player: (
    "HEAL"   if player.hp < 40 else
    "LOOT"   if len(player.inventory) == 0 else
    "ATTACK"
)
# ЗАДАЧА 19 — Файловая аналитика предметов (Dict, Set)
def analyze_inventory(inventories: list[Inventory]) -> dict:
    """
    Возвращает словарь:
      - unique_items: set уникальных предметов (по всем инвентарям)
      - top_power: предмет с наибольшей силой
    """
    all_items = [item for inv in inventories for item in inv]
    unique = set(all_items)
    top_item = max(all_items, key=lambda i: i.power) if all_items else None
    return {
        "unique_items": unique,
        "top_power": top_item,
    }
# ЗАДАЧА 20 — Финальная симуляция (main)
def main():
    print("=" * 60)
    print("Финальная симуляция")
    print("=" * 60)
    #  Создание предметов
    items = [
        Item(1, " Sword ",   50),
        Item(2, " Shield",   30),
        Item(3, "fire staff", 80),
        Item(4, "Dagger",    40),
        Item(5, "healing potion", 20),
    ]
    print("\n[Предметы]")
    for item in items:
        print(" ", item)
    #Создание игроков
    p1 = Player.from_string("1, alice , 100")
    p2 = Warrior(2, " bob ", 120)
    p3 = Mage(3, "charlie", 90)
    players = [p1, p2, p3]
    print("\n[Игроки]")
    for p in players:
        print(" ", p)
    # ── Задача 18: Comprehension по инвентарю (пока пустому) ───
    # Добавим начальный предмет p1 вручную
    p1.inventory.add_item(items[0])
    strong_for_p1 = [str(i) for i in p1.inventory if i.power >= 40]
    print(f"\n[Сильные предметы p1 (power>=40)]: {strong_for_p1}")
    #Генерация событий
    print("\n[Генерация событий — 3 на игрока]")
    events = generate_events(players, items, n=3)
    for e in events:
        print(" ", e)
    #  Задача 10: Итератор событий
    print("\n[Итератор EventIterator — первые 3]")
    ei = EventIterator(events)
    for _ in range(3):
        print(" ", next(ei))
    #Задача 11: Генератор урона
    total_dmg = sum(damage_stream(events))
    print(f"\n[Генератор урона] Суммарный урон из событий: {total_dmg}")
    #Задача 14
    print("\n[действия для каждого игрока]")
    for p in players:
        action = decide_action(p)
        print(f"  {p.name} (hp={p.hp}, items={len(p.inventory)}) → {action}")
    #Обработка событий игроками
    print("\n[Обработка событий]")
    logger = Logger()
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game_log.txt")
    # Очистить старый лог
    if os.path.exists(log_file):
        os.remove(log_file)
    for event in events:
        pid = event.data.get("player_id")
        player = next((p for p in players if p.id == pid), None)
        if player:
            player.handle_event(event)
            logger.log(event, player, log_file)
    print("  Состояние игроков после событий:")
    for p in players:
        items_in_inv = [i.name for i in p.inventory]
        print(f"  {p} | Инвентарь: {items_in_inv}")
    #Чтение логов
    print("\n[Чтение логов из файла]")
    logged_events = logger.read_logs(log_file)
    print(f"  Прочитано событий: {len(logged_events)}")
    #Задача 13 Аналитика
    # Для аналитики используем все сгенерированные события
    analytics = analyze_logs(events)
    print("\n[Аналитика событий]")
    print(f"  Суммарный урон:       {analytics['total_damage']}")
    print(f"  Топ игрок по урону:   Player id={analytics['top_player']}")
    print(f"  Самый частый тип:     {analytics['most_common_event']}")
    print(f"  Урон по игрокам:      {analytics['damage_by_player']}")
    print(f"  Типы событий:         {analytics['type_counts']}")
    #Задача 19: Аналитика предметов
    inv_analytics = analyze_inventory([p.inventory for p in players])
    print("\n[Аналитика инвентарей]")
    print(f"  Уникальных предметов: {len(inv_analytics['unique_items'])}")
    print(f"  Сильнейший предмет:   {inv_analytics['top_power']}")
    # Статистика предметов по игрокам
    max_items_player = max(players, key=lambda p: len(p.inventory))
    print(f"\n[Игрок с наибольшим количеством предметов]")
    print(f"  {max_items_player} — {len(max_items_player.inventory)} предметов")
    print("\n" + "=" * 60)
    print("  Симуляция завершена.")
    print("=" * 60)
if __name__ == "__main__":
    main()

