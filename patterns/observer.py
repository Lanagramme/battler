class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, event, *args):
        for observer in self._observers:
            observer.update(event, *args)

class Observer:
    def update(self, event, *args):
        """Observers must implement this method to react to state changes."""
        raise NotImplementedError("Observer subclasses must implement 'update()'")
