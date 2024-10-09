import os
import hashlib
import requests
from typing import Optional, List, Dict, Any, Union
from .exceptions import (
    RapidgatorAPIError,
    RapidgatorAuthenticationError,
    RapidgatorNotFoundError,
    RapidgatorValidationError,
)
from .models import (
    User,
    Folder,
    File,
    Upload,
    RemoteUploadJob,
    TrashCanItem,
    OneTimeLink,
)
from tqdm import tqdm
import time


class RapidgatorClient:
    """
    Client for interacting with the Rapidgator API.
    """
    BASE_URL = 'https://rapidgator.net/api/v2'
    MAX_RETRIES = 3

    def __init__(self, login: Optional[str] = None, password: Optional[str] = None, token: Optional[str] = None):
        """
        Initialize RapidgatorClient.

        :param login: User email.
        :param password: User password.
        :param token: Access token.
        """
        self.session = requests.Session()
        self.token = token

        if token is None and login and password:
            self.login(login, password)
        elif token is None:
            raise ValueError("You must provide either token or login and password.")

    def _request(self, endpoint: str, method: str = 'GET', params: Optional[Dict] = None,
                 data: Optional[Dict] = None, files: Optional[Dict] = None) -> Any:
        """
        Make an API request.

        :param endpoint: API endpoint.
        :param method: HTTP method.
        :param params: URL parameters.
        :param data: POST data.
        :param files: Files to upload.
        :return: Parsed JSON response.
        """
        url = f'{self.BASE_URL}/{endpoint}'
        if params is None:
            params = {}
        if self.token:
            params['token'] = self.token

        for attempt in range(self.MAX_RETRIES):
            try:
                response = self.session.request(
                    method, url, params=params, data=data, files=files, timeout=30
                )
                return self._handle_response(response)
            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(1)
                    continue  # Retry
                else:
                    raise RapidgatorAPIError(f'Connection failed after {self.MAX_RETRIES} attempts.') from e

    def _handle_response(self, response: requests.Response) -> Any:
        """
        Handle API response.

        :param response: Response object.
        :return: Parsed response data.
        """
        if not response.ok:
            raise RapidgatorAPIError(f'HTTP Error: {response.status_code}')

        json_resp = response.json()

        status = json_resp.get('status')
        details = json_resp.get('details')
        resp_data = json_resp.get('response')

        if status == 200:
            return resp_data
        elif status == 401:
            raise RapidgatorAuthenticationError(details or 'Authentication failed.')
        elif status == 404:
            raise RapidgatorNotFoundError(details or 'Resource not found.')
        elif status == 400:
            raise RapidgatorValidationError(details or 'Bad request.')
        else:
            raise RapidgatorAPIError(details or 'An error occurred.')

    def login(self, login: str, password: str, code: Optional[str] = None) -> Dict[str, Any]:
        """
        Authenticate and retrieve access token.

        :param login: User email.
        :param password: User password.
        :param code: 2FA code if enabled.
        :return: Response data.
        """
        params = {
            'login': login,
            'password': password,
        }
        if code:
            params['code'] = code
        response = self._request('user/login', params=params)
        self.token = response['token']
        return response

    def get_user_info(self) -> User:
        """
        Retrieve user information.

        :return: User object.
        """
        response = self._request('user/info')
        return User.from_dict(response['user'])

    ####################
    # Folder methods
    ####################

    def create_folder(self, name: str, parent_folder_id: Optional[str] = None) -> Folder:
        """
        Create a new folder.

        :param name: Folder name.
        :param parent_folder_id: Parent folder ID.
        :return: Folder object.
        """
        params = {'name': name}
        if parent_folder_id:
            params['folder_id'] = parent_folder_id
        response = self._request('folder/create', params=params)
        return Folder.from_dict(response['folder'])

    def get_folder_info(self, folder_id: Optional[str] = None) -> Folder:
        """
        Retrieve folder information.

        :param folder_id: Folder ID.
        :return: Folder object.
        """
        params = {}
        if folder_id:
            params['folder_id'] = folder_id
        response = self._request('folder/info', params=params)
        return Folder.from_dict(response['folder'])

    def get_folder_content(self, folder_id: Optional[str] = None, page: int = 1, per_page: int = 500,
                           sort_column: str = 'name', sort_direction: str = 'ASC') -> Dict[str, Any]:
        """
        Retrieve folder content.

        :param folder_id: Folder ID.
        :param page: Page number.
        :param per_page: Items per page.
        :param sort_column: Sort by column.
        :param sort_direction: Sort direction.
        :return: Dictionary with folder and content.
        """
        params = {
            'page': page,
            'per_page': per_page,
            'sort_column': sort_column,
            'sort_direction': sort_direction,
        }
        if folder_id:
            params['folder_id'] = folder_id
        response = self._request('folder/content', params=params)
        folder = Folder.from_dict(response['folder'])
        files = [File.from_dict(f) for f in response['folder'].get('files', [])]
        pager = response.get('pager')
        return {'folder': folder, 'files': files, 'pager': pager}

    def rename_folder(self, folder_id: str, name: str) -> Folder:
        """
        Rename a folder.

        :param folder_id: Folder ID.
        :param name: New name.
        :return: Folder object.
        """
        params = {
            'folder_id': folder_id,
            'name': name,
        }
        response = self._request('folder/rename', params=params)
        return Folder.from_dict(response['folder'])

    def delete_folder(self, folder_ids: Union[str, List[str]]) -> Dict[str, Any]:
        """
        Delete folder(s).

        :param folder_ids: Folder ID(s).
        :return: Result dictionary.
        """
        if isinstance(folder_ids, str):
            folder_ids = [folder_ids]
        params = {'folder_id': ','.join(folder_ids)}
        response = self._request('folder/delete', params=params)
        return response['result']

    def copy_folder(self, folder_ids: Union[str, List[str]], dest_folder_id: str) -> Dict[str, Any]:
        """
        Copy folder(s) to another folder.

        :param folder_ids: Folder ID(s) to copy.
        :param dest_folder_id: Destination folder ID.
        :return: Result dictionary.
        """
        if isinstance(folder_ids, str):
            folder_ids = [folder_ids]
        params = {
            'folder_id': ','.join(folder_ids),
            'folder_id_dest': dest_folder_id,
        }
        response = self._request('folder/copy', params=params)
        return response['result']

    def move_folder(self, folder_ids: Union[str, List[str]], dest_folder_id: str) -> Dict[str, Any]:
        """
        Move folder(s) to another folder.

        :param folder_ids: Folder ID(s) to move.
        :param dest_folder_id: Destination folder ID.
        :return: Result dictionary.
        """
        if isinstance(folder_ids, str):
            folder_ids = [folder_ids]
        params = {
            'folder_id': ','.join(folder_ids),
            'folder_id_dest': dest_folder_id,
        }
        response = self._request('folder/move', params=params)
        return response['result']

    def change_folder_mode(self, folder_id: str, mode: int) -> Folder:
        """
        Change a folder's mode.

        :param folder_id: Folder ID.
        :param mode: New mode (0=Public, 1=Premium only, 2=Private, 3=Hotlink).
        :return: Folder object.
        """
        params = {
            'folder_id': folder_id,
            'mode': mode,
        }
        response = self._request('folder/change_mode', params=params)
        return Folder.from_dict(response['folder'])

    ####################
    # File methods
    ####################

    def upload_file(self, file_path: str, folder_id: Optional[str] = None) -> File:
        """
        Upload a file.

        :param file_path: Local file path.
        :param folder_id: Destination folder ID.
        :return: File object.
        """
        # Initiate upload
        file_hash, file_size = self._get_file_hash_and_size(file_path)
        file_name = os.path.basename(file_path)
        params = {
            'name': file_name,
            'hash': file_hash,
            'size': file_size,
        }
        if folder_id:
            params['folder_id'] = folder_id
        upload_response = self._request('file/upload', params=params)
        upload = Upload.from_dict(upload_response['upload'])

        # Check the state of the upload
        if upload.state == 2:
            # Instant upload is possible
            return upload.file
        elif upload.state == 3:
            raise RapidgatorAPIError('Upload failed at initiation.')
        else:
            # Need to upload the file
            upload_url = upload.url
            upload_id = upload.upload_id
            self._upload_to_url(file_path, upload_url)
            # Check upload info
            for attempt in range(self.MAX_RETRIES):
                time.sleep(2)
                upload_info_response = self.get_upload_info(upload_id)
                upload_info = Upload.from_dict(upload_info_response['upload'])
                if upload_info.state == 2:
                    return upload_info.file
                elif upload_info.state == 3:
                    raise RapidgatorAPIError('Upload failed during processing.')
                else:
                    continue  # Wait and retry
            raise RapidgatorAPIError('Upload failed after multiple attempts.')

    def _upload_to_url(self, file_path: str, upload_url: str) -> None:
        """
        Upload file to given URL.

        :param file_path: Local file path.
        :param upload_url: URL to upload to.
        """
        with open(file_path, 'rb') as f:
            file_size = os.path.getsize(file_path)
            with tqdm(total=file_size, unit='B', unit_scale=True, desc='Uploading') as progress_bar:
                wrapped_file = self._FileWrapper(f, progress_bar)
                for attempt in range(self.MAX_RETRIES):
                    try:
                        response = requests.post(
                            upload_url,
                            files={'file': (os.path.basename(file_path), wrapped_file)},
                            timeout=60
                        )
                        if response.ok:
                            return
                        else:
                            if attempt < self.MAX_RETRIES - 1:
                                progress_bar.reset()
                                f.seek(0)
                                continue
                            else:
                                raise RapidgatorAPIError(f'Upload failed after {self.MAX_RETRIES} attempts.')
                    except (requests.ConnectionError, requests.Timeout) as e:
                        if attempt < self.MAX_RETRIES - 1:
                            progress_bar.reset()
                            f.seek(0)
                            continue  # Retry
                        else:
                            raise RapidgatorAPIError('Connection failed during file upload.') from e

    class _FileWrapper:
        def __init__(self, file_obj, progress_bar):
            self.file_obj = file_obj
            self.progress_bar = progress_bar

        def read(self, chunk_size):
            data = self.file_obj.read(chunk_size)
            if data:
                self.progress_bar.update(len(data))
            return data

        def __iter__(self):
            return self

    def get_upload_info(self, upload_id: str) -> Dict[str, Any]:
        """
        Get information about an upload.

        :param upload_id: Upload ID.
        :return: Upload information.
        """
        params = {'upload_id': upload_id}
        response = self._request('file/upload_info', params=params)
        return response

    def get_file_info(self, file_id: str) -> File:
        """
        Retrieve file information.

        :param file_id: File ID.
        :return: File object.
        """
        params = {'file_id': file_id}
        response = self._request('file/info', params=params)
        return File.from_dict(response['file'])

    def rename_file(self, file_id: str, new_name: str) -> File:
        """
        Rename a file.

        :param file_id: File ID.
        :param new_name: New file name.
        :return: File object.
        """
        params = {
            'file_id': file_id,
            'name': new_name,
        }
        response = self._request('file/rename', params=params)
        return File.from_dict(response['file'])

    def delete_file(self, file_ids: Union[str, List[str]]) -> Dict[str, Any]:
        """
        Delete file(s).

        :param file_ids: File ID(s).
        :return: Result dictionary.
        """
        if isinstance(file_ids, str):
            file_ids = [file_ids]
        params = {'file_id': ','.join(file_ids)}
        response = self._request('file/delete', params=params)
        return response['result']

    def copy_file(self, file_ids: Union[str, List[str]], dest_folder_id: str) -> Dict[str, Any]:
        """
        Copy file(s) to another folder.

        :param file_ids: File ID(s).
        :param dest_folder_id: Destination folder ID.
        :return: Result dictionary.
        """
        if isinstance(file_ids, str):
            file_ids = [file_ids]
        params = {
            'file_id': ','.join(file_ids),
            'folder_id_dest': dest_folder_id,
        }
        response = self._request('file/copy', params=params)
        return response['result']

    def move_file(self, file_ids: Union[str, List[str]], dest_folder_id: str) -> Dict[str, Any]:
        """
        Move file(s) to another folder.

        :param file_ids: File ID(s).
        :param dest_folder_id: Destination folder ID.
        :return: Result dictionary.
        """
        if isinstance(file_ids, str):
            file_ids = [file_ids]
        params = {
            'file_id': ','.join(file_ids),
            'folder_id_dest': dest_folder_id,
        }
        response = self._request('file/move', params=params)
        return response['result']

    def change_file_mode(self, file_id: str, mode: int) -> File:
        """
        Change a file's mode.

        :param file_id: File ID.
        :param mode: New mode (0=Public, 1=Premium only, 2=Private, 3=Hotlink).
        :return: File object.
        """
        params = {
            'file_id': file_id,
            'mode': mode,
        }
        response = self._request('file/change_mode', params=params)
        return File.from_dict(response['file'])

    def check_link(self, urls: Union[str, List[str]]) -> List[Dict[str, Any]]:
        """
        Check download link(s).

        :param urls: URL(s).
        :return: List of link info dictionaries.
        """
        if isinstance(urls, str):
            urls = [urls]
        params = {'url': ','.join(urls)}
        response = self._request('file/check_link', params=params)
        return response

    def create_onetime_link(self, file_id: str, callback_url: Optional[str] = None, notify: bool = False) -> OneTimeLink:
        """
        Create a one-time download link.

        :param file_id: File ID.
        :param callback_url: Callback URL.
        :param notify: Send notification when file is downloaded.
        :return: OneTimeLink object.
        """
        params = {
            'file_id': file_id,
            'notify': int(notify)
        }
        if callback_url:
            params['url'] = callback_url
        response = self._request('file/onetimelink_create', params=params)
        return OneTimeLink.from_dict(response['link'])

    def get_onetime_link_info(self, link_ids: Optional[Union[str, List[str]]] = None) -> List[Union[OneTimeLink, Dict[str, Any]]]:
        """
        Get one-time link information.

        :param link_ids: Link ID(s).
        :return: List of OneTimeLink objects or error dictionaries.
        """
        params = {}
        if link_ids:
            if isinstance(link_ids, str):
                link_ids = [link_ids]
            params['link_id'] = ','.join(link_ids)
        response = self._request('file/onetimelink_info', params=params)
        links = []
        for link_data in response['links']:
            if 'error' in link_data:
                links.append({'link_id': link_data.get('link_id'), 'error': link_data['error']})
            else:
                links.append(OneTimeLink.from_dict(link_data))
        return links

    def download_file(self, file_id: str, local_path: str) -> None:
        """
        Download a file from Rapidgator.

        :param file_id: File ID.
        :param local_path: Local path to save the file.
        """
        params = {'file_id': file_id}
        response = self._request('file/download', params=params)
        download_url = response['download_url']

        for attempt in range(self.MAX_RETRIES):
            try:
                with self.session.get(download_url, stream=True, timeout=60) as r:
                    r.raise_for_status()
                    total_size = int(r.headers.get('content-length', 0))
                    with open(local_path, 'wb') as f, tqdm(
                        total=total_size, unit='B', unit_scale=True, desc='Downloading'
                    ) as progress_bar:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                progress_bar.update(len(chunk))
                break  # Download successful
            except (requests.ConnectionError, requests.Timeout, requests.HTTPError) as e:
                if attempt < self.MAX_RETRIES - 1:
                    continue  # Retry
                else:
                    raise RapidgatorAPIError('Failed to download the file.') from e

    ####################
    # Trash Can methods
    ####################

    def get_trashcan_content(self, page: int = 1, per_page: int = 500,
                             sort_column: str = 'name', sort_direction: str = 'ASC') -> Dict[str, Any]:
        """
        Retrieve trash can content.

        :param page: Page number.
        :param per_page: Items per page.
        :param sort_column: Sort by column.
        :param sort_direction: Sort direction.
        :return: Dictionary with files and pager info.
        """
        params = {
            'page': page,
            'per_page': per_page,
            'sort_column': sort_column,
            'sort_direction': sort_direction,
        }
        response = self._request('trashcan/content', params=params)
        files = [TrashCanItem.from_dict(f) for f in response['files']]
        pager = response.get('pager')
        return {'files': files, 'pager': pager}

    def restore_trashcan_files(self, file_ids: Optional[Union[str, List[str]]] = None) -> Dict[str, Any]:
        """
        Restore file(s) from trash can.

        :param file_ids: File ID(s). If None, all files are restored.
        :return: Result dictionary.
        """
        params = {}
        if file_ids:
            if isinstance(file_ids, str):
                file_ids = [file_ids]
            params['file_id'] = ','.join(file_ids)
        response = self._request('trashcan/restore', params=params)
        return response['result']

    def empty_trashcan(self, file_ids: Optional[Union[str, List[str]]] = None) -> Dict[str, Any]:
        """
        Empty trash can.

        :param file_ids: File ID(s). If None, all files are deleted.
        :return: Result dictionary.
        """
        params = {}
        if file_ids:
            if isinstance(file_ids, str):
                file_ids = [file_ids]
            params['file_id'] = ','.join(file_ids)
        response = self._request('trashcan/empty', params=params)
        return response['result']

    ####################
    # Remote Upload methods
    ####################

    def create_remote_upload_job(self, urls: Union[str, List[str]]) -> List[RemoteUploadJob]:
        """
        Create remote upload job(s).

        :param urls: Remote file URL(s).
        :return: List of RemoteUploadJob objects.
        """
        if isinstance(urls, str):
            urls = [urls]
        params = {'url': ','.join(urls)}
        response = self._request('remote/create', params=params)
        jobs = [RemoteUploadJob.from_dict(job_data) for job_data in response['jobs']]
        return jobs

    def get_remote_upload_info(self, job_ids: Optional[Union[int, List[int]]] = None) -> List[RemoteUploadJob]:
        """
        Retrieve remote upload job information.

        :param job_ids: Job ID(s). If None, all jobs are returned.
        :return: List of RemoteUploadJob objects.
        """
        params = {}
        if job_ids:
            if isinstance(job_ids, int):
                job_ids = [job_ids]
            params['job_id'] = ','.join(map(str, job_ids))
        response = self._request('remote/info', params=params)
        jobs = [RemoteUploadJob.from_dict(job_data) for job_data in response['jobs']]
        return jobs

    def delete_remote_upload_job(self, job_ids: Union[int, List[int]]) -> Dict[str, Any]:
        """
        Delete remote upload job(s).

        :param job_ids: Job ID(s).
        :return: Result dictionary.
        """
        if isinstance(job_ids, int):
            job_ids = [job_ids]
        params = {'job_id': ','.join(map(str, job_ids))}
        response = self._request('remote/delete', params=params)
        return response['result']

    ####################
    # Utilities
    ####################

    def _get_file_hash_and_size(self, file_path: str) -> (str, int):
        """
        Calculate MD5 hash and size of a file.

        :param file_path: Local file path.
        :return: Tuple of (MD5 hash, file size).
        """
        md5_hash = hashlib.md5()
        total_size = 0
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                md5_hash.update(chunk)
                total_size += len(chunk)
        return md5_hash.hexdigest(), total_size

    def upload_folder(self, local_folder_path: str, parent_folder_id: Optional[str] = None) -> Folder:
        """
        Upload a local folder to Rapidgator.

        :param local_folder_path: Path to local folder.
        :param parent_folder_id: ID of remote parent folder.
        :return: Folder object of the created remote folder.
        """
        # Create remote folder
        folder_name = os.path.basename(os.path.normpath(local_folder_path))
        remote_folder = self.create_folder(name=folder_name, parent_folder_id=parent_folder_id)
        remote_folder_id = remote_folder.folder_id

        # Initialize folder mapping to keep track of remote folders
        folder_map = {local_folder_path: remote_folder_id}

        # Walk through the local folder and upload files
        for root, dirs, files in os.walk(local_folder_path):
            # Determine the parent remote folder ID
            local_parent_folder = os.path.dirname(root)
            parent_id = folder_map.get(local_parent_folder, remote_folder_id)

            # Create subfolders in remote
            for dir_name in dirs:
                local_dir_path = os.path.join(root, dir_name)
                remote_dir = self.create_folder(name=dir_name, parent_folder_id=parent_id)
                folder_map[local_dir_path] = remote_dir.folder_id

            # Upload files in the current directory
            for filename in files:
                local_file_path = os.path.join(root, filename)
                print(f'Uploading file: {local_file_path}')
                self.upload_file(local_file_path, folder_id=folder_map.get(root, parent_id))
        return remote_folder

    def _find_remote_folder(self, name: str, parent_folder_id: str) -> Optional[Folder]:
        """
        Find a remote folder by name.

        :param name: Folder name.
        :param parent_folder_id: Parent folder ID.
        :return: Folder object or None.
        """
        content = self.get_folder_content(folder_id=parent_folder_id)
        for folder in content['folder'].folders:
            if folder.name == name:
                return folder
        return None
