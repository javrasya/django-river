from river.models.managers.rivermanager import RiverManager


class StateManager(RiverManager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)
