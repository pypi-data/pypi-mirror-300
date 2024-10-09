import json
import os
from pymongo import MongoClient
from gridfs import GridFS, NoFile
import datetime
from bson.objectid import ObjectId

class DataAccess:
    """
        :Description: Data Access class for interacting with data
        :Attributes: ip: str, username: str, password: str
        :Method view_files: view all files
        :Method download_files: download a file
    """
    def __init__(self):
        self.ip = os.getenv("DATA3_IP")
        self.username = os.getenv("DATA3_USER_NAME")
        self.password = os.getenv("DATA3_PASSWORD")
        self.mongo_client = self._connect_to_database(self.ip, self.username, self.password)
        self.db = self.mongo_client['datasite'] if self.username and self.password else self.mongo_client['mockdatasite']
        self.fs = GridFS(self.db)
        self.user_type = "registered" if self.username and self.password else "guest"

        # Setting up guest client for mockdatasite (always used for fetching mock data)
        self.guest_client = MongoClient(f"mongodb://guest:data3network@{self.ip}:27017/mockdatasite")
        self.guest_db = self.guest_client['mockdatasite']
        self.guest_fs = GridFS(self.guest_db)

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
        '''
        Description: Download files based on the file type and file ID mapping provided in the environment variables.
        Parameters: None
        Creates a new directory 'downloads' if it doesn't exist.
        '''
        file_type = os.getenv("DATA3_FILE_TYPE")
        file_mapping_str = os.getenv("DATA3_FILE_ID_MAPPING", "{}")
        file_path = os.getenv("DATA3_FILE_PATH")
        file_path = file_path if file_path else "./downloads"

        if not file_type:
            raise ValueError("Error: DATA3_FILE_TYPE is required.")

        try:
            file_mapping = json.loads(file_mapping_str.replace("'", '"'))
        except json.JSONDecodeError:
            raise ValueError("Error: Invalid DATA3_FILE_ID_MAPPING format.")

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        # Get all training and mock files
        training_files = list(self.db.datasite.find()) if self.user_type == "registered" else []
        mock_files = list(self.guest_db.mockdatasite.find())

        # Create dictionaries to map file IDs to their types and original filenames
        training_file_map = {tf['fileId']: tf['fileName'] 
                            for doc in training_files 
                            for tf in doc.get('trainingFiles', [])}
        mock_file_map = {mf['fileId']: mf['fileName'] 
                        for doc in mock_files 
                        for mf in doc.get('mockFiles', [])}

        for file_id, new_filename in file_mapping.items():
            # Check if file already exists
            output_path = os.path.join(file_path, new_filename)
            if os.path.exists(output_path):
                print(f"File already exists: {output_path}")
                continue

            is_training = file_id in training_file_map
            is_mock = file_id in mock_file_map

            # Handle guest user restrictions
            if self.user_type == "guest":
                if is_training:
                    print(f"Warning: Guest users cannot access training file {file_id}.")
                    continue
                elif not is_mock:
                    print(f"Warning: File ID {file_id} not found in mock files.")
                    continue
            else:  # For registered users
                if not (is_training or is_mock):
                    print(f"Warning: File ID {file_id} not found in either training or mock files.")
                    continue

            # Handle file type restrictions
            if file_type == "training":
                if not is_training:
                    continue
                elif self.user_type == "guest":
                    print(f"Warning: Guest users cannot download training files ({file_id}).")
                    continue
            elif file_type == "mock" and not is_mock:
                continue

            try:
                file_id_obj = ObjectId(file_id)
                if is_training and (file_type in ["training", "all"]) and self.user_type == "registered":
                    self._download_and_rename_file(file_id_obj, new_filename, self.fs, file_path)
                elif is_mock and file_type in ["mock", "all"]:
                    self._download_and_rename_file(file_id_obj, new_filename, self.guest_fs, file_path)
            except Exception as e:
                print(f"Error downloading file {file_id}: {e}")

    def _download_and_rename_file(self, file_id, new_filename, fs_instance, file_path):
        try:
            output_path = os.path.join(file_path, new_filename)
            
            # Double-check file existence (in case of concurrent operations)
            if os.path.exists(output_path):
                print(f"File already exists: {output_path}")
                return
            
            file_data = fs_instance.get(file_id)
            with open(output_path, 'wb') as f:
                f.write(file_data.read())
            print(f"File downloaded and renamed successfully: {output_path}")
        except NoFile:
            print(f"Error: File with ID {file_id} not found in GridFS.")
        except Exception as e:
            print(f"Error downloading and renaming file: {e}")
