from observer.observer import Observer

class Subject:
    def __init__(self):
        self._observers: list[Observer] = []

    def attach(self, obs: Observer):
        self._observers.append(obs)

    def detach(self, obs: Observer):
        self._observers.remove(obs)

    def notify_observers(self, order, event: str):
        for obs in self._observers:
            obs.update(order, event)