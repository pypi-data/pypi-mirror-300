# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel
from .node_item import NodeItem
from .plan_config import PlanConfig
from .workflow_config import WorkflowConfig

__all__ = [
    "ConfigListResponse",
    "ConfigListResponseItem",
    "ConfigListResponseItemStateMachineConfig",
    "ConfigListResponseItemStateMachineConfigMachine",
    "ConfigListResponseItemStateMachineConfigMachineNextNode",
    "ConfigListResponseItemStateMachineConfigMachineNextNodeCase",
    "ConfigListResponseItemStateMachineConfigMachineNextNodeCaseCondition",
    "ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionUnaryCondition",
    "ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionCompoundCondition",
    "ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionCompoundConditionCondition",
    "ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionUnaryCondition",
    "ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundCondition",
    "ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundConditionCondition",
    "ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundConditionConditionUnaryCondition",
]


class ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionUnaryCondition(BaseModel):
    condition_input_var: str

    operator: str

    reference_var: Optional[object] = None


class ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionUnaryCondition(
    BaseModel
):
    condition_input_var: str

    operator: str

    reference_var: Optional[object] = None


class ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundConditionConditionUnaryCondition(
    BaseModel
):
    condition_input_var: str

    operator: str

    reference_var: Optional[object] = None


ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundConditionCondition: TypeAlias = Union[
    ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundConditionConditionUnaryCondition,
    object,
]


class ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundCondition(
    BaseModel
):
    conditions: Optional[
        List[
            ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundConditionCondition
        ]
    ] = None

    input_names: Optional[List[str]] = None

    logical_operator: Optional[Literal["ALL", "ANY", "NOT"]] = None


ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionCompoundConditionCondition: TypeAlias = Union[
    ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionUnaryCondition,
    ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundCondition,
]


class ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionCompoundCondition(BaseModel):
    conditions: Optional[
        List[ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionCompoundConditionCondition]
    ] = None

    input_names: Optional[List[str]] = None

    logical_operator: Optional[Literal["ALL", "ANY", "NOT"]] = None


ConfigListResponseItemStateMachineConfigMachineNextNodeCaseCondition: TypeAlias = Union[
    ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionUnaryCondition,
    ConfigListResponseItemStateMachineConfigMachineNextNodeCaseConditionCompoundCondition,
]


class ConfigListResponseItemStateMachineConfigMachineNextNodeCase(BaseModel):
    condition: ConfigListResponseItemStateMachineConfigMachineNextNodeCaseCondition
    """Representation of a boolean function with a single input e.g.

    the condition specified by input_name: x operator: 'contains' ref_value: 'c'
    would evaluate to True if x == 'cat' Operators are defined in the constant
    function store CONDITIONAL_ACTION_MAP
    """

    value: str


class ConfigListResponseItemStateMachineConfigMachineNextNode(BaseModel):
    default: str

    cases: Optional[List[ConfigListResponseItemStateMachineConfigMachineNextNodeCase]] = None


class ConfigListResponseItemStateMachineConfigMachine(BaseModel):
    next_node: ConfigListResponseItemStateMachineConfigMachineNextNode
    """A switch statement for state machines to select the next state to execute."""

    workflow_config: WorkflowConfig

    write_to_state: Optional[Dict[str, str]] = None


class ConfigListResponseItemStateMachineConfig(BaseModel):
    machine: Dict[str, ConfigListResponseItemStateMachineConfigMachine]

    starting_node: str

    id: Optional[str] = None

    account_id: Optional[str] = None

    application_variant_id: Optional[str] = None

    base_url: Optional[str] = None

    concurrency_default: Optional[bool] = None

    datasets: Optional[List[object]] = None

    done_string: Optional[str] = None

    egp_api_key_override: Optional[str] = None

    egp_ui_evaluation: Optional[object] = None

    evaluations: Optional[List[NodeItem]] = None

    final_output_nodes: Optional[List[str]] = None

    initial_state: Optional[object] = None

    nodes_to_log: Union[str, List[str], None] = None

    num_workers: Optional[int] = None

    streaming_nodes: Optional[List[str]] = None

    type: Optional[Literal["workflow", "plan", "state_machine"]] = None
    """An enumeration."""


ConfigListResponseItem: TypeAlias = Union[PlanConfig, WorkflowConfig, ConfigListResponseItemStateMachineConfig]

ConfigListResponse: TypeAlias = List[ConfigListResponseItem]
