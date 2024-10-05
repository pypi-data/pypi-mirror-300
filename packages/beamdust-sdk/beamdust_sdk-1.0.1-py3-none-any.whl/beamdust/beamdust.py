import json
import logging
import requests
import urllib3
import inspect
import webbrowser
import os
import re
import keyword
from jinja2 import Environment, FileSystemLoader
from types import MethodType
from urllib.parse import urlparse
from beamdust.config import DEFAULT_CONFIG, LOG_CONFIG, DOCUMENTATION_CONFIG
from beamdust.exceptions import LoginError, APICallError, MethodNotFoundError

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure the logger
logging.basicConfig(**LOG_CONFIG)
logger = logging.getLogger(__name__)

class Beamdust:
    LOGIN_URI = "/backend/api/v1/users/login"
    JSON_DOCS_URI = "/backend/swagger/doc.json"

    def __getattr__(self, name):
        logger.error(f"Method '{name}' not found.")
        raise MethodNotFoundError(name)

    def __init__(self, base_url=None, email=None, password=None):
        logger.info("Initializing Beamdust instance.")
        self.base_url = self._validate_base_url(base_url or DEFAULT_CONFIG["base_url"])
        self.token = None
        self.host = None
        self.base_path = None
        self._endpoints = {}
        self.swagger_spec = None
        self.blocked_functions = DEFAULT_CONFIG.get("blocked_functions", [])

        # Auto-login if credentials provided
        if email and password:
            logger.debug(f"Auto-logging in with email: {email}")
            self._login_swagger(email, password)

        # Load Swagger endpoints
        self._load_swagger()

    def _validate_base_url(self, base_url):
        logger.debug(f"Validating base URL: {base_url}")
        parsed_url = urlparse(base_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            logger.error(f"Invalid base URL: {base_url}")
            raise ValueError(f"Invalid base URL: {base_url}")
        return f"{parsed_url.scheme}://{parsed_url.netloc}"

    def _load_swagger(self):
        try:
            logger.info("Loading Swagger specification.")
            response = requests.get(f"{self.base_url}{self.JSON_DOCS_URI}", verify=False)
            response.raise_for_status()
            self.swagger_spec = response.json()

            self.host = self.swagger_spec.get('host')
            self.base_path = self.swagger_spec.get('basePath', '')

            for path, methods in self.swagger_spec.get('paths', {}).items():
                for method, details in methods.items():
                    func_name = details['operationId']

                    # Skip blocked functions
                    if func_name in self.blocked_functions:
                        logger.info(f"Skipping blocked function: {func_name}")
                        continue

                    url = f"https://{self.host}{self.base_path}{path}"

                    # Generate method name in snake_case
                    snake_case_func_name = self._make_valid_identifier(func_name)
                    self._create_method(snake_case_func_name, method, url, details)

        except requests.RequestException as e:
            logger.error(f"Failed to load Swagger specification: {e}")
            raise APICallError(
                "Failed to load Swagger specification",
                status_code=e.response.status_code if e.response else None,
                response=e.response,
                url=self.base_url + self.JSON_DOCS_URI
            )

    def _get_schema_example(self, schema_ref):
        # Get schema definition from the reference
        ref_path = schema_ref.split('/')
        definition = self.swagger_spec
        for key in ref_path[1:]:
            definition = definition.get(key, {})
        return self._build_example_from_schema(definition)

    def _build_example_from_schema(self, schema):
        if schema.get("type") == "object":
            return {prop: self._build_example_from_schema(details)
                    for prop, details in schema.get("properties", {}).items()}
        elif schema.get("type") == "array":
            return [self._build_example_from_schema(schema.get("items", {}))]
        else:
            return schema.get("example", "sample_value")

    def _make_valid_identifier(self, s):
        s = re.sub(r'\W|^(?=\d)', '_', s)
        if keyword.iskeyword(s):
            s += '_'
        s = re.sub(r'([a-z])([A-Z])', r'\1_\2', s).lower()
        return s

    def _create_method(self, func_name, http_method, url, details):
        if not func_name.isidentifier():
            func_name = self._make_valid_identifier(func_name)

        def api_method(self, body=None, _help=False, **kwargs):
            """
            Auto-generated method for API endpoint.
            If _help is passed as True, it returns information about the body parameters.
            """
            if _help:
                for param in details.get("parameters", []):
                    if param.get("in") == "body" and param.get("schema", {}).get("$ref"):
                        schema_ref = param['schema']['$ref']
                        return {"Body Example": self._get_schema_example(schema_ref)}
                return {"Message": "This endpoint does not require a body."}

            if not self.token:
                logger.error("Authentication required. Please log in.")
                raise LoginError("Authentication required! Please log in.")

            headers = kwargs.pop("headers", {})
            params = kwargs.pop("params", {})
            # Use the first argument as the body
            headers["Cookie"] = f"Auth={self.token}"
            headers["Content-Type"] = "application/json"

            try:
                logger.debug(f"Making API request to {url} with method {http_method}")
                response = requests.request(http_method, url, headers=headers, params=params, json=body, verify=False)
                response.raise_for_status()
                logger.info(f"API request successful: {url}")
                return response.json()
            except requests.RequestException as e:
                logger.error(f"API request error: {e}")
                raise APICallError(f"API request error", status_code=e.response.status_code if e.response else None, response=e.response, url=url)

        api_method.__doc__ = details.get("description", "No description available.")
        bound_method = MethodType(api_method, self)
        setattr(self, func_name, bound_method)
        self._endpoints[func_name] = {"method": http_method, "url": url}


    def _login_swagger(self, email, password):
        login_payload = {"email": email, "password": password}
        try:
            logger.info(f"Logging in user: {email}")
            response = requests.post(f"{self.base_url}{self.LOGIN_URI}", json=login_payload, verify=False)
            response.raise_for_status()  
            self.token = response.json().get("token")
            logger.info("Login successful.")
        except requests.HTTPError as e:
            error_message = e.response.json().get('message', 'Unknown error')
            logger.error(f"Login failed: {error_message} (Status Code: {e.response.status_code})")
            raise LoginError(f"Login failed: {error_message} (Status Code: {e.response.status_code})")
        except requests.RequestException as e:
            logger.error(f"Login error: {e}")
            raise LoginError(f"Login error: {e.response.json() if e.response else 'Unknown error'}")

    def get_available_functions(self):
        """
        Return a dictionary of available API methods with their HTTP methods and URLs.
        """
        logger.info("Returning available API methods.")
        return self._endpoints

    def generate_documentation(self):
        """
        Generate documentation based on available API functions and open it in the browser.
        """
        logger.info("Generating documentation.")
        available_functions = self.get_available_functions()

        # Retrieve text and settings from DOCUMENTATION_CONFIG
        package_name = DOCUMENTATION_CONFIG["package_name"]
        introduction = DOCUMENTATION_CONFIG["introduction"]
        usage = DOCUMENTATION_CONFIG["usage"]
        help_options = DOCUMENTATION_CONFIG["help_options"]
        output_file = DOCUMENTATION_CONFIG["output_file"]

        # Collect information about each endpoint
        endpoints = {}
        for func_name, details in available_functions.items():
            try:
                method = getattr(self, func_name)
                docstring = inspect.getdoc(method)
                help_info = method(_help=True)

                if isinstance(help_info, dict) and help_info.get('Message'):
                    body_example = json.dumps({}, indent=4) 
                else:
                    body_example = json.dumps(help_info, indent=4)
            except Exception:
                docstring = "No description available."
                body_example = json.dumps({}, indent=4)  # Default to empty body on exception

            endpoints[func_name] = {
                "method": details["method"].upper(),
                "url": details["url"],
                "description": docstring,
                "body_example": body_example  
            }

        # Using Jinja2 to insert dynamic data into template
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('documentation_template.html')

        # Render the template with data
        rendered_html = template.render(
            package_name=package_name,
            introduction=introduction,
            usage=usage,
            help_options=help_options,
            endpoints=endpoints
        )

        # Write to an HTML file
        with open(output_file, "w") as f:
            f.write(rendered_html)
            logger.info("Documentation generated successfully.")

        # Open the generated HTML file in the browser
        abs_path = os.path.abspath(output_file)
        webbrowser.open(f"file://{abs_path}")

