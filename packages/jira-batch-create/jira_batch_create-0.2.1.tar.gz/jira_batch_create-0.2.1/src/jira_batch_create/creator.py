import csv
import logging
import requests

import requests
from adf import get_description_in_adf_format

class JiraMetaClass(type):
    def __new__(mcs, name, bases, dct, base_url=None, auth=None, issue_key=None):
        if not base_url or not auth:
            raise ValueError("base_url and auth must be provided to the metaclass.")

        cls = super().__new__(mcs, name, bases, dct)

        # Fetch the project schema fields from Jira
        schema_url = f"{base_url}/rest/api/3/field"
        response = requests.get(schema_url, auth=auth)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch project schema. Status: {response.status_code}, Response: {response.text}")

        schema_data = response.json()
        
        cls.schema_data = {}
        cls._field_getters = {}
        cls.base_url = base_url
        cls.auth = auth
        # cls.issue_key = issue_key  # Store the issue key for future use

        # Dynamically create fields and getters for the project class
        for field in schema_data:
            field_id = field['id']
            field_name = field['name']
            cls.schema_data[field_name] = field_id
            field_schema_type = field['schema']['type']
            field_schema_custom = field['schema']['custom']
            field_key = field_name.lower().replace(' ', '_')

            # Define the getter function for each field
            def getter_func(issue_key, field_id=field_id):
                issue_url = f"{cls.base_url}/rest/api/3/issue/{issue_key}"
                response = requests.get(issue_url, auth=cls.auth)

                if response.status_code != 200:
                    raise Exception(f"Failed to fetch issue data for {issue_key}. "
                                    f"Status: {response.status_code}, Response: {response.text}")

                issue_data = response.json()
                
                field_value = issue_data.get('fields', {}).get(field_id, None)
                return field_value

            getter_name = f"get_{field_key}"

            setattr(cls, getter_name, getter_func)

            cls._field_getters[field_key] = getter_name

        return cls

def get_value_in_jira_format(user_key, **kwargs):
    value_to_payload_converter_methods = {
        "Description": get_description_in_adf_format,
    }
    try:
        return value_to_payload_converter_methods[user_key](**kwargs)
    except KeyError:
        return kwargs.get("value", None)


class JiraProjectManager(metaclass=JiraMetaClass, base_url="https://your-domain.atlassian.net", auth=("your-email@example.com", "your-api-token")):
    def __init__(self, base_url, auth, issue_key):
        self.base_url = base_url
        self.auth = auth
        self.issue_key = issue_key
        self.project_cache = {}
        self.fields = {}
        self.issue_types_cache = {}
        self.logger = logging.getLogger(__name__)

    def get_project_id(self, project_key):
        if project_key in self.project_cache:
            print(f"Fetching cached project ID for key: {project_key}")
            return self.project_cache[project_key]

        url = f"{self.base_url}/rest/api/3/project/{project_key}"
        response = requests.get(url, auth=self.auth)

        if response.status_code == 200:
            project_data = response.json()
            project_id = project_data["id"]

            self.project_cache[project_key] = project_id
            self.fields = project_data
            return {"id": project_id}
        else:
            raise Exception(f"Failed to fetch project ID for {project_key}. "
                            f"Status Code: {response.status_code}, Response: {response.text}")

    def get_project_issue_types(self, project_key):
        """
        Get and cache the issue types (names as keys, IDs as values) for a given project key.
        :param project_key: The key of the Jira project.
        :return: A dictionary mapping issue type names to their IDs.
        """
        if project_key in self.issue_types_cache:
            print(f"Fetching cached issue types for project key: {project_key}")
            return self.issue_types_cache[project_key]

        url = f"{self.base_url}/rest/api/3/project/{project_key}"
        response = requests.get(url, auth=self.auth)

        if response.status_code == 200:
            project_data = response.json()
            issue_types = project_data.get("issueTypes", [])
            
            issue_type_mapping = {issue_type["name"]: issue_type["id"] for issue_type in issue_types}
            
            self.issue_types_cache[project_key] = issue_type_mapping
            return issue_type_mapping
        else:
            raise Exception(f"Failed to fetch issue types for project {project_key}. "
                            f"Status Code: {response.status_code}, Response: {response.text}")

    def get_issue_type_id(self, project_key, issue_type_name):
        """
        Get the ID of a specific issue type for a given project.
        :param project_key: The key of the Jira project.
        :param issue_type_name: The name of the issue type.
        :return: The ID of the issue type if found, otherwise raise an exception.
        """
        # Get the cached issue types or fetch them if not already cached
        issue_types = self.get_project_issue_types(project_key)

        # Check if the issue type name exists in the cached dictionary
        issue_type_id = issue_types.get(issue_type_name)
        if issue_type_id:
            return {"id": issue_type_id}
        else:
            raise ValueError(f"Issue type '{issue_type_name}' not found for project '{project_key}'.")

    def get_field_by_name(self, field_name):
        field_key = field_name.lower().replace(' ', '_')

        if field_key in self._field_getters:
            getter_method_name = self._field_getters[field_key]
            return getattr(self, getter_method_name)()
        else:
            raise AttributeError(f"No such field: {field_name}")

    def get_all_getters(self):
        return {field_name: getattr(self, method_name) for field_name, method_name in self._field_getters.items()}


    def translate_fields(self, issue_data):
        """
        Translate user-facing Jira field names to backend names based on the mapping.
        """
        self.logger.debug(f"Translating fields for issue: {issue_data}")
        translated_data = {}
        translated_data['project'] = self.get_project_id(issue_data.pop('Project'))
        translated_data['issuetype'] = self.get_issue_type_id(issue_data.pop('Issue Type'))
        for user_field, value in issue_data.items():
            backend_field = self.schema_data.get(user_field, user_field)
            translated_data[backend_field] = get_value_in_jira_format(user_field, value=value)
        self.logger.debug(f"Translated issue: {translated_data}")
        return translated_data
        
    def batch_create_payload(self, issues_data):
        """
        Batch create Jira issues by translating field names and sending REST requests.
        """
        # self.logger.debug(f"Preparing to create issues in Jira: {jira_url}")
        translated_issues = []
        for issue in issues_data:
            translated_issue = {
                "fields": self.translate_fields(issue)
            }
            translated_issues.append(translated_issue)
        self.payload = {
            "issueUpdates": translated_issues
        }

    def post_batch_create_request(self, jira_url, auth):
        """
        Send request for payload prepared in self.payload
        """
        url = f"{jira_url}/rest/api/3/issue/bulk"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        try:
            self.logger.info("Sending batch issue creation request to Jira")
            response = requests.post(url, auth=auth, headers=headers, json=self.payload)
            response.raise_for_status()
            self.logger.info("Issues created successfully")
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error creating issues in Jira: {e}")
            raise
