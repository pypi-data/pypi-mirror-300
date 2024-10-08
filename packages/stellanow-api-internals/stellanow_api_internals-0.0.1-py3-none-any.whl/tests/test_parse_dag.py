import unittest
from unittest.mock import patch

from stellanow_api_internals.clients.workflow_manager_client import WorkflowManagerClient


class TestParseDag(unittest.TestCase):

    def setUp(self):
        with patch.object(WorkflowManagerClient, "authenticate", return_value=None):
            self.client = WorkflowManagerClient(
                base_url="https://example.com",
                username="testuser",
                password="testpass",
                organization_id="org-id",
                project_id="project-id",
            )
        self.client.auth_token = "mocked_token"

    def test_parse_workflow_dag(self):
        config_data = {
            "id": "2afa8461-19d2-4807-a89c-87639e6d4247",
            "workflowId": "955512e1-b40d-4981-8657-df508ccc5b0e",
            "commitMessage": "",
            "versionNumber": 7,
            "isLatest": True,
            "isPublished": False,
            "createdAt": "2024-08-13T10:23:33.848233Z",
            "structure": {
                "nodes": [
                    {
                        "type": "filter",
                        "id": "c09a8800-077b-4a26-aa01-c330ace78ba0",
                        "position": {"x": 960, "y": 60},
                        "data": {
                            "displayInfo": {"title": "FilterAirState", "description": ""},
                            "config": {
                                "id": "7018fff6-114b-470e-98c2-5505eb448570",
                                "conditions": [
                                    {
                                        "id": "01c1e650-929c-4722-bbe4-f8b4e8daed0a",
                                        "left": {
                                            "id": "6a0a5f4e-6200-4ab3-b7bf-16057dd6256d",
                                            "fieldName": "eventTypeDefinitionId",
                                        },
                                        "right": {
                                            "type": "ExplicitType",
                                            "id": "0bd4120b-8940-4ce3-bee3-4d8de39a9e40",
                                            "value": "air_quality_state",
                                            "multiValue": False,
                                        },
                                        "condition": "EQ",
                                        "negate": False,
                                        "fieldType": {"value": "String"},
                                    }
                                ],
                                "operator": "AND",
                            },
                            "isStateful": False,
                        },
                    },
                    {
                        "type": "notify",
                        "id": "57b80f86-83c7-46c0-8159-8ccd0f887638",
                        "position": {"x": 960, "y": 220},
                        "data": {
                            "displayInfo": {"title": "TestDEstiantion"},
                            "config": {
                                "id": "32c54d47-ded2-4785-aadd-7ab13cc0c116",
                                "channel": "5d50656f-e5c7-4464-84b5-86f283e59bf2",
                                "fields": [
                                    {
                                        "targetFieldName": "name",
                                        "source": {
                                            "type": "EventType",
                                            "id": "db096e59-cf14-43fb-bdeb-43a1cc5fe497",
                                            "fieldId": "1a9b7af0-3e8d-4144-8c71-71eb2505d140",
                                            "multiValue": False,
                                            "eventName": "air_quality_state",
                                            "fieldName": "ijp.name",
                                        },
                                    }
                                ],
                            },
                            "isStateful": True,
                        },
                    },
                    {
                        "type": "propagateToSource",
                        "id": "504805b9-2cf8-4c2f-9f6c-b4469b1399ac",
                        "position": {"x": 960, "y": 380},
                        "data": {
                            "displayInfo": {"title": "rtg45t", "description": ""},
                            "config": {"id": "5e6add30-db6a-471a-a2a1-316dc2c7a75f"},
                            "isStateful": False,
                        },
                    },
                ],
                "edges": [
                    {
                        "id": "e69ab4e5-11bb-46e3-9744-7ad74564216c",
                        "source": "c09a8800-077b-4a26-aa01-c330ace78ba0",
                        "target": "57b80f86-83c7-46c0-8159-8ccd0f887638",
                    },
                    {
                        "id": "cbb83131-b9e8-4845-88bd-97f333a703b8",
                        "source": "57b80f86-83c7-46c0-8159-8ccd0f887638",
                        "target": "504805b9-2cf8-4c2f-9f6c-b4469b1399ac",
                    },
                ],
            },
        }
        result = self.client._parse_workflow_dag(details=config_data)

        expected_structure = config_data["structure"]
        actual_structure = result.structure.model_dump(exclude_none=True)

        self.assertEqual(expected_structure, actual_structure)

        self.assertEqual(config_data["id"], result.id)
        self.assertEqual(config_data["workflowId"], result.workflowId)

    def test_parse_dag_node_config_with_filter(self):
        config_data = {
            "id": "7018fff6-114b-470e-98c2-5505eb448570",
            "conditions": [
                {
                    "id": "01c1e650-929c-4722-bbe4-f8b4e8daed0a",
                    "left": {"id": "6a0a5f4e-6200-4ab3-b7bf-16057dd6256d", "fieldName": "eventTypeDefinitionId"},
                    "right": {
                        "type": "ExplicitType",
                        "id": "0bd4120b-8940-4ce3-bee3-4d8de39a9e40",
                        "value": "air_quality_state",
                        "multiValue": False,
                    },
                    "condition": "EQ",
                    "negate": False,
                    "fieldType": {"value": "String"},
                }
            ],
            "operator": "AND",
        }

        result = self.client._parse_dag_node_config("filter", config_data)

        expected_result = {
            "id": "7018fff6-114b-470e-98c2-5505eb448570",
            "conditions": [
                {
                    "id": "01c1e650-929c-4722-bbe4-f8b4e8daed0a",
                    "left": {"id": "6a0a5f4e-6200-4ab3-b7bf-16057dd6256d", "fieldName": "eventTypeDefinitionId"},
                    "right": {
                        "type": "ExplicitType",
                        "id": "0bd4120b-8940-4ce3-bee3-4d8de39a9e40",
                        "value": "air_quality_state",
                        "multiValue": False,
                    },
                    "condition": "EQ",
                    "negate": False,
                    "fieldType": {"value": "String"},
                }
            ],
            "operator": "AND",
        }

        self.assertEqual(result, expected_result)

    def test_parse_dag_node_config_with_notify(self):
        config_data = {
            "id": "32c54d47-ded2-4785-aadd-7ab13cc0c116",
            "channel": "5d50656f-e5c7-4464-84b5-86f283e59bf2",
            "fields": [
                {
                    "targetFieldName": "name",
                    "source": {
                        "type": "EventType",
                        "id": "db096e59-cf14-43fb-bdeb-43a1cc5fe497",
                        "fieldId": "1a9b7af0-3e8d-4144-8c71-71eb2505d140",
                        "multiValue": False,
                        "eventName": "air_quality_state",
                        "fieldName": "ijp.name",
                    },
                }
            ],
        }

        result = self.client._parse_dag_node_config("notify", config_data)

        expected_result = {
            "id": "32c54d47-ded2-4785-aadd-7ab13cc0c116",
            "channel": "5d50656f-e5c7-4464-84b5-86f283e59bf2",
            "fields": [
                {
                    "targetFieldName": "name",
                    "source": {
                        "type": "EventType",
                        "id": "db096e59-cf14-43fb-bdeb-43a1cc5fe497",
                        "fieldId": "1a9b7af0-3e8d-4144-8c71-71eb2505d140",
                        "multiValue": False,
                        "eventName": "air_quality_state",
                        "fieldName": "ijp.name",
                    },
                }
            ],
        }

        self.assertEqual(result, expected_result)

    def test_parse_dag_node_config_with_propagate_to_source(self):
        config_data = {"id": "5e6add30-db6a-471a-a2a1-316dc2c7a75f"}

        result = self.client._parse_dag_node_config("propagateToSource", config_data)

        expected_result = {"id": "5e6add30-db6a-471a-a2a1-316dc2c7a75f"}

        self.assertEqual(result, expected_result)
