import app
from faker import Faker
from app.db_models import Tweet
from sqlalchemy.exc import IntegrityError
from app.config import config
from app.db_manager import Manager


class Fake(object):

    # session = Manager.Session()
    def __init__(self):
        manager = Manager()
        self.session = manager.Session()

    def tweet(self, count=1):
        fake = Faker()
        i = 0
        while i < count:
            t = Tweet(user_name=fake.name(),
                      latitude=1.111111,
                      longitude=-2.222222,
                      tweet=fake.text(),
                      sentiment=2,
                      )
            self.session.add(t)
            try:
                self.session.commit()
                i += 1
            except IntegrityError:
                self.session.rollback()


if __name__ == '__main__':
    generator = Fake()
    generator.tweet(5)

    print('-- DONE --')

