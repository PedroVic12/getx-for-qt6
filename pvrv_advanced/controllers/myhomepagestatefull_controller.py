from models.myhomepagestatefull_model import MyhomepagestatefullModel

class MyhomepagestatefullController:
    """
    Controller for myhomepagestatefull page
    """

    def __init__(self, model=None):
        self.model = model or MyhomepagestatefullModel

    def get_title(self):
        return "Myhomepagestatefull"
