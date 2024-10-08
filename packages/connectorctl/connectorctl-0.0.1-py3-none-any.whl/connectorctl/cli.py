#!/Users/girish/Desktop/workspace/py310/bin/python
import argparse
import json
import logging
import os
import sys

import requests
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()

TABLE_FORMAT = ['grid', 'simple', 'double_outline', 'fancy_grid', 'fancy_outline']
SELECTED_TABLE_FORMAT = TABLE_FORMAT[3]


def load_config():
    """
    Load the Kafka environment config from the JSON file

    Returns:
        dict: Kafka configuration (env, user, password, cert paths, server, port)
    """
    try:
        if os.path.exists(KafkaConnectorManager.CONFIG_FILE):
            with open(KafkaConnectorManager.CONFIG_FILE, "r") as config_file:
                return json.load(config_file)
    except Exception as e:
        print(f"Error loading config: {e}")

    return {"current_context": None, "environments": {}}


def setup_logger(log_file):
    """
    Set up the logger to capture errors and write to the specified log file.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create a file handler for logging
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.ERROR)

    # # Create a console handler for logging (optional)
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.DEBUG)

    # Set a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    # console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    # logger.addHandler(console_handler)

    return logger


class KafkaConnectorManager:
    CONFIG_DIR = os.path.expanduser("~/.connector_cli")
    CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

    def __init__(self, env, args):
        """
        Class constructor

        Args:
            env (str): The Kafka environment (e.g., dev, prod)
            args (Namespace): Parsed arguments from argparse
        """
        self.env = env
        self.args = args

        # Ensure the configuration directory exists
        self.ensure_config_dir()

        # Setup logger
        self.logger = setup_logger(os.path.join(KafkaConnectorManager.CONFIG_DIR, 'connectorctl.log'))

        # Load saved configuration
        self.config = load_config()
        self.active_env = self.get_active_env()


    def get_active_env(self):
        """
        Get the active environment from the config.

        Returns:
            dict: The active environment details.
        """
        env_name = self.config.get('current_context')
        if env_name:
            return self.config['environments'][env_name]
        else:
            self.logger.error("No active environment found. Set an environment first.")
            print("No active environment found. Set an environment first.")
            return None

    @staticmethod
    def ensure_config_dir():
        """
        Ensure the configuration directory exists
        """
        if not os.path.exists(KafkaConnectorManager.CONFIG_DIR):
            os.makedirs(KafkaConnectorManager.CONFIG_DIR)

    def save_config(self):
        """
        Save the Kafka environment config to a JSON file

        Args:
            env (str): Kafka environment (e.g., dev, stage)
            user (str): Kafka user
            password (str): Kafka password
            cacert (str): Path to the CA certificate
            key (str): Path to the key file
            cer (str): Path to the certificate file
            server (str): Kafka server host URL
            port (int): Kafka server port
        """
        KafkaConnectorManager.ensure_config_dir()

        with open(KafkaConnectorManager.CONFIG_FILE, "w") as config_file:
            json.dump(self.config, config_file, indent=4)

    def set_env(self, args):
        # Save environment details
        env_name = args.env
        self.config['environments'][env_name] = {
            "user": args.user,
            "password": args.password,
            "cacert": args.cacert,
            "key": args.key,
            "cer": args.cer,
            "server": args.server,
            "port": args.port,
        }
        # Set it as the current context
        self.config['current_context'] = env_name
        self.save_config()
        print(f"Environment '{env_name}' is set and activated.")

    def use_env(self, env_name):
        # Switch active environment context
        if env_name in self.config['environments']:
            self.config['current_context'] = env_name
            self.save_config()
            print(f"Switched to environment: {env_name}")
        else:
            msg = f"Environment '{env_name}' not found. Use 'set-env' to add it."
            self.logger.error(msg)
            print(msg)

    def get_current_env(self):
        # Display current environment details
        env_name = self.config.get('current_context')
        if not env_name:
            msg = "No active environment found. Set an environment first using 'set-env'."
            self.logger.error(msg)
            print(msg)
            return
        env_details = self.config['environments'][env_name]
        print(f"Current Environment: {env_name}")
        for key, value in env_details.items():
            print(f"{key}: {value}")

    def list_envs(self):
        # List all environments
        if not self.config['environments']:
            print("No environments configured.")
        else:
            print("Available Environments:")
            for env_name in self.config['environments']:
                current_marker = " (current)" if env_name == self.config['current_context'] else ""
                print(f"- {env_name}{current_marker}")

    def fetch_url(self):
        """
        Fetches the URL for Kafka connectors based on the environment

        Returns:
            str: The URL for Kafka connectors
        """
        protocol = "https" if self.active_env.get('cacert') is not None else "http"
        return f"{protocol}://{self.active_env['server']}:{self.active_env['port']}"

    def get_password(self):
        """
        Placeholder function for potentially retrieving password securely
        """
        return ""

    def request_kafka(self, method, endpoint, data=None):
        """
        Sends a request to the Kafka connector API

        Args:
            method (str): The HTTP method for the request (e.g., GET, POST)
            endpoint (str): The API endpoint for Kafka connectors
            data (dict, optional): Data to send in the request body (default: None)

        Returns:
            requests.Response: The response object from the HTTP request
        """
        if not self.active_env:
            self.logger.error("No active environment to execute commands.")
            print("No active environment to execute commands.")
            return
        url = f"{self.fetch_url()}{endpoint}"
        headers = {
            "Content-Type": "application/json",
        }
        response = None
        try:
            auth = requests.auth.HTTPBasicAuth(self.active_env.get('user'), self.active_env.get('password'))

            if self.active_env.get('cacert'):
                # Combine username and password for authentication
                response = requests.request(
                    method,
                    url,
                    headers=headers,
                    auth=auth,
                    data=json.dumps(data) if data else None,
                    verify=self.active_env.get('cacert'),
                    cert=(self.active_env.get('cer'), self.active_env.get('key')),
                )
            else:
                response = requests.request(
                    method, url, headers=headers, auth=auth, data=json.dumps(data) if data else None
                )

            response.raise_for_status()
            # return response

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error: {e}")
            # print(f"Error: {e}")
        return response

    def get_connector_status(self, connectors):
        status_data = []
        for connector in connectors:
            status = self._fetch_connector_status(connector)
            status_data.append([connector, status])

        self._display_status_table(status_data)

    def _fetch_connector_status(self, connector):
        try:
            response = self.request_kafka("GET", f"/connectors/{connector}/status")
            if response is None or not response.ok:
                return f"Error: Status code {response.status_code if response else 'N/A'}"

            status_json = response.json()
            return status_json.get("connector", {}).get("state", "Unknown")
        except Exception as e:
            return f"Error: {str(e)}"

    def _display_status_table(self, status_data):
        headers = ["Connector Name", "Status"]
        table = tabulate(status_data, headers=headers, tablefmt=SELECTED_TABLE_FORMAT)
        print(table)

    def get_connector_config(self, connector):
        config = self._fetch_connector_config(connector)
        if config:
            self._display_config(connector, config)

    def _fetch_connector_config(self, connector):
        response = self.request_kafka("GET", f"/connectors/{connector}/config")
        if response is None or not response.ok:
            # print(f"Failed to get config for connector {connector}. Status code: {response.status_code if response else 'N/A'}")
            print(f"Connector '{connector}' not found. Please check the name and try again.")
            exit(1)
            # return None

        try:
            return response.json()
        except json.JSONDecodeError:
            print(f"Failed to parse response for connector {connector}. Response text: {response.text}")
            return None

    def _display_config(self, connector, config):
        print(f"Configuration for connector: {connector}")

        table_data = []
        for key, value in config.items():
            json_value = json.dumps(value, indent=2) if isinstance(value, (dict, list)) else value
            table_data.append([key, json_value])

        headers = ["Config Key", "Value"]
        table = tabulate(table_data, headers=headers, tablefmt=SELECTED_TABLE_FORMAT)
        print(table)

        # # Convert the config dictionary to a list of lists
        # table_data = [[key, value] for key, value in config.items()]
        # # Create and print the table
        # table = tabulate(table_data, headers=["Config Key", "Value"], tablefmt=SELECTED_TABLE_FORMAT)
        # print(f"Configuration for connector: {connector}")
        # print(table)
        print("\nComplete JSON response:")
        print(json.dumps(config, indent=4))

    def _display_action_table(self, action_title, results):
        """
        Display a table showing the action (restart, pause, resume) and results for each connector.

        Args:
            action_title (str): Title of the action being performed (e.g., "Restart Results")
            results (list of lists): Each list contains [connector, result_message]
        """
        print(f"\n{action_title}:\n")
        headers = ["Connector Name", "Result"]
        table = tabulate(results, headers=headers, tablefmt=SELECTED_TABLE_FORMAT)
        print(table)

    def handle_command(self):
        """
        Executes a command to manage Kafka connectors
        """
        command = self.args.command
        method = "GET"

        if command == "list":
            print(f"\nList the connectors for {self.env}\n")
            response = self.request_kafka(method, "/connectors")
            if not response:
                return
            connectors = response.json()
            table = tabulate(
                [[connector] for connector in connectors],
                headers=["Connector Name"],
                tablefmt=SELECTED_TABLE_FORMAT,
            )
            print(table)

        elif command == "get":
            if not self.args.connector:
                print("Please provide a connector name for the get operation")
                return
            connector = self.args.connector
            # print(f"\nGet the connector config: {connector} for {self.env}\n")
            self.get_connector_config(connector)

        elif command == "status":
            connectors = [self.args.connector] if self.args.connector else self.request_kafka(method, "/connectors").json()
            print(f"\nGet the connector status for {self.env}\n")
            self.get_connector_status(connectors)

        elif command == "create":
            if self.args.config:
                try:
                    # Try to load the config from the provided JSON string
                    data = json.loads(self.args.config)
                except json.JSONDecodeError as e:
                    print(f"Invalid JSON string provided: {e}")
                    return
            elif self.args.config_file:
                try:
                    # If a config file is provided, load it
                    with open(self.args.config_file) as config_file:
                        data = json.load(config_file)
                except Exception as e:
                    print(f"Error reading config file: {e}")
                    return
            else:
                print("Please provide either a JSON string or a config file for the create operation.")
                return
            print(f"\nCreating the connector in {self.env}\n")
            self.request_kafka("POST", "/connectors", data=data)
            print("\nConnector created successfully.\n")
            self.get_connector_config(data["name"])

        elif command == "update":
            if self.args.config:
                try:
                    # Try to load the config from the provided JSON string
                    data = json.loads(self.args.config)
                except json.JSONDecodeError as e:
                    print(f"Invalid JSON string provided: {e}")
                    return
            elif self.args.config_file:
                try:
                    # If a config file is provided, load it
                    with open(self.args.config_file) as config_file:
                        data = json.load(config_file)
                except Exception as e:
                    print(f"Error reading config file: {e}")
                    return
            else:
                print("Please provide either a JSON string or a config file for the update operation.")
                return
            if not self.args.connector:
                print("Please provide a connector name for the update operation.")
                return
            connector = self.args.connector
            self.get_connector_config(connector)
            # response = self.request_kafka("GET", f"/connectors/{connector}/config")
            # if response is None or not response.ok:
            #     print(f"Connector '{connector}' not found. Please check the name and try again.")
            #     return
            # If the connector exists, proceed with the update
            print(f"\nUpdating the connector in {self.env}\n")
            self.request_kafka("PUT", f"/connectors/{connector}/config", data=data)
            print("\nConnector updated successfully.\n")
            self.get_connector_config(self.args.connector)

        elif command == "delete":
            if not self.args.connector:
                print("Please provide a connector name for the delete operation")
                return
            connector = self.args.connector
            self.get_connector_config(connector)
            print(f"\nDeleting the connector: {connector} for {self.env}\n")
            self.request_kafka("DELETE", f"/connectors/{connector}")
            print("\nConnector deleted successfully.\n")
            self.get_connector_status([connector])

        elif command == "restart":
            connectors = [self.args.connector] if self.args.connector else self.request_kafka(method, "/connectors").json()
            results = []
            for connector in connectors:
                print(f"Restarting connector: {connector} ...")
                response = self.request_kafka("POST", f"/connectors/{connector}/restart")
                if response and response.ok:
                    results.append([connector, "Restarted successfully"])
                else:
                    results.append([connector, f"Failed to restart (Status code: {response.status_code if response else 'N/A'})"])

            # Display results in table format
            self._display_action_table("Restart Results", results)

        elif command == "pause":
            connectors = [self.args.connector] if self.args.connector else self.request_kafka(method, "/connectors").json()
            results = []
            for connector in connectors:
                print(f"Pausing connector: {connector} ...")
                response = self.request_kafka("PUT", f"/connectors/{connector}/pause")
                if response and response.ok:
                    results.append([connector, "Paused successfully"])
                else:
                    results.append([connector, f"Failed to pause (Status code: {response.status_code if response else 'N/A'})"])

            # Display results in table format
            self._display_action_table("Pause Results", results)

        elif command == "resume":
            connectors = [self.args.connector] if self.args.connector else self.request_kafka(method, "/connectors").json()
            results = []
            for connector in connectors:
                print(f"Resuming connector: {connector} ...")
                response = self.request_kafka("PUT", f"/connectors/{connector}/resume")
                if response and response.ok:
                    results.append([connector, "Resumed successfully"])
                else:
                    results.append([connector, f"Failed to resume (Status code: {response.status_code if response else 'N/A'})"])

            # Display results in table format
            self._display_action_table("Resume Results", results)

        elif command == "set-env":
            self.set_env(self.args)
            print(f"Environment set to: {self.args.env}")
        elif command == "use-env":
            self.use_env(self.args.env)
        elif command == "get-env":
            self.get_current_env()
        elif command == "list-env":
            self.list_envs()
        else:
            print(f"Unknown command: {command}")


def main():
    """
    Main function - starting point of the script

    Parses command-line arguments and creates a KafkaConnectorManager object.
    """
    parser = argparse.ArgumentParser(description="Kafka Connect Management CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Connector commands
    subparsers.add_parser("list", help="List all connectors")
    parser_get = subparsers.add_parser("get", help="Get a connector config")
    parser_get.add_argument("connector", help="Connector name")
    parser_status = subparsers.add_parser("status", help="Get connector status")
    parser_status.add_argument("connector", help="Connector name", nargs="?")
    parser_create = subparsers.add_parser("create", help="Create a connector")
    parser_create.add_argument("config", help="Connector configuration as a JSON string")
    # Create a connector with either a config file or JSON string
    parser_create.add_argument("--config-file", help="Connector config JSON file")
    # parser_create.add_argument("--config-json", help="Connector configuration as a JSON string")

    parser_update = subparsers.add_parser("update", help="Update a connector")
    parser_update.add_argument("connector", help="Connector name")
    parser_update.add_argument("config", help="Connector config JSON file")
    parser_delete = subparsers.add_parser("delete", help="Delete a connector")
    parser_delete.add_argument("connector", help="Connector name")
    parser_restart = subparsers.add_parser("restart", help="Restart a connector")
    parser_restart.add_argument("connector", help="Connector name", nargs="?")
    parser_pause = subparsers.add_parser("pause", help="Pause a connector")
    parser_pause.add_argument("connector", help="Connector name", nargs="?")
    parser_resume = subparsers.add_parser("resume", help="Resume a connector")
    parser_resume.add_argument("connector", help="Connector name", nargs="?")

    # Environment commands
    parser_set_env = subparsers.add_parser("set-env", help="Set environment")
    parser_set_env.add_argument("env", help="Environment (dev, stage, prod)")
    parser_set_env.add_argument("--user", help="Kafka user")
    parser_set_env.add_argument("--password", help="Kafka password")
    parser_set_env.add_argument("--cacert", help="CA certificate file")
    parser_set_env.add_argument("--key", help="Key file")
    parser_set_env.add_argument("--cer", help="Certificate file")
    parser_set_env.add_argument("--server", help="Kafka server host URL", default="localhost")
    parser_set_env.add_argument("--port", help="Kafka server port", type=int, default=8083)

    # Use environment command (switch context)
    parser_use_env = subparsers.add_parser("use-env", help="Switch to a specific environment")
    parser_use_env.add_argument("env", help="Environment name to switch to")

    # Get current environment command
    subparsers.add_parser("get-env", help="Get current environment details")

    # List all environments command
    subparsers.add_parser("list-env", help="List all configured environments")

    # Load environment from config if not provided
    args = parser.parse_args()
    env = args.env if hasattr(args, "env") else load_config().get("current_context")

    if not env:
        print("Please set the environment using the 'set-env' command.")
        sys.exit(1)

    # Create KafkaConnectorManager instance and handle the command
    manager = KafkaConnectorManager(env, args)
    manager.handle_command()


if __name__ == "__main__":
    main()
