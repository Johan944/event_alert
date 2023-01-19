import os
import sqlalchemy
from datetime import datetime


class SendNotification:
    def __init__(self):
        user = os.environ("ALERT_USER_DB")
        password = os.environ("ALERT_PASSWORD_DB")
        port = os.environ("ALERT_PORT_DB")
        db_name = os.environ("ALERT_NAME_DB")

        self._engine = sqlalchemy.create_engine(f"mysql+pymysql://{user}:{password}@localhost:{port}/{db_name}")
        metadata = sqlalchemy.MetaData(bind=self._engine)
        metadata.reflect(views=False)
        self._tables = metadata.tables

        self._connection = self._engine.connect()
    
    def send(self, url, email, prices, event_date):
        event_date = datetime.strptime(event_date, "%d-%m-%Y %H:%M")

        notification = self._tables["notification"]
        sqlalchemy.insert(notification.values(
            {
                "url": url,
                "email": email,
                "prices": prices,
                "event_date": event_date,
            }
        )).execute()

