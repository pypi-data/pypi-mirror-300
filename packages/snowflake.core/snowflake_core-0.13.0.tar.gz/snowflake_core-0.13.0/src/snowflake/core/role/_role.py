from typing import TYPE_CHECKING, Iterator, Optional

from pydantic import StrictStr

from snowflake.core._common import AccountObjectCollectionParent, CreateMode, ObjectReferenceMixin
from snowflake.core._internal.telemetry import api_telemetry
from snowflake.core._internal.utils import deprecated
from snowflake.core.role._generated.api import RoleApi
from snowflake.core.role._generated.api_client import StoredProcApiClient
from snowflake.core.role._generated.models.role import RoleModel as Role


if TYPE_CHECKING:
    from snowflake.core import Root


class RoleCollection(AccountObjectCollectionParent["RoleResource"]):
    """Represents the collection operations on the Snowflake Role resource.

    With this collection, you can create, iterate through, and search for roles that you have access to in the
    current context.

    Examples
    ________
    Creating a role instance:

    >>> role_collection = root.roles
    >>> role_collection.create(Role(
    ...     name="test-role",
    ...     comment="samplecomment"
    ... ))
    """

    def __init__(self, root: "Root") -> None:
        super().__init__(root, ref_class=RoleResource)
        self._api = RoleApi(
            root=self.root,
            resource_class=self._ref_class,
            sproc_client=StoredProcApiClient(root=self.root)
        )

    @api_telemetry
    def create(self, role: Role, *, mode: CreateMode = CreateMode.error_if_exists) -> "RoleResource":
        """Create a role in Snowflake.

        Parameters
        __________
        role: Role
            The ``Role`` object, together with the ``Role``'s properties:
            name ; comment is optional
        mode: CreateMode, optional
            One of the following enum values.

            ``CreateMode.error_if_exists``: Throw an :class:`snowflake.core.exceptions.ConflictError`
            if the role already exists in Snowflake.  Equivalent to SQL ``create role <name> ...``.

            ``CreateMode.or_replace``: Replace if the role already exists in Snowflake. Equivalent to SQL
            ``create or replace role <name> ...``.

            ``CreateMode.if_not_exists``: Do nothing if the role already exists in Snowflake.
            Equivalent to SQL ``create role <name> if not exists...``

            Default is ``CreateMode.error_if_exists``.


        Examples
        ________
        Creating a role, replacing any existing role with the same name:

        >>> role = Role(
        ...     name="test-role",
        ...     comment="samplecomment"
        ... )
        >>> role_ref = root.roles.create(role, mode=CreateMode.or_replace)
        """
        real_mode = CreateMode[mode].value
        self._api.create_role(role._to_model(), StrictStr(real_mode))
        return self[role.name]

    def iter(self,
             *,
             like: Optional[str] = None,
             limit: Optional[int] = None,
             starts_with: Optional[str] = None,
             from_name: Optional[str] = None
             ) -> Iterator[Role]:
        """Iterate through ``Role`` objects from Snowflake, filtering on any optional 'like' pattern.

        Parameters
        _________
        like: str, optional
            A case-insensitive string functioning as a filter, with support for SQL
            wildcard characters (% and _).
        starts_with: str, optional
            String used to filter the command output based on the string of characters that appear
            at the beginning of the object name. Uses case-sensitive pattern matching.
        show_limit: int, optional
            Limit of the maximum number of rows returned by iter(). The default is ``None``, which behaves equivalently
            to show_limit=10000. This value must be between ``1`` and ``10000``.
        from_name: str, optional
            Fetch rows only following the first row whose object name matches
            the specified string. This is case-sensitive and does not have to be the full name.

        Examples
        ________
        Showing all roles that you have access to see:

        >>> roles = role_collection.iter()

        Showing information of the exact role you want to see:

        >>> roles = role_collection.iter(like="your-role-name")

        Showing roles starting with 'your-role-name-':

        >>> roles = role_collection.iter(like="your-role-name-%")
        >>> roles = role_collection.iter(starts_with="your-role-name")

        Using a for loop to retrieve information from iterator:

        >>> for role in roles:
        ...    print(role.name, role.comment)
        """
        roles = self._api.list_roles(
            StrictStr(like) if like else None,
            StrictStr(starts_with) if starts_with else None,
            limit,
            from_name=from_name,
            async_req=False
        )

        return map(Role._from_model, iter(roles))


class RoleResource(ObjectReferenceMixin[RoleCollection]):
    """Represents a reference to a Snowflake role.

    With this role reference, you can delete roles.
    """

    def __init__(self, name: str, collection: RoleCollection) -> None:
        self.name = name
        self.collection = collection

    @api_telemetry
    @deprecated("drop")
    def delete(self) -> None:
        self.drop()

    @api_telemetry
    def drop(self) -> None:
        """Drop this role.

        Examples
        ________
        Deleting a role using its reference:

        >>> role_reference.drop()
        """
        self.collection._api.delete_role(self.name, async_req=False)
