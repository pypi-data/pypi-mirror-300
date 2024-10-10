from chainalysis.orm import Orm
from chainalysis.sql import Sql
from chainalysis.utils import Utils


class DataSolutionsClient:
    """
    This class provides SDK functions for users to query
    Data Solutions databases.

    Note this class should be imported using the following:

    .. code-block:: python

            from chainalysis import DataSolutionsClient

    The below import is still valid but deprecated:

    .. code-block:: python

            from chainalysis.data_solutions import DataSolutionsClient

    :ivar sql: The SQL class for querying Data Solutions tables using SQL queries.
    :vartype sql: Sql
    :ivar orm: The ORM class for querying Data Solutions tables using Ordinal Relational Mapping.
    :vartype orm: Orm
    :ivar utils: The Utils class for utility functions.
    :vartype utils: Utils
    """

    def __init__(
        self,
        api_key: str,
    ):
        """
        Initialize the DataSolutionsClient class.

        :param api_key: The API key for the Data Solutions API
        :type api_key: str
        """
        self.api_key = api_key

        self.sql = Sql(self.api_key)

        self.orm = Orm(self.api_key)

        self.utils = Utils()
