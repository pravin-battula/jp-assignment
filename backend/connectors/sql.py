from contextlib import contextmanager
import functools

from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend.response import response

def get_engine():
    """Create engine based on config settings."""
    return create_engine('sqlite:////tmp/test.db')

db_engine = get_engine()
db_session_maker = sessionmaker(bind=db_engine)

base_model = declarative_base()


@contextmanager
def db_session():
    """Provide a transactional scope around a series of operations.

    Taken from http://docs.sqlalchemy.org/en/latest/orm/session_basics.html
    This handles rollback and closing of session, so there is no need
    to do that throughout the code.

    Usage:
        with db_session() as session:
            session.execute(query)
    """
    session = db_session_maker()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def wrap_db_errors(function):
    """Decorate the given function with logic to handle SQLAlchemy errors.

    If a SQLAlchemy exception is thrown, it will be caught and logged and the
    function will return a fatal response.

    Args:
        function (func): the function to decorate

    Returns:
        func: function decorated with error-handling logic
    """
    @functools.wraps(function)
    def call_function_with_error_handling(*args, **kwargs):
        try:
            function_return = function(*args, **kwargs)
        except exc.SQLAlchemyError as exception:
            return response.create_fatal_response()

        return function_return
    return call_function_with_error_handling
