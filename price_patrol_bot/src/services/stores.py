import enum


class Stores(enum.Enum, int):
    WILDBERRIES = 1
    # MEGAMARKET = 2
    # OZON = 3
    # YANDEX = 4


STORE_NAMES = {
    Stores.WILDBERRIES: "Wildberries",
    # Stores.MEGAMARKET: "Мегамаркет",
    # Stores.OZON: "Ozon",
    # Stores.YANDEX: "ЯндексМаркет",
}
