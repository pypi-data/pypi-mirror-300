from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

@dataclass
class Traffic:
    total: Optional[int]
    left: Optional[int]

@dataclass
class Storage:
    total: int
    left: int

@dataclass
class UploadInfo:
    max_file_size: int
    nb_pipes: int

@dataclass
class RemoteUploadInfo:
    max_nb_jobs: int
    refresh_time: int

@dataclass
class User:
    email: str
    is_premium: bool
    premium_end_time: Optional[int]
    state: int
    state_label: str
    traffic: Traffic
    storage: Storage
    upload: UploadInfo
    remote_upload: RemoteUploadInfo

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        return cls(
            email=data['email'],
            is_premium=data['is_premium'],
            premium_end_time=data['premium_end_time'],
            state=data['state'],
            state_label=data['state_label'],
            traffic=Traffic(
                total=int(data['traffic']['total']) if data['traffic']['total'] else None,
                left=int(data['traffic']['left']) if data['traffic']['left'] else None
            ),
            storage=Storage(
                total=int(data['storage']['total']),
                left=int(data['storage']['left'])
            ),
            upload=UploadInfo(
                max_file_size=int(data['upload']['max_file_size']),
                nb_pipes=int(data['upload']['nb_pipes'])
            ),
            remote_upload=RemoteUploadInfo(
                max_nb_jobs=int(data['remote_upload']['max_nb_jobs']),
                refresh_time=int(data['remote_upload']['refresh_time'])
            )
        )

@dataclass
class Folder:
    folder_id: str
    mode: int
    mode_label: str
    parent_folder_id: Optional[str]
    name: str
    url: str
    nb_folders: int
    nb_files: int
    size_files: Optional[int]
    created: int
    folders: List['Folder'] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Folder':
        folder_list = data.get('folders', [])
        folders = [cls.from_dict(f) for f in folder_list]
        return cls(
            folder_id=data['folder_id'],
            mode=int(data['mode']),
            mode_label=data['mode_label'],
            parent_folder_id=data.get('parent_folder_id'),
            name=data['name'],
            url=data['url'],
            nb_folders=int(data.get('nb_folders', 0)),
            nb_files=int(data.get('nb_files', 0)),
            size_files=int(data['size_files']) if data['size_files'] else None,
            created=int(data['created']),
            folders=folders
        )

@dataclass
class File:
    file_id: str
    mode: int
    mode_label: str
    folder_id: Optional[str]
    name: str
    hash: str
    size: int
    created: int
    url: str
    nb_downloads: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'File':
        return cls(
            file_id=data['file_id'],
            mode=int(data['mode']),
            mode_label=data['mode_label'],
            folder_id=data.get('folder_id'),
            name=data['name'],
            hash=data['hash'],
            size=int(data['size']),
            created=int(data['created']),
            url=data['url'],
            nb_downloads=int(data['nb_downloads']) if data.get('nb_downloads') else None
        )

@dataclass
class Upload:
    upload_id: str
    url: Optional[str]
    file: Optional[File]
    state: int
    state_label: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Upload':
        file = None
        if data.get('file'):
            if isinstance(data['file'], Dict) and data['file']:
                file = File.from_dict(data['file'])
        return cls(
            upload_id=data['upload_id'],
            url=data.get('url'),
            file=file,
            state=int(data['state']),
            state_label=data['state_label']
        )

@dataclass
class RemoteUploadJob:
    job_id: int
    type: int
    type_label: str
    folder_id: str
    url: str
    name: str
    size: int
    state: int
    state_label: str
    file: Optional[File]
    dl_size: int
    speed: int
    created: int
    updated: Optional[int]
    error: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RemoteUploadJob':
        file = None
        if data.get('file'):
            if isinstance(data['file'], Dict) and data['file']:
                file = File.from_dict(data['file'])
        return cls(
            job_id=int(data['job_id']),
            type=int(data['type']),
            type_label=data['type_label'],
            folder_id=data['folder_id'],
            url=data['url'],
            name=data['name'],
            size=int(data['size']),
            state=int(data['state']),
            state_label=data['state_label'],
            file=file,
            dl_size=int(data['dl_size']),
            speed=int(data['speed']),
            created=int(data['created']),
            updated=int(data['updated']) if data.get('updated') else None,
            error=data.get('error')
        )

@dataclass
class TrashCanItem:
    file_id: str
    mode: int
    mode_label: str
    folder_id: Optional[str]
    name: str
    hash: str
    size: int
    created: int
    url: str
    nb_downloads: Optional[int]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TrashCanItem':
        return cls(
            file_id=data['file_id'],
            mode=int(data['mode']),
            mode_label=data['mode_label'],
            folder_id=data.get('folder_id'),
            name=data['name'],
            hash=data['hash'],
            size=int(data['size']),
            created=int(data['created']),
            url=data['url'],
            nb_downloads=int(data['nb_downloads']) if data['nb_downloads'] else None
        )

@dataclass
class OneTimeLink:
    link_id: str
    file: File
    url: str
    state: int
    state_label: str
    callback_url: Optional[str]
    notify: bool
    created: int
    downloaded: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OneTimeLink':
        file = File.from_dict(data['file']) if data.get('file') else None
        return cls(
            link_id=data['link_id'],
            file=file,
            url=data['url'],
            state=int(data['state']),
            state_label=data['state_label'],
            callback_url=data.get('callback_url'),
            notify=bool(data['notify']),
            created=int(data['created']),
            downloaded=bool(data['downloaded'])
        )
