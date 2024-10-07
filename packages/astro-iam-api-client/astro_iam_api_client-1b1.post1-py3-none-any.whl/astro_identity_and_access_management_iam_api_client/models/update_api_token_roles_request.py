from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.api_token_role import ApiTokenRole


T = TypeVar("T", bound="UpdateApiTokenRolesRequest")


@_attrs_define
class UpdateApiTokenRolesRequest:
    """
    Attributes:
        roles (List['ApiTokenRole']): The roles of the API token.
    """

    roles: List["ApiTokenRole"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        roles = []
        for roles_item_data in self.roles:
            roles_item = roles_item_data.to_dict()

            roles.append(roles_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "roles": roles,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.api_token_role import ApiTokenRole

        d = src_dict.copy()
        roles = []
        _roles = d.pop("roles")
        for roles_item_data in _roles:
            roles_item = ApiTokenRole.from_dict(roles_item_data)

            roles.append(roles_item)

        update_api_token_roles_request = cls(
            roles=roles,
        )

        update_api_token_roles_request.additional_properties = d
        return update_api_token_roles_request

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
