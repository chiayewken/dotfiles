import hashlib
import json
import os
import shutil
import time
from pathlib import Path
from typing import List

from fire import Fire
from pydantic import BaseModel
from tqdm import tqdm
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class ShellOutput(BaseModel):
    text: str
    error: str
    is_success: bool


def run_shell(command: str) -> ShellOutput:
    import subprocess

    process = subprocess.run(command.split(), capture_output=True)
    return ShellOutput(
        text=process.stdout.decode(),
        error=process.stderr.decode(),
        is_success=process.returncode == 0,
    )


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


def copy_if_changed(path_in: str, path_out: str):
    with open(path_in, "rb") as f:
        hash_a = hashlib.md5(f.read()).hexdigest()
    if Path(path_out).exists():
        with open(path_out, "rb") as f:
            hash_b = hashlib.md5(f.read()).hexdigest()
    else:
        hash_b = ""
    if hash_a != hash_b:
        copy_path(path_in, path_out)


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

    def run(self, command: str, strict: bool = True) -> str:
        path = Path(self.path).resolve(strict=True)
        output = run_shell(f"git -C {path} {command}")
        if strict:
            assert output.is_success
        return output.text

    def get_remote(self) -> str:
        return self.run("remote get-url origin")

    def get_remote_head(self) -> str:
        url = self.get_remote()
        output = run_shell(f"git ls-remote {url} HEAD")
        assert output.is_success
        return output.text.split()[0].strip()

    def get_head(self) -> str:
        return self.run("rev-parse HEAD").strip()

    def clear(self):
        for path in sorted(Path(self.path).glob("*")):
            if path not in [Path(self.path, ".git"), Path(self.path, "README.md")]:
                delete_path(str(path))

    def push_all(self, commit_message: str = "New Commit"):
        self.run("add --all")
        if len(self.run("diff HEAD")) > 0:
            self.run("commit -m {commit_message}")
            self.run("push")

    def pull_all(self):
        self.run("pull")

    def check_remote_changes(self) -> bool:
        return self.get_remote_head() != self.get_head()


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


class Downloader(BaseModel):
    path_config: str

    def init(self):
        config = SyncConfig.load(self.path_config)
        config.path_in, config.path_out = config.path_out, config.path_in
        for pattern in config.file_patterns:
            for path in Path(config.path_in).glob(pattern):
                path_out = convert_path(str(path), config.path_in, config.path_out)
                copy_if_changed(str(path), path_out)

    def run(self):
        config = SyncConfig.load(self.path_config)
        repo = GitRepo(path=config.path_out)

        for _ in tqdm(range(int(1e6))):
            if repo.check_remote_changes():
                repo.pull_all()
                self.init()
            else:
                time.sleep(config.update_interval)


def upload(path: str):
    Uploader(path_config=path).run()


def download(path: str):
    Downloader(path_config=path).run()


if __name__ == "__main__":
    Fire()
