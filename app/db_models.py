from sqlalchemy import Column, Integer, Text, DECIMAL
from app.db_manager import Manager


class Tweet(Manager.Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(Text, nullable=False)
    latitude = Column(DECIMAL(precision=10, scale=6), nullable=False)
    longitude = Column(DECIMAL(precision=10, scale=6), nullable=False)
    tweet = Column(Text, nullable=False)
    sentiment = Column(Integer, nullable=False)
   
    def __repr__(self):
        # return '<Id: %d # Name: %r # Point: %s # Senti: %d # Tweet: %s>' % (self.id, self.user_name, self.coordinate, self.sentiment, self.tweet)
        return '<Id: %d # Name: %r # Senti: %d # Tweet: %s>' % (self.id, self.user_name, self.sentiment, self.tweet)


