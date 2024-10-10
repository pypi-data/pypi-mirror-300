from chainalysis.sql._analytical import AnalyticalQuery
from chainalysis.sql._transactional import TransactionalQuery


class Sql:
    """
    The SQL class is used to query Database tables using SQL queries.

    :ivar transactional_query: The TransactionalQuery object.
    :vartype transactional_query: TransactionalQuery
    :ivar analytical_query: The AnalyticalQuery object.
    :vartype analytical_query: AnalyticalQuery
    :ivar transactional: The TransactionalQuery object (To be depricated).
    :vartype transactional: TransactionalQuery
    :ivar analytical: The AnalyticalQuery object (To be depricated).
    :vartype analytical: AnalyticalQuery
    """

    def __init__(self, api_key: str):
        """
        Initialize the SQL class.

        :param api_key: The API key for the Data Solutions API
        :type api_key: str
        """
        self.transactional_query = TransactionalQuery(api_key)
        self.analytical_query = AnalyticalQuery(api_key)
        self.transactional = TransactionalQuery(api_key)
        self.analytical = AnalyticalQuery(api_key)
