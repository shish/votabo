from sqlalchemy import (
    Table,
    Column,
    ForeignKey,

    Integer,
    Text,
    String,
    Unicode,
    DateTime,
    Boolean,

    func,
    desc,
    )
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

import logging
from hashlib import md5

logger = logging.getLogger(__name__)


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

