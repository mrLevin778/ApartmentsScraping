from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, DateTime, create_engine

class Apartment():

    __tablename__ = 'apartment'
    __tableargs__ = {
        'comment': 'Apartments from site'
    }
    apartment_id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    imageURL = Column(Text, comment='')
    price = Column(Text, comment='')
    description = Column(Text, comment='')
    title = Column(Text, comment='')
    date = Column(Text, comment='')
    bedrooms = Column(Text, comment='')
    location = Column(Text, comment='')

    def __repr__(self):
        return f'{self.apartment_id} ' \
               f'{self.imageURL} ' \
               f'{self.price} ' \
               f'{self.description} ' \
               f'{self.title} ' \
               f'{self.date} ' \
               f'{self.bedrooms} ' \
               f'{self.location}'