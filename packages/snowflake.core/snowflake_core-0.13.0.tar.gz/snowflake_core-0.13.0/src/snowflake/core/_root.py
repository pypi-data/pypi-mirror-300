import logging
import os

from typing import TYPE_CHECKING, Optional, Union

from snowflake.connector import SnowflakeConnection
from snowflake.core._options import require_snowpark

from ._constants import (
    PLATFORM,
    PYTHON_VERSION,
)
from ._internal.snowapi_parameters import SnowApiParameters
from ._internal.telemetry import ApiTelemetryClient
from .account import AccountCollection
from .catalog_integration import CatalogIntegrationCollection
from .compute_pool import ComputePoolCollection
from .database import DatabaseCollection
from .external_volume import ExternalVolumeCollection
from .grant._grants import Grants
from .managed_account import ManagedAccountCollection
from .network_policy import NetworkPolicyCollection
from .notification_integration import NotificationIntegrationCollection
from .role import RoleCollection
from .session import SnowAPISession
from .user import UserCollection
from .version import __version__
from .warehouse import WarehouseCollection


if TYPE_CHECKING:
    from snowflake.snowpark import Session

logger = logging.getLogger(__name__)


class Root:
    """The entry point of the Snowflake Core Python APIs that manage the Snowflake objects.

    Parameters
    __________
    connection: Union[SnowflakeConnection, Session]
        A ``SnowflakeConnection`` or Snowpark ``Session`` instance.

    Examples
    ________
    Creating a ``Root`` instance:

    >>> from snowflake.connector import connect
    >>> from snowflake.core import Root
    >>> from snowflake.snowpark import Session
    >>> CONNECTION_PARAMETERS = {
    ...    "account": os.environ["snowflake_account_demo"],
    ...    "user": os.environ["snowflake_user_demo"],
    ...    "password": os.environ["snowflake_password_demo"],
    ...    "database": test_database,
    ...    "warehouse": test_warehouse,
    ...    "schema": test_schema,
    ... }
    >>> # create from a Snowflake Connection
    >>> connection = connect(**CONNECTION_PARAMETERS)
    >>> root = Root(connection)
    >>> # or create from a Snowpark Session
    >>> session = Session.builder.config(CONNECTION_PARAMETERS).create()
    >>> root = Root(session)

    Using the ``Root`` instance to access resource management APIs:

    >>> tasks = root.databases["mydb"].schemas["myschema"].tasks
    >>> mytask = tasks["mytask"]
    >>> mytask.resume()
    >>> compute_pools = root.compute_pools
    >>> my_computepool = compute_pools["mycomputepool"]
    >>> my_computepool.delete()
    """

    def __init__(
        self,
        connection: Union[SnowflakeConnection, "Session"],
    ) -> None:
        self._session: Optional[Session] = None
        if isinstance(connection, SnowflakeConnection):
            self._connection = connection
        else:
            self._session = connection
            self._connection = connection._conn._conn

        logger.info("New root object was created for %r", connection)

        self._snowapi_session = SnowAPISession(self)
        self._refresh_parameters()

        self._databases = DatabaseCollection(self)
        self._accounts = AccountCollection(self)
        self._managed_accounts = ManagedAccountCollection(self)
        self._compute_pools = ComputePoolCollection(self)
        self._external_volumes = ExternalVolumeCollection(self)
        self._telemetry_client = ApiTelemetryClient(self._connection)
        self._warehouses = WarehouseCollection(self)
        self._network_policies = NetworkPolicyCollection(self)
        self._roles = RoleCollection(self)
        self._grants = Grants(self)
        self._users = UserCollection(self)
        self._catalog_integrations = CatalogIntegrationCollection(self)
        self._notification_integrations = NotificationIntegrationCollection(self)
        logger.info("Snowflake Core version: %s, on Python %s, on platform: %s", __version__, PYTHON_VERSION, PLATFORM)
        parameter_map = self._parameters.params_map
        for parameter in parameter_map:
            logger.info("Parameter %s: %s", parameter, parameter_map.get(parameter))

    @property
    def parameters(self, refresh: bool = False) -> SnowApiParameters:
        if refresh:
            self._refresh_parameters()

        return self._parameters

    @property
    def connection(self) -> SnowflakeConnection:
        """Return the connection in use.

        This is the connection used to create this ``Root`` instance, or the
        Snowpark session's connection if this root is created from a
        session.
        """
        return self._connection

    @property
    def session(self) -> "Session":
        """Returns the session that is used to create this ``Root`` instance."""
        require_snowpark()
        if self._session is None:
            from snowflake.snowpark.session import Session, _active_sessions
            self._session = Session.builder.configs(
                {"connection": self._connection}
            ).create()
            _active_sessions.remove(
                self._session
            )  # This is supposed to avoid a user double using sessions
        return self._session

    @property
    def databases(self) -> DatabaseCollection:
        """Returns the ``DatabaseCollection`` that represents the visible databases.

        Examples
        ________

        Getting a specific database resource:

        >>> root = Root(session)
        >>> my_db = root.databases["my_db"]
        """
        return self._databases

    @property
    def accounts(self) -> AccountCollection:
        """Returns the ``AccountCollection`` that represents the visible accounts.

        Examples
        ________

        Getting a specific account resource:

        >>> root = Root(session)
        >>> my_account = root.accounts["my_account"]
        """
        return self._accounts

    @property
    def managed_accounts(self) -> ManagedAccountCollection:
        """Returns the ``ManagedAccountCollection`` that represents the visible accounts.

        Examples
        ________

        Getting a specific managed account resource:

        >>> root = Root(session)
        >>> my_managed_account = root.managed_accounts["my_managed_account"]
        """
        return self._managed_accounts

    @property
    def compute_pools(self) -> ComputePoolCollection:
        """Returns the ``ComputePoolCollection`` that represents the visible compute pools.

        Examples
        ________

        Getting a specific compute pool resource:

        >>> root = Root(session)
        >>> my_cp = root.compute_pools["my_cp"]
        """
        return self._compute_pools

    @property
    def external_volumes(self) -> ExternalVolumeCollection:
        """Returns the ``ExternalVolumeCollection`` that represents the visible external volumes.

        Examples
        ________

        Getting a specific external volume resource:

        >>> root = Root(session)
        >>> my_external_volume = root.external_volumes["my_external_volume"]
        """
        return self._external_volumes

    @property
    def network_policies(self) -> NetworkPolicyCollection:
        """Returns the ``NetworkPolicyCollection`` that represents the visible network policies.

        Examples
        ________

        Getting a specific network policy resource:

        >>> root = Root(session)
        >>> my_network_policy = root.network_policies["my_network_policy"]
        """
        return self._network_policies

    @property
    def notification_integrations(self) -> NotificationIntegrationCollection:
        """Returns the ``NotificationIntegrationCollection`` that represents the visible notification integrations.

        Examples
        ________

        Listing all available Notification Integrations:

        >>> root = Root(session)
        >>> my_nis = list(root.notification_integrations.iter())
        """
        return self._notification_integrations

    @property
    def warehouses(self) -> WarehouseCollection:
        """Returns the ``WarehouseCollection`` that represents the visible warehouses.

        Examples
        ________

        Getting a specific warehouse resource:

        >>> root = Root(session)
        >>> my_wh = root.warehouses["my_wh"]
        """
        return self._warehouses

    @property
    def roles(self) -> RoleCollection:
        """Returns the ``RoleCollection`` that represents the visible roles.

        Examples
        ________

        Getting a specific role resource:

        >>> root = Root(session)
        >>> my_role = root.roles["my_role"]
        """
        return self._roles

    @property
    def grants(self) -> Grants:
        """Returns the visible Grants in Snowflake.

        Examples
        ________

        Using the ``Grants`` object to grant a privilege to a role:

        >>> grants.grant(
        ...    Grant(
        ...        grantee=Grantees.role(name="public"),
        ...        securable=Securables.database("invaliddb123"),
        ...        privileges=[Privileges.create_database],
        ...        grant_option=False,
        ...    )
        ... )
        """
        return self._grants

    @property
    def users(self) -> UserCollection:
        """Returns the ``UserCollection`` that represents the visible users.

        Examples
        ________

        Getting a specific user resource:

        >>> root = Root(session)
        >>> my_user = root.users["my_user"]
        """
        return self._users


    @property
    def catalog_integrations(self) -> CatalogIntegrationCollection:
        """Returns the ``CatalogIntegrationCollection`` that represents the visible catalog integrations.

        Examples
        ________

        Getting a specific catalog integration resource:

        >>> root = Root(session)
        >>> my_catalog_integration = root.catalog_integrations["my_catalog_integration"]
        """
        return self._catalog_integrations

    @property
    def _session_token(self) -> Optional[str]:
        # TODO: this needs to be fixed in the connector
        return self._connection.rest.token  # type: ignore[union-attr]

    @property
    def _master_token(self) -> Optional[str]:
        # TODO: this needs to be fixed in the connector
        return self._connection.rest.master_token  # type: ignore[union-attr]

    def _refresh_parameters(self) -> None:
        parameters = {"PARAM_USE_CLIENT_RETRY": os.getenv("_SNOWFLAKE_ENABLE_RETRY_REQUEST_QUERY")}
        self._parameters = SnowApiParameters(parameters)
