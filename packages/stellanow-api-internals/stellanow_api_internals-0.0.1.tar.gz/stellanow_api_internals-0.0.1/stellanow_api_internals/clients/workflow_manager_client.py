"""
Copyright (C) 2022-2024 Stella Technologies (UK) Limited.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

from typing import Dict, List, Optional

import httpx

from stellanow_api_internals.clients.base_api_client import StellanowBaseAPIClient
from stellanow_api_internals.core.enums import FilterIncludeArchived, FilterIncludeInactive
from stellanow_api_internals.datatypes.workflow_mgmt import (
    DAGAggregationNodeData,
    DAGAwaitNodeData,
    DAGClearEntityNodeData,
    DAGFilterNodeData,
    DAGNodeCondition,
    DAGNotificationNodeData,
    DAGPropagateToEntityNodeData,
    DAGPropagateToSourceNodeData,
    DAGTerminationTypeDefinition,
    DAGTransformationNodeData,
    StellaEntity,
    StellaEntityCreate,
    StellaEntityDetailed,
    StellaEntityField,
    StellaEntityUpdate,
    StellaEvent,
    StellaEventCreate,
    StellaEventDetailed,
    StellaField,
    StellaModel,
    StellaModelCreate,
    StellaModelDetailed,
    StellaModelField,
    StellaProject,
    StellaProjectCreate,
    StellaProjectDetailed,
    StellaShortEntity,
    StellaShortEvent,
    StellaWorkflow,
    StellaWorkflowCreate,
    StellaWorkflowDAG,
    StellaWorkflowDagCreate,
    StellaWorkflowDAGData,
    StellaWorkflowDAGDisplayInfo,
    StellaWorkflowDAGEdge,
    StellaWorkflowDAGNodes,
    StellaWorkflowDAGPosition,
    StellaWorkflowDAGStructure,
    StellaWorkflowDetailed,
)

WORKFLOW_MANAGEMENT_API = "/workflow-management/projects/"


class WorkflowManagerClient(StellanowBaseAPIClient):
    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        organization_id: str,
        project_id: Optional[str] = None,
        client: Optional[httpx.Client] = None,
    ) -> None:
        super().__init__(base_url, username, password, organization_id, client)
        self.project_id = project_id

    @property
    def base_path(self) -> str:
        return WORKFLOW_MANAGEMENT_API

    @property
    def _projects_url(self):
        return f"{self.base_url}{WORKFLOW_MANAGEMENT_API}"

    @property
    def _project_url(self):
        return self._build_url_project_required("")

    @property
    def _events_url(self):
        return self._build_url_project_required("/events")

    @property
    def _event_url(self):
        return self._build_url_project_required("/events/{eventId}")

    @property
    def _entities_url(self):
        return self._build_url_project_required("/entities")

    @property
    def _entity_url(self):
        return self._build_url_project_required("/entities/{entityId}")

    @property
    def _models_url(self):
        return self._build_url_project_required("/models")

    @property
    def _model_url(self):
        return self._build_url_project_required("/models/{modelId}")

    @property
    def _workflows_url(self):
        return self._build_url_project_required("/workflows")

    @property
    def _workflow_url(self):
        return self._build_url_project_required("/workflows/{workflowId}")

    @property
    def _workflow_dag_latest_url(self):
        return self._build_url_project_required("/workflows/{workflowId}/dag/latest")

    @property
    def _workflow_dag_version_url(self):
        return self._build_url_project_required("/workflows/{workflowId}/dag/versions/{versionId}")

    @staticmethod
    def _parse_dag_node_config(node_type: str, config_data: Dict) -> Dict:
        """Parse the DAG node config and return the correct dictionary representation."""

        node_type_to_class = {
            "aggregate": DAGAggregationNodeData,
            "clearEntity": DAGClearEntityNodeData,
            "condition": DAGNodeCondition,
            "filter": DAGFilterNodeData,
            "notify": DAGNotificationNodeData,
            "propagateToEntity": DAGPropagateToEntityNodeData,
            "propagateToSource": DAGPropagateToSourceNodeData,
            "termination": DAGTerminationTypeDefinition,
            "transform": DAGTransformationNodeData,
            "await": DAGAwaitNodeData,
        }

        if node_type not in node_type_to_class:
            raise ValueError(f"Unknown DAG node type: {node_type}")

        config_class = node_type_to_class[node_type]

        config_instance = config_class.model_validate(config_data)
        config_model = config_class.model_validate(config_instance.model_dump())
        config_dict = config_model.dict()
        config_flattened: Dict = {k: v for k, v in config_dict.items() if v is not None}
        config_flattened["id"] = config_data.get("id")

        return config_flattened

    def _parse_workflow_dag(self, details: Dict) -> StellaWorkflowDAG:
        nodes = [
            StellaWorkflowDAGNodes(
                id=node.get("id"),
                type=node.get("type"),
                position=StellaWorkflowDAGPosition(**node.get("position")),
                data=StellaWorkflowDAGData(
                    displayInfo=StellaWorkflowDAGDisplayInfo(
                        title=node["data"]["displayInfo"].get("title", ""),
                        description=node["data"]["displayInfo"].get("description"),
                    ),
                    config=self._parse_dag_node_config(node.get("type"), node["data"]["config"]),
                    isStateful=node["data"].get("isStateful"),
                ),
            )
            for node in details["structure"]["nodes"]
        ]

        edges = [
            StellaWorkflowDAGEdge(id=edge.get("id"), source=edge.get("source"), target=edge.get("target"))
            for edge in details["structure"]["edges"]
        ]

        structure = StellaWorkflowDAGStructure(nodes=nodes, edges=edges)

        return StellaWorkflowDAG(
            id=details.get("id"),
            workflowId=details.get("workflowId"),
            commitMessage=details.get("commitMessage"),
            versionNumber=details.get("versionNumber"),
            isLatest=details.get("isLatest"),
            isPublished=details.get("isPublished"),
            createdAt=details.get("createdAt"),
            structure=structure,
        )

    def create_project(self, project_data: dict) -> StellaProjectDetailed:
        url = self._projects_url
        project_data_model = StellaProjectCreate(**project_data)
        details = self._make_request(url=url, method="POST", data=project_data_model.model_dump())

        return StellaProjectDetailed(**details)

    def create_event(self, event_data: dict) -> StellaEventDetailed:
        url = self._events_url
        event_data_model = StellaEventCreate(**event_data)
        details = self._make_request(url=url, method="POST", data=event_data_model.model_dump())

        return StellaEventDetailed(**details)

    def create_entity(self, entity_data: dict) -> StellaEntityDetailed:
        url = self._entities_url
        entity_data_model = StellaEntityCreate(**entity_data)
        details = self._make_request(url=url, method="POST", data=entity_data_model.model_dump())

        return StellaEntityDetailed(**details)

    def update_entity(self, entity_data: dict, entity_id: str) -> StellaEntityDetailed:
        url = self._entity_url.format(entityId=entity_id)
        entity_data_model = StellaEntityUpdate(**entity_data)
        details = self._make_request(url=url, method="PATCH", data=entity_data_model.model_dump())

        return StellaEntityDetailed(**details)

    def create_model(self, model_data: dict) -> StellaModelDetailed:
        url = self._models_url
        model_data_model = StellaModelCreate(**model_data)
        details = self._make_request(url=url, method="POST", data=model_data_model.model_dump())

        return StellaModelDetailed(**details)

    def create_workflow(self, workflow_data: dict) -> StellaWorkflowDetailed:
        url = self._workflows_url
        workflow_data_model = StellaWorkflowCreate(**workflow_data)
        details = self._make_request(url=url, method="POST", data=workflow_data_model.model_dump())

        return StellaWorkflowDetailed(**details)

    def create_workflow_dag(self, workflow_id: str, dag_data: dict) -> StellaWorkflowDAG:
        url = f"{self._workflows_url}/{workflow_id}/dag"
        dag_data_model = StellaWorkflowDagCreate(**dag_data)
        details = self._make_request(url=url, method="POST", data=dag_data_model.model_dump())

        return StellaWorkflowDAG(**details)

    def get_projects(
        self,
        page: int = 1,
        page_size: int = 20,
        include_archived: Optional[bool] = None,
        search: Optional[str] = None,
        sorting: Optional[str] = "projects:created:asc",
    ) -> List[StellaProject]:
        filter_query = None
        if include_archived:
            filter_query = FilterIncludeArchived.INCLUDE_ARCHIVED.value

        return self._get_paginated_results(
            url_template=self._projects_url,
            result_class=StellaProject,
            page=page,
            page_size=page_size,
            filter=filter_query,
            search=search,
            sorting=sorting,
        )

    def get_project_details(self) -> StellaProjectDetailed:
        url = self._project_url
        details = self._make_request(url)

        return StellaProjectDetailed(**details)

    def get_events(
        self,
        page: int = 1,
        page_size: int = 20,
        include_inactive: Optional[bool] = None,
        search: Optional[str] = None,
        sorting: Optional[str] = "events:created:asc",
    ) -> List[StellaEvent]:

        filter_query = None
        if include_inactive:
            filter_query = FilterIncludeInactive.INCLUDE_INACTIVE.value

        return self._get_paginated_results(
            url_template=self._events_url,
            result_class=StellaEvent,
            page=page,
            page_size=page_size,
            filter=filter_query,
            search=search,
            sorting=sorting,
        )

    def get_event_details(self, event_id: str) -> StellaEventDetailed:
        url = self._event_url.format(eventId=event_id)
        details = self._make_request(url)

        details["entities"] = [StellaShortEntity(**entity) for entity in details.get("entities", [])]
        details["fields"] = [StellaField(**field) for field in details.get("fields", [])]

        return StellaEventDetailed(**details)

    def get_entities(
        self,
        page: int = 1,
        page_size: int = 20,
        include_inactive: Optional[bool] = None,
        search: Optional[str] = None,
        sorting: Optional[str] = "entities:created:asc",
    ) -> List[StellaEntity]:
        filter_query = None
        if include_inactive:
            filter_query = FilterIncludeInactive.INCLUDE_INACTIVE.value

        return self._get_paginated_results(
            url_template=self._entities_url,
            result_class=StellaEntity,
            page=page,
            page_size=page_size,
            filter=filter_query,
            search=search,
            sorting=sorting,
        )

    def get_entity_details(self, entity_id: str) -> StellaEntityDetailed:
        url = self._entity_url.format(entityId=entity_id)
        details = self._make_request(url)

        details["events"] = [StellaShortEvent(**event) for event in details.get("events", list())]
        details["fields"] = [StellaEntityField(**field) for field in details.get("fields", list())]

        return StellaEntityDetailed(**details)

    def get_models(
        self,
        page: int = 1,
        page_size: int = 20,
        filter: Optional[str] = None,
        search: Optional[str] = None,
        sorting: Optional[str] = None,
    ) -> List[StellaModel]:
        return self._get_paginated_results(
            url_template=self._models_url,
            result_class=StellaModel,
            page=page,
            page_size=page_size,
            filter=filter,
            search=search,
            sorting=sorting,
        )

    def get_model_details(self, model_id: str) -> StellaModelDetailed:
        url = self._model_url.format(modelId=model_id)
        details = self._make_request(url)
        details["fields"] = [StellaModelField(**field) for field in details.get("fields", list())]

        return StellaModelDetailed(**details)

    def get_workflows(
        self,
        page: int = 1,
        page_size: int = 20,
        include_inactive: Optional[bool] = None,
        search: Optional[str] = None,
        sorting: Optional[str] = "workflows:created:asc",
    ) -> List[StellaWorkflow]:
        filter_query = None
        if include_inactive:
            filter_query = FilterIncludeInactive.INCLUDE_INACTIVE.value

        return self._get_paginated_results(
            url_template=self._workflows_url,
            result_class=StellaWorkflow,
            page=page,
            page_size=page_size,
            filter=filter_query,
            search=search,
            sorting=sorting,
        )

    def get_workflow_details(self, workflow_id: str) -> StellaWorkflowDetailed:
        url = self._workflow_url.format(workflowId=workflow_id)
        details = self._make_request(url)

        details["events"] = [StellaShortEvent(**event) for event in details.get("events", list())]
        details["entities"] = [StellaShortEntity(**entity) for entity in details.get("entities", list())]

        return StellaWorkflowDetailed(**details)

    def get_latest_workflow_dag(self, workflow_id: str) -> StellaWorkflowDAG:
        url = self._workflow_dag_latest_url.format(workflowId=workflow_id)
        details = self._make_request(url)
        return self._parse_workflow_dag(details)

    def get_workflow_dag_version(self, workflow_id: str, version_id: str) -> StellaWorkflowDAG:
        url = self._workflow_dag_version_url.format(workflowId=workflow_id, versionId=version_id)
        details = self._make_request(url)
        return self._parse_workflow_dag(details)
