import os
import shutil
import tempfile
import urllib.request
import zipfile
import logging
from typing import Optional

class GitHubRepoExtractor:
    def __init__(self, repo_url: str, branch: str = 'main', debug: bool = False):
        self.repo_url = repo_url
        self.branch = branch
        self.logger = logging.getLogger(__name__)
        log_level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")

    def _log_debug(self, message: str):
        self.logger.debug(message)

    def _download_zip(self, temp_dir: str) -> str:
        zip_file_path = os.path.join(temp_dir, 'repo.zip')
        zip_url = f'{self.repo_url}/archive/refs/heads/{self.branch}.zip'
        self._log_debug(f"###### Downloading repository from URL: {zip_url}")
        with urllib.request.urlopen(zip_url) as response:
            with open(zip_file_path, 'wb') as out_file:
                out_file.write(response.read())
        self._log_debug(f"   Zip file downloaded to: {zip_file_path}")
        return zip_file_path

    def _extract_zip(self, zip_file_path: str, temp_dir: str) -> str:
        self._log_debug("###### Extracting zip file")
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        extracted_contents = os.listdir(temp_dir)

        repo_extracted_dir = None
        for item in extracted_contents:
            if os.path.isdir(os.path.join(temp_dir, item)) and item != '__MACOSX':
                repo_extracted_dir = os.path.join(temp_dir, item)
                break

        if repo_extracted_dir is None:
            raise Exception("Could not find extracted repository directory")

        self._log_debug(f"   Zip file extracted to: {repo_extracted_dir}")
        return repo_extracted_dir

    def _copy_subdirectory(self, src: str, dest: str):
        self._log_debug(f"###### Checking if subdirectory exists: {src}")
        if os.path.exists(src):
            self._log_debug(f"   Subdirectory found. Copying contents...")
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dest, item)
                self._log_debug(f"     Copying {s} to {d}")
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
            self._log_debug("   Copying completed.")
        else:
            self._log_debug(f"   Subdirectory {src} does not exist.")

    def extract_to_directory(self, subdir_name: str, target_dir: Optional[str] = None):
        self._log_debug(f"## Initial Parameters:")
        self._log_debug(f"   repo_url: {self.repo_url}")
        self._log_debug(f"   subdir_name: {subdir_name}")
        self._log_debug(f"   branch: {self.branch}")
        self._log_debug(f"   target_dir: {target_dir}")

        temp_dir = tempfile.mkdtemp()
        self._log_debug(f"###### Created temporary directory at: {temp_dir}")

        try:
            zip_file_path = self._download_zip(temp_dir)
            repo_extracted_dir = self._extract_zip(zip_file_path, temp_dir)

            self._log_debug("###### Listing contents of extracted directory:")
            for root, dirs, files in os.walk(repo_extracted_dir):
                level = root.replace(repo_extracted_dir, '').count(os.sep)
                indent = ' ' * 4 * (level)
                self._log_debug(f"{indent}{os.path.basename(root)}/")
                subindent = ' ' * 4 * (level + 1)
                for f in files:
                    self._log_debug(f"{subindent}{f}")

            if target_dir == ".":
                target_dir = os.getcwd()
            elif target_dir is None:
                target_dir = os.getcwd()
            else:
                target_dir = os.path.join(os.getcwd(), target_dir)
                self._log_debug(f"###### Creating target directory: {target_dir}")
                os.makedirs(target_dir, exist_ok=True)

            subdir_path = os.path.join(repo_extracted_dir, subdir_name)
            self._copy_subdirectory(subdir_path, target_dir)

        finally:
            shutil.rmtree(temp_dir)
            self._log_debug(f"###### Removed temporary directory: {temp_dir}")
