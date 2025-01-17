from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from main import app
from superagi.models.organisation import Organisation
from superagi.models.tool import Tool
from superagi.models.tool_config import ToolConfig
from superagi.models.toolkit import Toolkit

client = TestClient(app)


@pytest.fixture
def mocks():
    # Mock tool kit data for testing
    user_organisation = Organisation(id=1)
    toolkit_1 = Toolkit(
        id=1,
        name="toolkit_1",
        description="None",
        show_toolkit=None,
        organisation_id=1
    )
    toolkit_2 = Toolkit(
        id=1,
        name="toolkit_2",
        description="None",
        show_toolkit=None,
        organisation_id=1
    )
    user_toolkits = [toolkit_1, toolkit_2]
    tool_1 = Tool(
        id=1,
        name="tool_1",
        description="Test Tool",
        folder_name="test folder",
        file_name="test file",
        toolkit_id=1
    )
    tool_2 = Tool(
        id=1,
        name="tool_2",
        description="Test Tool",
        folder_name="test folder",
        file_name="test file",
        toolkit_id=1
    )
    tool_3 = Tool(
        id=1,
        name="tool_3",
        description="Test Tool",
        folder_name="test folder",
        file_name="test file",
        toolkit_id=2
    )
    tools = [tool_1, tool_2, tool_3]
    return user_organisation, user_toolkits, tools, toolkit_1, toolkit_2, tool_1, tool_2, tool_3


def test_handle_marketplace_operations_list(mocks):
    # Unpack the fixture data
    user_organisation, user_toolkits, tools, toolkit_1, toolkit_2, tool_1, tool_2, tool_3 = mocks

    # Mock the database session and query functions
    with patch('superagi.helper.auth.get_user_organisation') as mock_get_user_org, \
            patch('superagi.controllers.toolkit.db') as mock_db, \
            patch('superagi.models.toolkit.Toolkit.fetch_marketplace_list') as mock_fetch_marketplace_list, \
            patch('superagi.helper.auth.db') as mock_auth_db:

        # Set up mock data
        mock_db.session.query.return_value.filter.return_value.all.side_effect = [user_toolkits]
        mock_fetch_marketplace_list.return_value = [toolkit_1.to_dict(), toolkit_2.to_dict()]

        # Call the function
        response = client.get("/toolkits/get/list", params={"page": 0})

        # Assertions
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 1,
                "name": "toolkit_1",
                "description": "None",
                "show_toolkit": None,
                "organisation_id": 1,
                "is_installed": True
            },
            {
                "id": 1,
                "name": "toolkit_2",
                "description": "None",
                "show_toolkit": None,
                "organisation_id": 1,
                "is_installed": True
            }
        ]
