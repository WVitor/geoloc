
class Feedback():
    def __init__(self):
        self.id= None
        self.feed= None

    def get_id(self):
        return self.id
    
    def set_id(self, id: int):
        self.id = id

    def get_feed(self):
        return self.feed
    
    def set_feed(self, feed):
        self.feed = feed
       