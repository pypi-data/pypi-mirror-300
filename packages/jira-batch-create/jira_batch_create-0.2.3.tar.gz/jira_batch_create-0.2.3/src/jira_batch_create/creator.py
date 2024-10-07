import csv
import json
import logging
import os
import requests

from cffi import FFI
from dotenv import load_dotenv

load_dotenv()
ssl_verify = os.getenv('SSLVerify', True)
if ssl_verify == 'False':
    ssl_verify = False

class JiraMetaClass(type):
    def __new__(mcs, name, bases, dct, ssl_verify=ssl_verify):
        cls = super().__new__(mcs, name, bases, dct)
        cls.ssl_verify=ssl_verify
        auth = (os.getenv('JiraUser'), os.getenv('JiraToken'))
        base_url = os.getenv('JiraUrl')
        if not base_url or not auth:
            raise ValueError("JiraUser, JiraToken and JiraUrl must be provided in .env file to fetch project schema.")

        # Fetch the project schema fields from Jira
        schema_url = f"{base_url}/rest/api/3/field"
        response = requests.get(schema_url, auth=auth, verify=ssl_verify)

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
            # field_schema_type = field['schema']['type']
            # field_schema_custom = field['schema']['custom']
            field_key = field_name.lower().replace(' ', '_')

            # Define the getter function for each field
            def getter_func(issue_key, field_id=field_id):
                issue_url = f"{cls.base_url}/rest/api/3/issue/{issue_key}"
                response = requests.get(issue_url, auth=cls.auth, verify=ssl_verify)

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
    
def get_parent_in_dict(**kwargs):
    parent = kwargs.get('value')
    return {'key': parent}


def get_description_in_adf_format(**kwargs):
    description = kwargs.get("value")
    ffi = FFI()
    lib = ffi.dlopen("htmltoadf.dll")
    ffi.cdef("char * convert(char *);")
    desc = description.encode('utf-8')
    converted_text = json.loads(ffi.string(lib.convert(desc)).decode('utf-8'))
    return converted_text


def get_value_in_jira_format(user_key, **kwargs):
    value_to_payload_converter_methods = {
        "Description": get_description_in_adf_format,
        "Parent": get_parent_in_dict
    }
    try:
        return value_to_payload_converter_methods[user_key](**kwargs)
    except KeyError:
        return kwargs.get("value", None)


class JiraProjectManager(metaclass=JiraMetaClass):
    def __init__(self):
        self.project_cache = {}
        self.fields = {}
        self.issue_types_cache = {}
        self.logger = logging.getLogger(__name__)

    def get_project_id_in_dict(self, project_key):
        if project_key in self.project_cache:
            self.logger.debug(f"Fetching cached project ID for key: {project_key}")
            return {'id': self.project_cache[project_key]}

        url = f"{self.base_url}/rest/api/3/project/{project_key}"
        response = requests.get(url, auth=self.auth, verify=self.ssl_verify)

        if response.status_code == 200:
            project_data = response.json()
            project_id = project_data["id"]

            self.project_cache[project_key] = project_id
            self.fields = project_data
            return {"id": project_id}
        else:
            raise Exception(f"Failed to fetch project ID for {project_key}. "
                            f"Status Code: {response.status_code}, Response: {response.text}")
        
    def get_issue_type_id_in_dict(self, project_key, issue_type_name):
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

    def get_project_issue_types(self, project_key):
        """
        Get and cache the issue types (names as keys, IDs as values) for a given project key.
        :param project_key: The key of the Jira project.
        :return: A dictionary mapping issue type names to their IDs.
        """
        if project_key in self.issue_types_cache:
            self.logger.debug(f"Fetching cached issue types for project key: {project_key}")
            return self.issue_types_cache[project_key]

        url = f"{self.base_url}/rest/api/3/project/{project_key}"
        response = requests.get(url, auth=self.auth, verify=self.ssl_verify)

        if response.status_code == 200:
            project_data = response.json()
            issue_types = project_data.get("issueTypes", [])
            issue_type_mapping = {issue_type["name"]: issue_type["id"] for issue_type in issue_types}
            self.issue_types_cache[project_key] = issue_type_mapping
            return issue_type_mapping
        else:
            raise Exception(f"Failed to fetch issue types for project {project_key}. "
                            f"Status Code: {response.status_code}, Response: {response.text}")

    def get_field_by_name(self, field_name, issue_key):
        field_key = field_name.lower().replace(' ', '_')

        if field_key in self._field_getters:
            getter_method_name = self._field_getters[field_key]
            return getattr(self, getter_method_name)(issue_key)
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
        project = issue_data.pop('Project')
        translated_data['project'] = self.get_project_id_in_dict(issue_data.pop('Project'))
        translated_data['issuetype'] = self.get_issue_type_id_in_dict(project, issue_data.pop('Issue Type'))
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
        self.issues_data = issues_data
        translated_issues = []
        for issue in issues_data:
            translated_issue = {
                "fields": self.translate_fields(issue)
            }
            translated_issues.append(translated_issue)
        self.payload = {
            "issueUpdates": translated_issues
        }

    def post_batch_create_issues(self):
        """
        Send request for payload prepared in self.payload
        """
        def post_create_request(batch_payload):
            url = f"{self.base_url}/rest/api/3/issue/bulk"
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            try:
                
                response = requests.post(url, auth=self.auth, headers=headers, json=batch_payload, verify=self.ssl_verify)
                response.raise_for_status()
                self.logger.debug("Issues created successfully")
                return response.json()
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error creating issues in Jira: {e}")
                raise

        self.logger.info("Sending batch issue creation request to Jira")

        batch_size = 50  # JIRa endpoint creates upto 50 issues
        issues = []
        errors = []
        self.logger.debug('Sending batch issues creation request to Jira')
        for i in range (0, len(self.payload['issueUpdates']), batch_size):
            self.logger.debug(f'Processing issues batch: {i}:{i+batch_size}')
            batch = self.payload['issueUpdates'][i:i+batch_size]
            response = post_create_request({'issueUpdates':batch})
            issues.extend(response['issues'])
            errors.extend(response['errors'])
            if response['errors']:
                self.logger.warning(f'Errors during processing batch: {i}-{i+batch_size}')
            for n in range(i, i+len(response['issues'])):
                self.issues_data[n].update({'self':response['issues'][n-i]})
            self.logger.debug("Batch create issues finished.")
        return {
            'issues': issues,
            'errors': errors
        }
    
    def save_created_issues_json(self, filenanme, indent=None):
        with open(filenanme, 'w') as file:
            file.write(json.dumps(self.issues_data, indent=indent))
