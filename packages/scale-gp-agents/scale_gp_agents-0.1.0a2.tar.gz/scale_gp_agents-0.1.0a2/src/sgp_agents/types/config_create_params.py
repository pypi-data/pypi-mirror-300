# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .node_item_param import NodeItemParam
from .plan_config_param import PlanConfigParam
from .workflow_config_param import WorkflowConfigParam

__all__ = [
    "ConfigCreateParams",
    "Config",
    "ConfigStateMachineConfig",
    "ConfigStateMachineConfigMachine",
    "ConfigStateMachineConfigMachineNextNode",
    "ConfigStateMachineConfigMachineNextNodeCase",
    "ConfigStateMachineConfigMachineNextNodeCaseCondition",
    "ConfigStateMachineConfigMachineNextNodeCaseConditionUnaryCondition",
    "ConfigStateMachineConfigMachineNextNodeCaseConditionCompoundCondition",
    "ConfigStateMachineConfigMachineNextNodeCaseConditionCompoundConditionCondition",
    "ConfigStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionUnaryCondition",
    "ConfigStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundCondition",
    "ConfigStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundConditionCondition",
    "ConfigStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundConditionConditionUnaryCondition",
]


class ConfigCreateParams(TypedDict, total=False):
    config: Required[Config]
    """Representation of a plan, i.e. a composition of workflows and branch complexes

    Public attributes: workflows: maps a workflow "name" to either a workflow yaml
    file or an inline workflow definition plan: representation of the graph
    connecting workflows / branch complexes

    Private attributes: helper_workflows: a list of workflows created by default, in
    order to support loops and other control flow features
    """


class ConfigStateMachineConfigMachineNextNodeCaseConditionUnaryCondition(TypedDict, total=False):
    condition_input_var: Required[str]

    operator: Required[str]

    reference_var: object


class ConfigStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionUnaryCondition(
    TypedDict, total=False
):
    condition_input_var: Required[str]

    operator: Required[str]

    reference_var: object


class ConfigStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundConditionConditionUnaryCondition(
    TypedDict, total=False
):
    condition_input_var: Required[str]

    operator: Required[str]

    reference_var: object


ConfigStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundConditionCondition: TypeAlias = Union[
    ConfigStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundConditionConditionUnaryCondition,
    object,
]


class ConfigStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundCondition(
    TypedDict, total=False
):
    conditions: Iterable[
        ConfigStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundConditionCondition
    ]

    input_names: List[str]

    logical_operator: Literal["ALL", "ANY", "NOT"]


ConfigStateMachineConfigMachineNextNodeCaseConditionCompoundConditionCondition: TypeAlias = Union[
    ConfigStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionUnaryCondition,
    ConfigStateMachineConfigMachineNextNodeCaseConditionCompoundConditionConditionCompoundCondition,
]


class ConfigStateMachineConfigMachineNextNodeCaseConditionCompoundCondition(TypedDict, total=False):
    conditions: Iterable[ConfigStateMachineConfigMachineNextNodeCaseConditionCompoundConditionCondition]

    input_names: List[str]

    logical_operator: Literal["ALL", "ANY", "NOT"]


ConfigStateMachineConfigMachineNextNodeCaseCondition: TypeAlias = Union[
    ConfigStateMachineConfigMachineNextNodeCaseConditionUnaryCondition,
    ConfigStateMachineConfigMachineNextNodeCaseConditionCompoundCondition,
]


class ConfigStateMachineConfigMachineNextNodeCase(TypedDict, total=False):
    condition: Required[ConfigStateMachineConfigMachineNextNodeCaseCondition]
    """Representation of a boolean function with a single input e.g.

    the condition specified by input_name: x operator: 'contains' ref_value: 'c'
    would evaluate to True if x == 'cat' Operators are defined in the constant
    function store CONDITIONAL_ACTION_MAP
    """

    value: Required[str]


class ConfigStateMachineConfigMachineNextNode(TypedDict, total=False):
    default: Required[str]

    cases: Iterable[ConfigStateMachineConfigMachineNextNodeCase]


class ConfigStateMachineConfigMachine(TypedDict, total=False):
    next_node: Required[ConfigStateMachineConfigMachineNextNode]
    """A switch statement for state machines to select the next state to execute."""

    workflow_config: Required[WorkflowConfigParam]

    write_to_state: Dict[str, str]


class ConfigStateMachineConfig(TypedDict, total=False):
    machine: Required[Dict[str, ConfigStateMachineConfigMachine]]

    starting_node: Required[str]

    id: str

    account_id: str

    application_variant_id: str

    base_url: str

    concurrency_default: bool

    datasets: Iterable[object]

    done_string: str

    egp_api_key_override: str

    egp_ui_evaluation: object

    evaluations: Iterable[NodeItemParam]

    final_output_nodes: List[str]

    initial_state: object

    nodes_to_log: Union[str, List[str]]

    num_workers: int

    streaming_nodes: List[str]

    type: Literal["workflow", "plan", "state_machine"]
    """An enumeration."""


Config: TypeAlias = Union[PlanConfigParam, WorkflowConfigParam, ConfigStateMachineConfig]
