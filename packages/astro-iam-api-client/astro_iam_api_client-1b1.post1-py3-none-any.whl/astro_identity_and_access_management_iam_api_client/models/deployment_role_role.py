from enum import Enum


class DeploymentRoleRole(str, Enum):
    DEPLOYMENT_ADMIN = "DEPLOYMENT_ADMIN"

    def __str__(self) -> str:
        return str(self.value)
