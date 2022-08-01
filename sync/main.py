import json
import os
import shutil
import time
from pathlib import Path
from typing import List

from fire import Fire
from git import Repo
from pydantic import BaseModel
from tqdm import tqdm
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


def copy_path(path_in: str, path_out: str):
    print(dict(copy=path_in, path_out=path_out))
    if Path(path_in).exists():
        Path(path_out).parent.mkdir(parents=True, exist_ok=True)
        if Path(path_in).is_dir():
            if Path(path_out).exists():
                shutil.rmtree(path_out)
            shutil.copytree(path_in, path_out)
        else:
            shutil.copyfile(path_in, path_out)


def delete_path(path: str):
    print(dict(delete=path))
    if Path(path).exists():
        if Path(path).is_dir():
            shutil.rmtree(path)
        else:
            os.remove(path)


def convert_path(path: str, folder_in: str, folder_out: str) -> str:
    assert path.startswith(folder_in)
    parts = Path(path).parts[len(Path(folder_in).parts) :]
    path_out = str(Path(folder_out, *parts))
    assert path_out.startswith(folder_out)
    return path_out


class PathMatcher(BaseModel):
    patterns: List[str]

    def run(self, path: str) -> bool:
        return any(Path(path).resolve().match(p) for p in self.patterns)


class FileHandler(FileSystemEventHandler):
    """Adapted from LoggingEventHandler"""

    def __init__(self, folder_in: str, folder_out: str, matcher: PathMatcher):
        super().__init__()
        self.matcher = matcher
        self.folder_in = str(Path(folder_in).resolve())
        self.folder_out = str(Path(folder_out).resolve())

    def on_moved(self, event):
        super().on_moved(event)
        if self.matcher.run(event.src_path):
            path_in = convert_path(event.src_path, self.folder_in, self.folder_out)
            path_out = convert_path(event.dest_path, self.folder_in, self.folder_out)
            copy_path(path_in, path_out)
            delete_path(path_in)

    def on_created(self, event):
        super().on_created(event)
        if self.matcher.run(event.src_path):
            path = convert_path(event.src_path, self.folder_in, self.folder_out)
            copy_path(event.src_path, path)

    def on_deleted(self, event):
        super().on_deleted(event)
        if self.matcher.run(event.src_path):
            path = convert_path(event.src_path, self.folder_in, self.folder_out)
            delete_path(path)

    def on_modified(self, event):
        super().on_modified(event)
        if self.matcher.run(event.src_path):
            path = convert_path(event.src_path, self.folder_in, self.folder_out)
            copy_path(event.src_path, path)


def test_handler(folder_in: str = "temp_in", folder_out: str = "temp_out"):
    handler = FileHandler(folder_in, folder_out, matcher=PathMatcher(patterns=["*"]))
    observer = Observer()
    observer.schedule(handler, folder_in, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()


class GitRepo(BaseModel):
    path: str
    remote_name: str = "origin"

    def clear(self):
        for path in sorted(Path(self.path).glob("*")):
            if path not in [Path(self.path, ".git"), Path(self.path, "README.md")]:
                delete_path(str(path))

    def push_all(self, commit_message: str = "New Commit"):
        repo = Repo(self.path)
        repo.git.add("--all")
        if repo.head.commit.diff():
            for diff in repo.head.commit.diff():
                print(dict(diff=(diff.a_mode, diff.a_path, diff.b_mode, diff.b_path)))
            repo.git.commit(f"-m {commit_message}")
            remote = repo.remote(self.remote_name)
            remote.push()
            print(dict(push=sorted(remote.urls)))


def test_repo(folder: str = "../CodeDrive"):
    repo = GitRepo(path=folder)
    repo.push_all()


class SyncConfig(BaseModel):
    path_in: str
    path_out: str
    update_interval: int
    file_patterns: List[str]

    @classmethod
    def load(cls, path: str):
        with open(path) as f:
            return cls(**json.load(f))


class Uploader(BaseModel):
    path_config: str

    def init(self):
        config = SyncConfig.load(self.path_config)
        for pattern in config.file_patterns:
            for path in Path(config.path_in).glob(pattern):
                path_out = convert_path(str(path), config.path_in, config.path_out)
                copy_path(str(path), path_out)

    def run(self):
        config = SyncConfig.load(self.path_config)
        matcher = PathMatcher(patterns=config.file_patterns)
        handler = FileHandler(config.path_in, config.path_out, matcher=matcher)
        observer = Observer()
        observer.schedule(handler, config.path_in, recursive=True)
        observer.start()
        repo = GitRepo(path=config.path_out)
        repo.clear()
        self.init()

        try:
            for _ in tqdm(range(int(1e6))):
                time.sleep(config.update_interval)
                repo.push_all()
        finally:
            observer.stop()
            observer.join()


def upload(path: str):
    Uploader(path_config=path).run()


if __name__ == "__main__":
    Fire()
