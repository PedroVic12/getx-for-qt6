from models.myhomepage_model import MyhomepageModel

class MyhomepageController:
    """
    Controller for myhomepage page
    """

    def __init__(self, model=None):
        self.model = model or MyhomepageModel

    def get_title(self):
        return "Myhomepage"
