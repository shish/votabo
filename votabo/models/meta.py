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
import sqlalchemy.types as types

from zope.sqlalchemy import ZopeTransactionExtension

import logging
from hashlib import md5

logger = logging.getLogger(__name__)


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class BooleanYN(types.TypeDecorator):
    '''Stores a boolean value as 'Y' or 'N',
    because mysql lacks native boolean...
    '''

    impl = types.Boolean

    def process_bind_param(self, value, dialect):
        return (u"Y" if value else u"N")

    def process_result_value(self, value, dialect):
        return (value == u"Y")
