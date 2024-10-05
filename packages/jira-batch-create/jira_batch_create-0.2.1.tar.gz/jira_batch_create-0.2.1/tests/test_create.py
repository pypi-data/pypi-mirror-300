import pytest
from unittest import mock
from jira_batch_create.creator import JiraIssueCreator

# Fixture for the mocked  field mapping (input from CSV)
@pytest.fixture
def mock_field_mapping():
    return {
        "Summary": "summary",
        "Description": "description",
        "Assignee": "assignee",
        "Priority": "priority",
        "Customer Impact Score": "customfield_11223"
    }


# Fixture for the mocked JSON data (input)
@pytest.fixture
def mock_json_issues():
    return [
        {
            "Summary": "Fix login bug",
            "Description": "Users are unable to log in due to timeout.",
            "Assignee": "john.doe",
            "Customer Impact Score": 4
        },
        {
            "Summary": "Update documentation",
            "Description": "Add documentation for the new feature.",
            "Assignee": "jane.smith",
            "Customer Impact Score": 1
        }
    ]

# Test to check if the fields are correctly translated
def test_field_translation(mock_json_issues, mock_field_mapping):
    # Initialize JiraIssueCreator with the mocked CSV data
    with mock.patch('jira_batch_create.creator.JiraIssueCreator._load_field_mapping') as init:
        jira_creator = JiraIssueCreator("fake_path")
        with mock.patch.object(jira_creator, 'field_mapping', mock_field_mapping):
            # Call batch_create_issues with the mocked JSON data
            jira_creator.batch_create_payload(mock_json_issues)
            
            # Check if the fields in the JSON data were translated correctly
            expected_translated_data = {
                "issueUpdates": [
                    {
                        "fields": {
                            "summary": "Fix login bug",
                            "description": "Users are unable to log in due to timeout.",
                            "assignee": "john.doe",
                            "customfield_11223": 4
                        },
                    },
                    {
                        "fields": {
                            "summary": "Update documentation",
                            "description": "Add documentation for the new feature.",
                            "assignee": "jane.smith",
                            "customfield_11223": 1
                        },
                    }
                ]
            }
            assert len(jira_creator.payload["issueUpdates"]) == 2
            for actual, expected in zip(jira_creator.payload["issueUpdates"],
                                        expected_translated_data["issueUpdates"]):
                assert actual == expected

            
@pytest.mark.skip()
def test_send():
    with mock.patch('jira_batch_create.creator.requests.post') as req:
        #  req.assert_called_with(json=expected_translated_data)
        pass
         
        