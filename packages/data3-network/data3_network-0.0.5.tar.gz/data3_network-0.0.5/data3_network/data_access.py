import os
from dotenv import load_dotenv
from pymongo import MongoClient
from gridfs import GridFS, NoFile
import datetime
from bson.objectid import ObjectId

load_dotenv()


class DataAccess:
    """
    :Description: Data Access class for interacting with data
    :Attributes: ip: str, username: str, password: str
    :Method view_files: view all files
    :Method download_files: download a file
    """

    def __init__(self):
        ip = os.getenv("IP")
        username = os.getenv("USER_NAME", None)
        password = os.getenv("PASSWORD", None)
        self.mongo_client = self._connect_to_database(ip, username, password)
        self.db = self.mongo_client['datasite'] if username and password else self.mongo_client['mockdatasite']
        self.fs = GridFS(self.db)
        self.user_type = "registered" if username and password else "guest"

        # Setting up guest client for mockdatasite (always used for fetching mock data)
        self.guest_client = MongoClient(f"mongodb://guest:data3network@{ip}:27017/mockdatasite")
        self.guest_db = self.guest_client['mockdatasite']
        self.guest_fs = GridFS(self.guest_db)  # Separate GridFS instance for mock data

    def _connect_to_database(self, ip: str, username: str = None, password: str = None):
        if username and password:
            uri = f"mongodb://{username}:{password}@{ip}:27017/datasite"
        else:
            uri = f"mongodb://guest:data3network@{ip}:27017/mockdatasite"

        try:
            client = MongoClient(uri)
            print("Connected to MongoDB successfully.")
            return client
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            return None

    def view_files(self):
        """
        Description: View all files in the database
        Parameters: None
        Returns: List of file metadata
        """
        formatted_files = []

        # Fetch files from the 'datasite' collection (for registered users)
        if self.user_type == "registered":
            training_files_cursor = self.db.datasite.find()
            for file in training_files_cursor:
                formatted_file = {
                    "name": file.get("name", ""),
                    "description": file.get("description", ""),
                    "metadata": {
                        "createdBy": file.get("metadata", {}).get("createdBy", ""),
                        "createdAt": {
                            "$numberLong": str(file.get("metadata", {}).get("createdAt", 0))
                        }
                    },
                }
                
                # Add only non-empty trainingFiles to the output
                training_files = file.get("trainingFiles", [])
                if training_files:
                    formatted_file["trainingFiles"] = [
                        {
                            "fileName": tf.get("fileName", ""),
                            "uploadedAt": {
                                "$date": tf.get("uploadedAt", "").isoformat() if isinstance(tf.get("uploadedAt"), datetime.datetime) else ""
                            },
                            "fileId": tf.get("fileId", ""),
                            "fileSize": {
                                "$numberLong": str(tf.get("fileSize", 0))
                            }
                        } for tf in training_files
                    ]
                
                formatted_files.append(formatted_file)

        # Fetch files from the 'mockdatasite' collection (for guest users)
        mock_files_cursor = self.guest_db.mockdatasite.find()
        for file in mock_files_cursor:
            formatted_file = {
                "name": file.get("name", ""),
                "description": file.get("description", ""),
                "metadata": {
                    "createdBy": file.get("metadata", {}).get("createdBy", ""),
                    "createdAt": {
                        "$numberLong": str(file.get("metadata", {}).get("createdAt", 0))
                    }
                },
            }

            # Include mock files
            mock_files = file.get("mockFiles", [])
            if mock_files:
                formatted_file["mockFiles"] = [
                    {
                        "fileName": mf.get("fileName", ""),
                        "uploadedAt": {
                            "$date": mf.get("uploadedAt", "").isoformat() if isinstance(mf.get("uploadedAt"), datetime.datetime) else ""
                        },
                        "fileId": mf.get("fileId", ""),
                        "fileSize": {
                            "$numberLong": str(mf.get("fileSize", 0))
                        }
                    } for mf in mock_files
                ]
            
            # Add training files from mockdatasite only for guest users
            if self.user_type == "guest":
                training_files = file.get("trainingFiles", [])
                if training_files:
                    formatted_file["trainingFiles"] = [
                        {
                            "fileName": tf.get("fileName", ""),
                            "uploadedAt": {
                                "$date": tf.get("uploadedAt", "").isoformat() if isinstance(tf.get("uploadedAt"), datetime.datetime) else ""
                            },
                            "fileId": tf.get("fileId", ""),
                            "fileSize": {
                                "$numberLong": str(tf.get("fileSize", 0))
                            }
                        } for tf in training_files
                    ]

            formatted_files.append(formatted_file)

        return formatted_files


    def download_files(self):
        """
        Description: Download a file or multiple files (training/mock/all)
        Parameters:
            file_type: str ("training", "mock", or "all")
            file_names: list (specific filenames to download, empty list means download all)
        Creates: Files in the "download/<file_id>/<file_name>" path
        """
        
        # Fetch file type and file ID from environment variables
        file_type = os.getenv("FILE_TYPE")
        file_ids = os.getenv("FILE_ID", "").split(",")  # Split by comma to convert to list
        file_path = os.getenv("FILE_PATH")
        file_path = file_path if file_path else "./downloads"  # Default value for file path
        
        # Check if file_type is provided, else throw error
        if not file_type:
            raise ValueError("Error: FILE_TYPE is required. Please provide a valid file type (training/mock/all).")
        
        # Trim whitespace from each file ID and remove empty strings
        file_ids = [file_id.strip() for file_id in file_ids if file_id.strip()]

        # Check for user authentication
        user_authenticated = self.user_type == "registered"

        # If user is not authenticated and the file type is "all", only download mock files
        if not user_authenticated and file_type == "all":
            file_type = "mock"  # Set to mock to download only mock files

        # Check if guest users attempt to download training files
        if self.user_type == "guest" and file_type in ["training", "all"]:
            print("Guest users cannot download training files.")
            return None

        # Fetch all files based on type
        training_files = []
        mock_files = []
        if file_type in ["training", "all"]:
            training_files = self.db.datasite.find() if self.user_type == "registered" else []
        if file_type in ["mock", "all"]:
            mock_files = self.guest_db.mockdatasite.find()

        files_to_download = []

        # If file_ids is empty, download all files based on the file type
        if not file_ids:
            if file_type in ["training", "all"]:
                files_to_download.extend(training_files)
            if file_type in ["mock", "all"]:
                files_to_download.extend(mock_files)
        else:
            # Filter files based on provided file IDs
            if file_type in ["training", "all"]:
                for file in training_files:
                    # Check if any training file has a matching file ID
                    matched_files = [tf for tf in file.get('trainingFiles', []) if tf['fileId'] in file_ids]
                    if matched_files:
                        files_to_download.append({"trainingFiles": matched_files})
                        
            if file_type in ["mock", "all"]:
                for file in mock_files:
                    # Check if any mock file has a matching file ID
                    matched_files = [mf for mf in file.get('mockFiles', []) if mf['fileId'] in file_ids]
                    if matched_files:
                        files_to_download.append({"mockFiles": matched_files})

        if not files_to_download:
            raise ValueError("Error: No files found with the specified file IDs.")

        print(f"Files to download: {files_to_download}")  # Debugging statement

        # Process download
        for file in files_to_download:
            # Handle mock files
            if (file_type == "mock" or file_type == "all") and "mockFiles" in file:
                for mock_file in file.get("mockFiles", []):
                    self._download_single_file(mock_file, is_mock=True, file_path=file_path)

            # Handle training files
            if (file_type == "training" or file_type == "all") and "trainingFiles" in file:
                for training_file in file.get("trainingFiles", []):
                    self._download_single_file(training_file, is_mock=False, file_path=file_path)

    def _download_single_file(self, file, is_mock=False, file_path="downloads"):
        file_id = file.get("fileId")
        file_name = file.get("fileName")

        if file_id is None:
            print(f"Error: No file_id found for the file '{file_name}'. Skipping download.")
            return

        # Convert file_id to ObjectId for GridFS lookup
        try:
            file_id = ObjectId(file_id)
        except Exception as e:
            print(f"Error converting file_id to ObjectId: {e}")
            return

        # Ensure the download directory exists
        download_dir = os.path.join(file_path, str(file_id))
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        download_path = os.path.join(download_dir, file_name)

        # Check if the file already exists
        if os.path.exists(download_path):
            print(f"File '{file_name}' already exists in '{download_dir}'.")
            return

        # Download the file
        try:
            fs_instance = self.guest_fs if is_mock else self.fs
            with open(download_path, 'wb') as f:
                f.write(fs_instance.get(file_id).read())
            print(f"File '{file_name}' downloaded successfully to '{download_path}'.")
        except NoFile:
            print(f"Error: File '{file_name}' not found in GridFS.")
        except Exception as e:
            print(f"Error downloading file '{file_name}': {e}")
