import requests
from pathlib import Path
from loguru import logger
import sys
import fire
import os
import yaml
from tqdm import tqdm

logger.remove()
logger.add(sys.stdout, level="INFO")


def parse_frontmatter(file_path):
    """Parses the YAML frontmatter of a markdown file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            if content.startswith("---"):
                frontmatter, body = content.split("---", 2)[1:]
                return yaml.safe_load(frontmatter)
    except Exception as e:
        logger.error(f"Error parsing frontmatter for {file_path}: {str(e)}")
    return None


def mdsync(path=".", api_key=None, debug=False):
    if debug:
        logger.add(sys.stdout, level="DEBUG")
    domain = os.getenv("MARKOPOLIS_DOMAIN")
    api_key = os.getenv("MARKOPOLIS_API")
    if not api_key:
        logger.error("API key is required")
        return

    api_endpoint = f"{domain}/api/upload"
    headers = {"X-API-Key": api_key}

    path = Path(path)
    if not path.is_dir():
        logger.error(f"{path} is not a valid directory")
        return

    # Get list of all files from the API (remote)
    try:
        response = requests.get(api_endpoint, headers=headers)
        if response.status_code == 200:
            remote_files = set(response.json())
        else:
            logger.error(
                f"Failed to get file list from API. Status code: {response.status_code}"
            )
            return
    except Exception as e:
        logger.error(f"Error getting file list from API: {str(e)}")
        return

    # Track files that need to be deleted
    files_to_delete = set()

    # Process local files
    local_files = [
        file_path
        for file_path in path.rglob("*")
        if file_path.is_file()
        and file_path.suffix.lower()
        in [".md", ".markdown", ".jpg", ".jpeg", ".png", ".gif", ".webp"]
    ]

    for file_path in tqdm(local_files, desc="Processing files", unit="file"):
        relative_path = str(file_path.relative_to(path))

        # Check if it's a markdown file with frontmatter
        if file_path.suffix.lower() in [".md", ".markdown"]:
            frontmatter = parse_frontmatter(file_path)

            # If publish is false, schedule for deletion
            if frontmatter and frontmatter.get("publish") is False:
                if relative_path in remote_files:
                    logger.info(f"Deleting {relative_path} (publish: false)")
                    files_to_delete.add(relative_path)
                continue  # Don't upload

        # Upload the file
        logger.debug(f"Uploading {file_path}")
        try:
            with open(file_path, "rb") as file:
                files = {"file": file}
                data = {"url": relative_path}
                response = requests.post(
                    api_endpoint, files=files, data=data, headers=headers
                )
                if response.status_code == 200:
                    logger.debug(f"Successfully uploaded {file_path}")
                else:
                    logger.error(
                        f"Failed to upload {file_path}. Status code: {response.status_code}"
                    )
        except Exception as e:
            logger.error(f"Error uploading {file_path}: {str(e)}")

    # Now delete files that have publish: false or are not present locally
    all_files_to_delete = files_to_delete | (
        remote_files - set(map(lambda x: str(x.relative_to(path)), local_files))
    )

    for file_to_delete in tqdm(all_files_to_delete, desc="Deleting files", unit="file"):
        try:
            logger.debug(f"Deleting {file_to_delete}")
            response = requests.delete(
                api_endpoint, json={"url": file_to_delete}, headers=headers
            )
            if response.status_code == 200:
                logger.debug(f"Successfully deleted {file_to_delete}")
            elif response.status_code == 404:
                logger.debug(f"File {file_to_delete} not found on the server")
            else:
                logger.error(
                    f"Failed to delete {file_to_delete}. Status code: {response.status_code}"
                )
        except Exception as e:
            logger.error(f"Error deleting {file_to_delete}: {str(e)}")


if __name__ == "__main__":
    fire.Fire(mdsync)
