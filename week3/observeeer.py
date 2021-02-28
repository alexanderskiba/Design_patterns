from abc import ABC, abstractmethod

class ObservableEngine(Engine):
    def __init__(self):
        self.__subscribers = set()

    def subscribe(self, subscriber):
        """Добавить подписчика"""
        self.__subscribers.add(subscriber)

    def unsubscribe(self, subscriber):
        """Удалить подписчика"""
        self.__subscribers.remove(subscriber)

    def notify(self, message):
        """Отправить уведомление все подписчикам,
        чтобы отправить им уведомление,
        необходимо у них вызвать метод update"""
        for subscriber in self.__subscribers:
            subscriber.update(message)

class AbstractObserver(ABC):
    @abstractmethod
    def update(self, message):
        pass

class ShortNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = set()

    def update(self, message):
        if message["title"] in self.achievements:
            pass
        else:
            self.achievements.add(message["title"])


class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = list()

    def update(self, message):
        if message in self.achievements:
            pass
        else:
            self.achievements.append(message)