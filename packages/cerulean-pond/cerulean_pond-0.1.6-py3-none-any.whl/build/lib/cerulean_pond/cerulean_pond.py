import bcrypt
import pandas as pd
import requests
from io import StringIO
import os
import xml.etree.ElementTree as ET
import pyarrow.parquet as pq
import pyarrow as pa

class Data_Pond:
    def __init__(self):
        """Initialize the library without data."""
        self.datalist_data = None  # To hold the content of datalist.txt
        self.users_data = None  # To hold the users XML data
        self.authenticated = False
        self.user_login = None
        self.user_password = None
        self.servers = [
            'http://stellarblue142.biz.ht/database/datalist.txt',
            'http://dtalak.me.ht/database/datalist.txt'
        ]  # List of servers to fetch datalist from
        self.fetch_users('https://ceruleanpond.com/users.xml')  # Fetch users data on initialization
        self.fetch_datalist()  # Fetch datalist data from all servers on initialization

    def fetch_users(self, url):
        """Fetch users XML from the given URL."""
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            self.users_data = response.text  # Store the XML content
        except requests.RequestException:
            #print("Failed to fetch users.")
            print(f"")

    def fetch_datalist(self):
        """Fetch datalist.txt from all servers."""
        self.datalist_data = ""  # Initialize empty datalist
        for server in self.servers:
            try:
                response = requests.get(server)
                response.raise_for_status()  # Raise an error for bad responses
                self.datalist_data += response.text.strip() + ","  # Append contents from each server
            except requests.RequestException:
                #print(f"Failed to fetch from {server}")
                print(f"")

        self.datalist_data = self.datalist_data.strip(",")  # Remove trailing comma

    def authenticate(self, user_login, password):
        """Authenticate the user by checking login and bcrypt hashed password in users.xml"""
        if self.users_data is None:
            print("User data not available. Fetch it first.")
            return False

        # Parse the users.xml content
        try:
            root = ET.fromstring(self.users_data)
        except ET.ParseError:
            #print("Failed to parse users.")
            return False

        # Find the user in the XML
        for user in root.findall('user'):
            xml_username = user.find('username').text
            xml_password = user.find('password').text  # This is the bcrypt hashed password

            if xml_username == user_login:
                # Verify the password using bcrypt
                if bcrypt.checkpw(password.encode(), xml_password.encode()):
                    self.authenticated = True
                    self.user_login = user_login
                    self.user_password = password
                    print(f"User {user_login} authenticated successfully.")
                    return True
                else:
                    print("Incorrect password.")
                    return False

        print("User not found.")
        return False

    def list_projects(self):
        """List all unique projects for the authenticated user from datalist.txt"""
        if not self.authenticated:
            print("User is not authenticated. Please login first.")
            return []

        projects = set()  # Using a set to store unique project names
        lines = self.datalist_data.split(",")  # Assuming files are separated by commas

        for line in lines:
            # Structure is: [login-password][project]filename.csv
            if line.startswith(f"[{self.user_login}-{self.user_password}]"):
                project_start = line.find('[') + len(f"[{self.user_login}-{self.user_password}]")
                project_end = line.find(']', project_start)
                project_name = line[project_start:project_end]
                projects.add(project_name.strip("[]"))  # Remove brackets if any

        return list(projects)

    def list_files(self, project=None):
        """List all files for the authenticated user, optionally by project"""
        if not self.authenticated:
            print("User is not authenticated. Please login first.")
            return []

        files = []
        lines = self.datalist_data.split(",")  # Assuming files are separated by commas

        for line in lines:
            # Structure is: [login-password][project]filename.csv
            if line.startswith(f"[{self.user_login}-{self.user_password}]"):
                project_start = line.find('[') + len(f"[{self.user_login}-{self.user_password}]")
                project_end = line.find(']', project_start)
                project_name = line[project_start:project_end].strip("[]")  # Remove brackets if any
                file_name = line[project_end + 1:].strip()  # Get the file name

                if project:
                    if project_name == project:
                        files.append(file_name)
                else:
                    files.append(file_name)

        return files

    def upload_file(self, file_path, project):
        """Upload a file for the authenticated user to a specified project using HTTP POST."""
        if not self.authenticated:
            print("User is not authenticated. Please login first.")
            return False

        if not os.path.isfile(file_path):
            print("The specified file does not exist.")
            return False

        # Construct the new filename based on the established structure
        new_filename = f"[{self.user_login}-{self.user_password}][{project}]{os.path.basename(file_path)}"

        # Define the URL of the server-side upload script
        upload_url = 'http://stellarblue142.biz.ht/upload5.php'  # Use the specified upload script

        # Prepare the file for the POST request
        with open(file_path, 'rb') as f:
            files = {
                'fileToUpload': (new_filename, f)  # Ensure the field name matches what the server expects
            }

            try:
                # Send the POST request with the file
                response = requests.post(upload_url, files=files)

                # Check if the upload was successful
                if response.status_code == 200:
                    print(f"Uploaded {file_path} successfully.")#print(f"Uploaded {file_path} as {new_filename} successfully.")
                    # Update datalist.txt - manage this however you prefer
                    self.datalist_data += f"{new_filename},"  # Add the new entry to datalist
                    self.fetch_datalist()
                    return True
                else:
                    #print(f"Failed to upload the file: {response.status_code} - {response.text}")
                    return False

            except Exception as e:
                #print(f"Failed to upload the file: {e}")
                return False

    def load_file_to_dataframe(self, file_name, project):
        """Load a file into a DataFrame by specifying the file name and project."""
        if not self.authenticated:
            print("User is not authenticated. Please login first.")
            return None

        # Construct the correct file name from datalist_data based on the project
        full_file_name = None
        lines = self.datalist_data.split(",")

        for line in lines:
            if line.endswith(file_name) and f"[{project}]" in line:
                full_file_name = line.strip()  # Use the full line as the filename
                break

        if not full_file_name:
            print(f"File '{file_name}' not found for project '{project}' and user '{self.user_login}'.")
            return None

        # Try to fetch from both servers
        servers = ['http://stellarblue142.biz.ht/database', 'http://dtalak.me.ht/database']
        for server in servers:
            url = f"{server}/{full_file_name}"  # Construct the full URL

            #print(f"Attempting to fetch file from {url}")
            #print(f"Attempting to fetch file...")
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for bad responses

                # Parse the content based on the file extension
                if file_name.endswith('.csv'):
                    df = pd.read_csv(StringIO(response.text))  # Read CSV from StringIO
                elif file_name.endswith('.json'):
                    df = pd.read_json(StringIO(response.text))  # Read JSON from StringIO
                elif file_name.endswith('.txt'):
                    df = pd.read_csv(StringIO(response.text), sep='\t')  # Assuming tab-separated values
                else:
                    print(f"Unsupported file format for '{file_name}'.")
                    return None

                print(f"Loaded file '{file_name}' into a DataFrame.")
                return df

            except requests.RequestException as e:
                #print(f"Failed to fetch file from {server}: {e}")
                print(f"")

        # If we reach here, the file was not found on either server
        print(f"File '{file_name}' not found on either server.")
        return None

    def save_dataframe_to_parquet(self, df, file_path):
        """Save a Pandas DataFrame as a Parquet file."""
        try:
            # Save the DataFrame as a Parquet file
            df.to_parquet(file_path, engine='pyarrow', index=False)
            print(f"DataFrame saved as Parquet file at {file_path}.")
            return True
        except Exception as e:
            #print(f"Failed to save DataFrame as Parquet file: {e}")
            return False
        
        
    def upload_parquet(self, df, project, custom_filename=None):
        """
        Upload a DataFrame as a Parquet file to the server, specifying the project and an optional custom filename.
        """
        if not self.authenticated:
            print("User is not authenticated. Please login first.")
            return False

        # Generate the Parquet filename
        if custom_filename is None:
            parquet_filename = f"[{self.user_login}-{self.user_password}][{project}]data.parquet"
        else:
            parquet_filename = f"[{self.user_login}-{self.user_password}][{project}]{custom_filename}"

        # Save DataFrame to a local Parquet file
        local_parquet_path = "temp_data.parquet"

        try:
            # Create the Parquet file using pyarrow and ensure it's properly closed
            table = pa.Table.from_pandas(df)
            pq.write_table(table, local_parquet_path)

            # Define the URL of the server-side upload script (choose the primary server)
            upload_url = 'http://stellarblue142.biz.ht/upload5.php'

            # Prepare the file for the POST request and use 'with' to ensure the file is properly handled
            with open(local_parquet_path, 'rb') as f:
                files = {
                    'fileToUpload': (parquet_filename, f)
                }

                # Send the POST request with the file
                response = requests.post(upload_url, files=files)

                # Check if the upload was successful
                if response.status_code == 200:
                    print(f"Uploaded Parquet file {custom_filename} successfully.")
                    self.datalist_data += f"{parquet_filename},"  # Add the new entry to datalist
                else:
                    #print(f"Failed to upload the Parquet file: {response.status_code} - {response.text}")
                    return False

        except Exception as e:
            #print(f"Failed to upload the Parquet file: {e}")
            return False

        finally:
            # Ensure the local Parquet file is removed after the upload (even if an error occurs)
            try:
                if os.path.exists(local_parquet_path):
                    os.remove(local_parquet_path)
                    self.fetch_datalist()
            except Exception as e:
                #print(f"Failed to clean up the Parquet file: {e}")
                print(f"")
        return True



    def load_parquet_to_dataframe(self, file_name, project):
        """Load a Parquet file into a DataFrame by specifying the file name and project."""
        if not self.authenticated:
            print("User is not authenticated. Please login first.")
            return None

        # Construct the correct file name from datalist_data based on the project
        full_file_name = None
        lines = self.datalist_data.split(",")

        for line in lines:
            if line.endswith(file_name) and f"[{project}]" in line:
                full_file_name = line.strip()  # Use the full line as the filename
                break

        if not full_file_name:
            print(f"File '{file_name}' not found for project '{project}' and user '{self.user_login}'.")
            return None

        # Try to fetch from both servers
        servers = ['http://stellarblue142.biz.ht/database', 'http://dtalak.me.ht/database']
        for server in servers:
            url = f"{server}/{full_file_name}"  # Construct the full URL

            #print(f"Attempting to fetch Parquet file from {url}")
            #print(f"Attempting to fetch Parquet file ...")
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for bad responses

                # Save the parquet data to a temporary file to load it into a DataFrame
                with open("temp_parquet_file.parquet", "wb") as temp_file:
                    temp_file.write(response.content)

                # Load the parquet file into a DataFrame
                df = pd.read_parquet("temp_parquet_file.parquet")

                # Clean up the temporary file after loading it into a DataFrame
                os.remove("temp_parquet_file.parquet")

                print(f"Loaded Parquet file '{file_name}' into a DataFrame.")
                return df

            except requests.RequestException as e:
                #print(f"Failed to fetch Parquet file from {server}: {e}")
                print(f"")

        # If we reach here, the file was not found on either server
        print(f"Parquet file '{file_name}' not found on either server.")
        return None



    