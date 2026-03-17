from . import db

class Property(db.Model):

    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    desc = db.Column(db.String(500))
    numBaths = db.Column(db.Integer)
    numRooms = db.Column(db.Integer)
    ptype = db.Column(db.String(30))
    price = db.Column(db.Integer)
    filename = db.Column(db.String(250))
    location = db.Column(db.String(150))

    def __init__(self, title, desc, numBaths, numRooms, ptype, price, location, filename):
        self.title = title
        self.desc = desc
        self.numBaths = numBaths
        self.numRooms = numRooms
        self.ptype = ptype
        self.price = price
        self.location = location
        self.filename = filename

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '< %r>' % (self.title)