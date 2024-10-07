from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.permission_entry import PermissionEntry


T = TypeVar("T", bound="PermissionGroup")


@_attrs_define
class PermissionGroup:
    """
    Attributes:
        description (str): The permission group's description. Example: Astro notification channel defines where alert
            messages can be sent. For example, alert messages issued via email or slack..
        name (str): The permission group's name. Example: workspace.notificationChannels.
        permissions (List['PermissionEntry']): The permission group's permissions.
        scope (str): The permission group's scope. Example: Workspace NotificationChannels.
    """

    description: str
    name: str
    permissions: List["PermissionEntry"]
    scope: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        name = self.name
        permissions = []
        for permissions_item_data in self.permissions:
            permissions_item = permissions_item_data.to_dict()

            permissions.append(permissions_item)

        scope = self.scope

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "description": description,
                "name": name,
                "permissions": permissions,
                "scope": scope,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.permission_entry import PermissionEntry

        d = src_dict.copy()
        description = d.pop("description")

        name = d.pop("name")

        permissions = []
        _permissions = d.pop("permissions")
        for permissions_item_data in _permissions:
            permissions_item = PermissionEntry.from_dict(permissions_item_data)

            permissions.append(permissions_item)

        scope = d.pop("scope")

        permission_group = cls(
            description=description,
            name=name,
            permissions=permissions,
            scope=scope,
        )

        permission_group.additional_properties = d
        return permission_group

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
