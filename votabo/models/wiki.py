from votabo.models.meta import *


class WikiPage(Base):
    __tablename__ = "wiki_pages"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column("owner_id", Integer, ForeignKey("users.id"), nullable=False)
    #user_ip = Column("owner_ip", postgresql.INET, nullable=False)
    user_ip = Column("owner_ip", String(255), nullable=False)
    title = Column(Unicode, nullable=False)
    body = Column(Unicode, nullable=False)
    revision = Column(Integer, nullable=False)
    posted = Column("date", DateTime, nullable=False)
    locked = Column(Boolean, nullable=False)

    user = relationship("User")
