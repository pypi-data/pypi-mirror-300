from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.role_template_scope_type import RoleTemplateScopeType
from ..types import UNSET, Unset

T = TypeVar("T", bound="RoleTemplate")


@_attrs_define
class RoleTemplate:
    """
    Attributes:
        name (str): The role's name. Example: Deployment_Viewer.
        permissions (List[str]): The role's permissions. Example: ['deployment.get'].
        scope_type (RoleTemplateScopeType): The role's scope. Example: DEPLOYMENT.
        description (Union[Unset, str]): The role's description. Example: Subject can only view deployments..
    """

    name: str
    permissions: List[str]
    scope_type: RoleTemplateScopeType
    description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        permissions = self.permissions

        scope_type = self.scope_type.value

        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "permissions": permissions,
                "scopeType": scope_type,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        permissions = cast(List[str], d.pop("permissions"))

        scope_type = RoleTemplateScopeType(d.pop("scopeType"))

        description = d.pop("description", UNSET)

        role_template = cls(
            name=name,
            permissions=permissions,
            scope_type=scope_type,
            description=description,
        )

        role_template.additional_properties = d
        return role_template

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
