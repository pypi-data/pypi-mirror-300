# pylint: disable=too-few-public-methods,too-many-arguments
from decimal import (
    Decimal,
)
from fluidattacks_core.testing.constants import (
    CREATED_BY,
    FIXED_DATE,
)
from fluidattacks_core.testing.fakers.entities import (
    fake_severity_score,
)
from fluidattacks_core.testing.fakers.types import (
    SeverityLevelType,
    TreatmentStatusType,
)
from typing import (
    Any,
    Callable,
    Self,
)


class MetaBuilder(type):
    """
    Metaclass for implementing `set_` methods for every attribute in the class
    dynamically.

    Type annotations and expected value types for every set method
    must be defined in the class.
    """

    def __new__(mcs, name: str, bases: tuple, dct: dict) -> type:  # noqa: N804
        for attr in dct.get("__annotations__", {}):
            if attr.startswith("_") or attr.startswith("set_"):
                continue

            dct[f"set_{attr}"] = lambda self, value, attr=attr: (
                setattr(self, attr, value),  # type: ignore
                self,
            )[1]
        return super().__new__(mcs, name, bases, dct)


class GroupFaker(metaclass=MetaBuilder):
    # Required attributes
    org_id: str
    group_name: str

    # Optional attributes
    created_by: str = CREATED_BY
    creation_date: str = FIXED_DATE
    description: str = "Test group"
    language: str = "EN"
    tier: str = "ADVANCED"
    managed: str = "MANAGED"
    service: str = "WHITE"
    tags: list[str] = ["test-group"]
    subscription_type: str = "CONTINUOUS"
    status: str = "ACTIVE"
    business_id: str = "14441323"
    business_name: str = "Example ABC Inc."
    sprint_duration: int = 2
    policies: dict[str, str | int | Decimal] = {
        "max_number_acceptances": 3,
        "min_acceptance_severity": Decimal("0.0"),
        "vulnerability_grace_period": Decimal("10"),
        "min_breaking_severity": Decimal("3.9"),
        "max_acceptance_days": 90,
        "max_acceptance_severity": Decimal("3.9"),
        "modified_by": "unknown@fluidattacks.com",
        "modified_date": FIXED_DATE,
    }

    # Setters
    # Meta methods must be defined for linting support
    set_created_by: Callable[[str], Self]
    set_creation_date: Callable[[str], Self]
    set_description: Callable[[str], Self]
    set_language: Callable[[str], Self]
    set_tier: Callable[[str], Self]
    set_managed: Callable[[str], Self]
    set_service: Callable[[str], Self]
    set_tags: Callable[[list[str]], Self]
    set_subscription_type: Callable[[str], Self]
    set_status: Callable[[str], Self]
    set_business_id: Callable[[str], Self]
    set_business_name: Callable[[str], Self]
    set_sprint_duration: Callable[[int], Self]
    set_policies: Callable[[dict[str, str | int | Decimal]], Self]

    def __init__(
        self,
        org_id: str,
        group_name: str,
    ) -> None:
        self.org_id = org_id
        self.group_name = group_name

    def build(self) -> dict[str, Any]:
        return {
            "pk": f"GROUP#{self.group_name}",
            "sk": f"ORG#{self.org_id}",
            "name": self.group_name,
            "description": self.description,
            "language": self.language,
            "created_by": self.created_by,
            "created_date": self.creation_date,
            "state": {
                "modified_by": self.created_by,
                "modified_date": self.creation_date,
                "has_advanced": self.tier == "ADVANCED",
                "tier": self.tier,
                "managed": self.managed,
                "service": self.service,
                "has_essential": self.tier in ["ESSENTIAL", "ADVANCED"],
                "type": self.subscription_type,
                "status": self.status,
                **({"tags": self.tags} if self.tags else {}),
            },
            "organization_id": self.org_id,
            "business_id": self.business_id,
            "business_name": self.business_name,
            "sprint_duration": self.sprint_duration,
            "policies": self.policies,
        }


class VulnerabilityFaker(metaclass=MetaBuilder):
    # Required attributes
    vuln_id: str
    finding_id: str
    root_id: str
    group_name: str
    org_name: str

    # Optional attributes
    created_by: str = CREATED_BY
    creation_date: str = FIXED_DATE
    vuln_type: str = "LINES"
    vuln_technique: str = "SCA"
    report_date: str = FIXED_DATE
    source: str = "MACHINE"
    priority: int = 125
    efficacy: int = 0
    reattack_cycles: int = 0
    treatment_changes: int = 0
    where: str = "scanners/skipfish/Dockerfile"
    specific: str = "1"
    commit: str = "356a192b7913b04c54574d18c28d46e6395428ab"
    status: str = "VULNERABLE"
    zero_risk: dict[str, Any] | None = None
    severity_level: SeverityLevelType | None = None
    webhook_url: str | None = None
    bug_tracking_system_url: str | None = None
    treatment_status: TreatmentStatusType = "UNTREATED"

    # Setters
    # Meta methods must be defined for linting support
    set_created_by: Callable[[str], Self]
    set_creation_date: Callable[[str], Self]
    set_vuln_type: Callable[[str], Self]
    set_vuln_technique: Callable[[str], Self]
    set_report_date: Callable[[str], Self]
    set_source: Callable[[str], Self]
    set_priority: Callable[[int], Self]
    set_efficacy: Callable[[int], Self]
    set_reattack_cycles: Callable[[int], Self]
    set_treatment_changes: Callable[[int], Self]
    set_where: Callable[[str], Self]
    set_specific: Callable[[str], Self]
    set_commit: Callable[[str], Self]
    set_status: Callable[[str], Self]
    set_zero_risk: Callable[[dict[str, Any] | None], Self]
    set_severity_level: Callable[[SeverityLevelType], Self]
    set_webhook_url: Callable[[str], Self]
    set_bug_tracking_system_url: Callable[[str], Self]
    set_treatment_status: Callable[[TreatmentStatusType], Self]

    def __init__(
        self,
        vuln_id: str,
        finding_id: str,
        root_id: str,
        group_name: str,
        org_name: str,
    ) -> None:
        self.vuln_id = vuln_id
        self.finding_id = finding_id
        self.root_id = root_id
        self.group_name = group_name
        self.org_name = org_name

    def build(self) -> dict[str, Any]:
        deleted = str(self.status == "DELETED").lower()
        released = str(self.status in ["VULNERABLE", "SAFE"]).lower()

        return {
            "created_by": self.created_by,
            "created_date": self.creation_date,
            "pk": f"VULN#{self.vuln_id}",
            "sk": f"FIN#{self.finding_id}",
            "pk_2": f"ROOT#{self.root_id}",
            "sk_2": f"VULN#{self.vuln_id}",
            "pk_3": "USER",
            "sk_3": f"VULN#{self.vuln_id}",
            "pk_5": f"GROUP#{self.group_name}",
            "sk_5": (
                f"VULN#ZR#{bool(self.zero_risk)}#"
                f"STATE#{self.status.lower()}#TREAT#false"
            ),
            "pk_6": f"FIN#{self.finding_id}",
            "sk_6": (
                f"VULN#DELETED#{deleted}#RELEASED#{released}#"
                f"ZR#{bool(self.zero_risk)}#"
                f"STATE#{self.status.lower()}#VERIF#none"
            ),
            "treatment": {
                "modified_date": self.creation_date,
                "status": self.treatment_status,
            },
            "hacker_email": self.created_by,
            "group_name": self.group_name,
            "organization_name": self.org_name,
            "type": self.vuln_type,
            "technique": self.vuln_technique,
            "root_id": self.root_id,
            "unreliable_indicators": {
                "unreliable_reattack_cycles": self.reattack_cycles,
                "unreliable_source": self.source,
                "unreliable_efficacy": self.efficacy,
                "unreliable_priority": self.priority,
                "unreliable_report_date": self.report_date,
                "unreliable_treatment_changes": self.treatment_changes,
            },
            "state": {
                "modified_by": self.created_by,
                "commit": self.commit,
                "where": self.where,
                "source": self.source,
                "modified_date": self.creation_date,
                "specific": self.specific,
                "status": self.status,
            },
            **({"webhook_url": self.webhook_url} if self.webhook_url else {}),
            **(
                {"bug_tracking_system_url": self.bug_tracking_system_url}
                if self.bug_tracking_system_url
                else {}
            ),
            **(
                {"severity_score": fake_severity_score(self.severity_level)}
                if self.severity_level
                else {}
            ),
            **({"zero_risk": self.zero_risk} if self.zero_risk else {}),
        }
