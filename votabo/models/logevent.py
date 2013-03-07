from votabo.models.meta import *


class LogEvent(Base):
    __tablename__ = "score_log"
    id = Column(Integer, primary_key=True, nullable=False)
    timestamp = Column("date_sent", DateTime(timezone=True), nullable=False, default=func.now())
    section = Column(String, nullable=False)
    username = Column(String, nullable=False)
    #address = Column(postgresql.INET, nullable=False)
    address = Column(String(255), nullable=False)
    priority = Column(Integer, nullable=False)
    message = Column(Unicode, nullable=False)
