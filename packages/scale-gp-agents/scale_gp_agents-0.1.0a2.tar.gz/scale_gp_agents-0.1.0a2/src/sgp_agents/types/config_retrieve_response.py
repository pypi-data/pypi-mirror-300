# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel
from .node_item import NodeItem
from .plan_config import PlanConfig
from .workflow_config import WorkflowConfig

__all__ = [
    "ConfigRetrieveResponse",
    "StateMachineConfig",
    "StateMachineConfigMachine",
    "StateMachineConfigMachineNextNode",
    "StateMachineConfigMachineNextNodeCase",
    "StateMachineConfigMachineNextNodeCaseCondition",
    "StateMachineConfigMachineNextNodeCaseConditionUnaryCondition",
    "StateMachineConfigMachineNextNodeCaseConditionCompoundCondition",
    "StateMachineConfigMachineNextNodeCaseConditionCompoundConditionCondition",
    "StateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionUnaryCondition",
    "StateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundCondition",
    "StateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundConditionCondition",
    "StateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundConditionConditionUnaryCondition",
]


class StateMachineConfigMachineNextNodeCaseConditionUnaryCondition(BaseModel):
    condition_input_var: str

    operator: str

    reference_var: Optional[object] = None


class StateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionUnaryCondition(BaseModel):
    condition_input_var: str

    operator: str

    reference_var: Optional[object] = None


class StateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundConditionConditionUnaryCondition(
    BaseModel
):
    condition_input_var: str

    operator: str

    reference_var: Optional[object] = None


StateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundConditionCondition: TypeAlias = Union[
    StateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundConditionConditionUnaryCondition,
    object,
]


class StateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundCondition(BaseModel):
    conditions: Optional[
        List[StateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundConditionCondition]
    ] = None

    input_names: Optional[List[str]] = None

    logical_operator: Optional[Literal["ALL", "ANY", "NOT"]] = None


StateMachineConfigMachineNextNodeCaseConditionCompoundConditionCondition: TypeAlias = Union[
    StateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionUnaryCondition,
    StateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundCondition,
]


class StateMachineConfigMachineNextNodeCaseConditionCompoundCondition(BaseModel):
    conditions: Optional[List[StateMachineConfigMachineNextNodeCaseConditionCompoundConditionCondition]] = None

    input_names: Optional[List[str]] = None

    logical_operator: Optional[Literal["ALL", "ANY", "NOT"]] = None


StateMachineConfigMachineNextNodeCaseCondition: TypeAlias = Union[
    StateMachineConfigMachineNextNodeCaseConditionUnaryCondition,
    StateMachineConfigMachineNextNodeCaseConditionCompoundCondition,
]


class StateMachineConfigMachineNextNodeCase(BaseModel):
    condition: StateMachineConfigMachineNextNodeCaseCondition
    """Representation of a boolean function with a single input e.g.

    the condition specified by input_name: x operator: 'contains' ref_value: 'c'
    would evaluate to True if x == 'cat' Operators are defined in the constant
    function store CONDITIONAL_ACTION_MAP
    """

    value: str


class StateMachineConfigMachineNextNode(BaseModel):
    default: str

    cases: Optional[List[StateMachineConfigMachineNextNodeCase]] = None


class StateMachineConfigMachine(BaseModel):
    next_node: StateMachineConfigMachineNextNode
    """A switch statement for state machines to select the next state to execute."""

    workflow_config: WorkflowConfig

    write_to_state: Optional[Dict[str, str]] = None


class StateMachineConfig(BaseModel):
    machine: Dict[str, StateMachineConfigMachine]

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


ConfigRetrieveResponse: TypeAlias = Union[PlanConfig, WorkflowConfig, StateMachineConfig]
