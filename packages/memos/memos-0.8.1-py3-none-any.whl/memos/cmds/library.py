import typer
import httpx
import asyncio
import logging
from tqdm import tqdm
from pathlib import Path
from tabulate import tabulate
from memos.config import settings
from magika import Magika
from datetime import datetime
from enum import Enum
from typing import List, Tuple
import os

from memos.read_metadata import read_metadata
from memos.schemas import MetadataSource


lib_app = typer.Typer()

file_detector = Magika()

IS_THUMBNAIL = "is_thumbnail"

BASE_URL = f"http://{settings.server_host}:{settings.server_port}"

include_files = [".jpg", ".jpeg", ".png", ".webp"]


class FileStatus(Enum):
    UPDATED = "updated"
    ADDED = "added"


def format_timestamp(timestamp):
    if isinstance(timestamp, str):
        return timestamp
    return datetime.fromtimestamp(timestamp).replace(tzinfo=None).isoformat()


def get_file_type(file_path):
    file_result = file_detector.identify_path(file_path)
    return file_result.output.ct_label, file_result.output.group


def display_libraries(libraries):
    table = []
    for library in libraries:
        table.append(
            [
                library["id"],
                library["name"],
                "\n".join(
                    f"{folder['id']}: {folder['path']}" for folder in library["folders"]
                ),
                "\n".join(
                    f"{plugin['id']}: {plugin['name']} {plugin['webhook_url']}"
                    for plugin in library["plugins"]
                ),
            ]
        )

    print(
        tabulate(table, headers=["ID", "Name", "Folders", "Plugins"], tablefmt="plain")
    )


@lib_app.command("ls")
def ls():
    response = httpx.get(f"{BASE_URL}/libraries")
    libraries = response.json()
    display_libraries(libraries)


@lib_app.command("create")
def add(name: str, folders: List[str]):
    absolute_folders = []
    for folder in folders:
        folder_path = Path(folder).resolve()
        absolute_folders.append({
            "path": str(folder_path),
            "last_modified_at": datetime.fromtimestamp(folder_path.stat().st_mtime).isoformat(),
        })

    response = httpx.post(
        f"{BASE_URL}/libraries",
        json={"name": name, "folders": absolute_folders},
    )
    if 200 <= response.status_code < 300:
        print("Library created successfully")
    else:
        print(f"Failed to create library: {response.status_code} - {response.text}")


@lib_app.command("add-folder")
def add_folder(library_id: int, folders: List[str]):
    absolute_folders = []
    for folder in folders:
        folder_path = Path(folder).resolve()
        absolute_folders.append({
            "path": str(folder_path),
            "last_modified_at": datetime.fromtimestamp(folder_path.stat().st_mtime).isoformat(),
        })

    response = httpx.post(
        f"{BASE_URL}/libraries/{library_id}/folders",
        json={"folders": absolute_folders},
    )
    if 200 <= response.status_code < 300:
        print("Folders added successfully")
        library = response.json()
        display_libraries([library])
    else:
        print(f"Failed to add folders: {response.status_code} - {response.text}")


@lib_app.command("show")
def show(library_id: int):
    response = httpx.get(f"{BASE_URL}/libraries/{library_id}")
    if response.status_code == 200:
        library = response.json()
        display_libraries([library])
    else:
        print(f"Failed to retrieve library: {response.status_code} - {response.text}")


async def loop_files(library_id, folder, folder_path, force, plugins):
    updated_file_count = 0
    added_file_count = 0
    scanned_files = set()
    semaphore = asyncio.Semaphore(settings.batchsize)
    async with httpx.AsyncClient(timeout=60) as client:
        tasks = []
        for root, _, files in os.walk(folder_path):
            with tqdm(total=len(files), desc=f"Scanning {root}", leave=True) as pbar:
                candidate_files = []
                for file in files:
                    file_path = Path(root) / file
                    absolute_file_path = file_path.resolve()  # Get absolute path
                    relative_path = absolute_file_path.relative_to(folder_path)

                    # Check if the file extension is in the include_files list
                    if file_path.suffix.lower() in include_files:
                        scanned_files.add(str(absolute_file_path))
                        candidate_files.append(str(absolute_file_path))

                batching = 200
                for i in range(0, len(candidate_files), batching):
                    batch = candidate_files[i : i + batching]

                    # Get batch of entities
                    get_response = await client.post(
                        f"{BASE_URL}/libraries/{library_id}/entities/by-filepaths",
                        json=batch,
                    )

                    if get_response.status_code == 200:
                        existing_entities = get_response.json()
                    else:
                        print(
                            f"Failed to get entities: {get_response.status_code} - {get_response.text}"
                        )
                        continue

                    existing_entities_dict = {
                        entity["filepath"]: entity for entity in existing_entities
                    }

                    for file_path in batch:
                        absolute_file_path = Path(file_path).resolve()
                        file_stat = absolute_file_path.stat()
                        file_type, file_type_group = get_file_type(absolute_file_path)

                        new_entity = {
                            "filename": absolute_file_path.name,
                            "filepath": str(absolute_file_path),
                            "size": file_stat.st_size,
                            "file_created_at": format_timestamp(file_stat.st_ctime),
                            "file_last_modified_at": format_timestamp(
                                file_stat.st_mtime
                            ),
                            "file_type": file_type,
                            "file_type_group": file_type_group,
                            "folder_id": folder["id"],
                        }

                        is_thumbnail = False

                        if file_type_group == "image":
                            metadata = read_metadata(absolute_file_path)
                            if metadata:
                                if (
                                    "active_window" in metadata
                                    and "active_app" not in metadata
                                ):
                                    metadata["active_app"] = metadata[
                                        "active_window"
                                    ].split(" - ")[0]
                                new_entity["metadata_entries"] = [
                                    {
                                        "key": key,
                                        "value": str(value),
                                        "source": MetadataSource.SYSTEM_GENERATED.value,
                                        "data_type": (
                                            "number"
                                            if isinstance(value, (int, float))
                                            else "text"
                                        ),
                                    }
                                    for key, value in metadata.items()
                                    if key != IS_THUMBNAIL
                                ]
                                if "active_app" in metadata:
                                    new_entity.setdefault("tags", []).append(
                                        metadata["active_app"]
                                    )
                                is_thumbnail = metadata.get(IS_THUMBNAIL, False)

                        existing_entity = existing_entities_dict.get(
                            str(absolute_file_path)
                        )
                        if existing_entity:
                            existing_created_at = format_timestamp(
                                existing_entity["file_created_at"]
                            )
                            new_created_at = format_timestamp(
                                new_entity["file_created_at"]
                            )
                            existing_modified_at = format_timestamp(
                                existing_entity["file_last_modified_at"]
                            )
                            new_modified_at = format_timestamp(
                                new_entity["file_last_modified_at"]
                            )

                            # Ignore file changes for thumbnails
                            if is_thumbnail:
                                new_entity["file_created_at"] = existing_entity[
                                    "file_created_at"
                                ]
                                new_entity["file_last_modified_at"] = existing_entity[
                                    "file_last_modified_at"
                                ]
                                new_entity["file_type"] = existing_entity["file_type"]
                                new_entity["file_type_group"] = existing_entity[
                                    "file_type_group"
                                ]
                                new_entity["size"] = existing_entity["size"]

                            # Merge existing metadata with new metadata
                            if new_entity.get("metadata_entries"):
                                new_metadata_keys = {
                                    entry["key"]
                                    for entry in new_entity["metadata_entries"]
                                }
                                for existing_entry in existing_entity[
                                    "metadata_entries"
                                ]:
                                    if existing_entry["key"] not in new_metadata_keys:
                                        new_entity["metadata_entries"].append(
                                            existing_entry
                                        )

                            if (
                                force
                                or existing_created_at != new_created_at
                                or existing_modified_at != new_modified_at
                            ):
                                tasks.append(
                                    update_entity(
                                        client,
                                        semaphore,
                                        plugins,
                                        new_entity,
                                        existing_entity,
                                    )
                                )
                        elif not is_thumbnail:  # Ignore thumbnails
                            tasks.append(
                                add_entity(
                                    client, semaphore, library_id, plugins, new_entity
                                )
                            )
                    pbar.update(len(batch))
                    pbar.set_postfix({"Candidates": len(tasks)}, refresh=True)

        # Process all tasks after they've been created
        for future in tqdm(
            asyncio.as_completed(tasks),
            desc=f"Processing {folder_path}",
            total=len(tasks),
            leave=True,
        ):
            file_path, file_status, succeeded, response = await future
            if file_status == FileStatus.ADDED:
                if succeeded:
                    added_file_count += 1
                    tqdm.write(f"Added file to library: {file_path}")
                else:
                    error_message = "Failed to add file"
                    if hasattr(response, "status_code"):
                        error_message += f": {response.status_code}"
                    if hasattr(response, "text"):
                        error_message += f" - {response.text}"
                    else:
                        error_message += " - Unknown error occurred"
                    tqdm.write(error_message)
            elif file_status == FileStatus.UPDATED:
                if succeeded:
                    updated_file_count += 1
                    tqdm.write(f"Updated file in library: {file_path}")
                else:
                    error_message = "Failed to update file"
                    if hasattr(response, "status_code"):
                        error_message += f": {response.status_code}"
                    elif hasattr(response, "text"):
                        error_message += f" - {response.text}"
                    else:
                        error_message += f" - Unknown error occurred"
                    tqdm.write(error_message)

        return added_file_count, updated_file_count, scanned_files


@lib_app.command("scan")
def scan(
    library_id: int,
    force: bool = False,
    plugins: List[int] = typer.Option(None, "--plugin", "-p"),
    folders: List[int] = typer.Option(None, "--folder", "-f"),
):

    response = httpx.get(f"{BASE_URL}/libraries/{library_id}")
    if response.status_code != 200:
        print(f"Failed to retrieve library: {response.status_code} - {response.text}")
        return

    library = response.json()
    total_files_added = 0
    total_files_updated = 0
    total_files_deleted = 0

    # Filter folders if the folders parameter is provided
    if folders:
        library_folders = [
            folder for folder in library["folders"] if folder["id"] in folders
        ]
    else:
        library_folders = library["folders"]

    for folder in library_folders:
        folder_path = Path(folder["path"])
        if not folder_path.exists() or not folder_path.is_dir():
            tqdm.write(f"Folder does not exist or is not a directory: {folder_path}")
            continue

        added_file_count, updated_file_count, scanned_files = asyncio.run(
            loop_files(library_id, folder, folder_path, force, plugins)
        )
        total_files_added += added_file_count
        total_files_updated += updated_file_count

        # Check for deleted files
        limit = 100
        offset = 0
        total_entities = 0  # We'll update this after the first request
        with tqdm(
            total=total_entities, desc="Checking for deleted files", leave=True
        ) as pbar2:
            while True:
                existing_files_response = httpx.get(
                    f"{BASE_URL}/libraries/{library_id}/folders/{folder['id']}/entities",
                    params={"limit": limit, "offset": offset},
                    timeout=60,
                )
                if existing_files_response.status_code != 200:
                    pbar2.write(
                        f"Failed to retrieve existing files: {existing_files_response.status_code} - {existing_files_response.text}"
                    )
                    break

                existing_files = existing_files_response.json()
                if not existing_files:
                    break

                # Update total if this is the first request
                if offset == 0:
                    total_entities = int(
                        existing_files_response.headers.get(
                            "X-Total-Count", total_entities
                        )
                    )
                    pbar2.total = total_entities
                    pbar2.refresh()

                for existing_file in existing_files:
                    if existing_file["filepath"] not in scanned_files:
                        # File has been deleted
                        delete_response = httpx.delete(
                            f"{BASE_URL}/libraries/{library_id}/entities/{existing_file['id']}"
                        )
                        if 200 <= delete_response.status_code < 300:
                            pbar2.write(
                                f"Deleted file from library: {existing_file['filepath']}"
                            )
                            total_files_deleted += 1
                        else:
                            pbar2.write(
                                f"Failed to delete file: {delete_response.status_code} - {delete_response.text}"
                            )
                    pbar2.update(1)

                offset += limit

    print(f"Total files added: {total_files_added}")
    print(f"Total files updated: {total_files_updated}")
    print(f"Total files deleted: {total_files_deleted}")


async def add_entity(
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    library_id,
    plugins,
    new_entity,
) -> Tuple[FileStatus, bool, httpx.Response]:
    async with semaphore:
        MAX_RETRIES = 3
        RETRY_DELAY = 2.0
        for attempt in range(MAX_RETRIES):
            try:
                post_response = await client.post(
                    f"{BASE_URL}/libraries/{library_id}/entities",
                    json=new_entity,
                    params={"plugins": plugins} if plugins else {},
                    timeout=60,
                )
                if 200 <= post_response.status_code < 300:
                    return new_entity["filepath"], FileStatus.ADDED, True, post_response
                else:
                    return (
                        new_entity["filepath"],
                        FileStatus.ADDED,
                        False,
                        post_response,
                    )
            except Exception as e:
                logging.error(
                    f"Error while adding entity (attempt {attempt + 1}/{MAX_RETRIES}): {e}"
                )
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(RETRY_DELAY)
                else:
                    return new_entity["filepath"], FileStatus.ADDED, False, None


async def update_entity(
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    plugins,
    new_entity,
    existing_entity,
) -> Tuple[FileStatus, bool, httpx.Response]:
    MAX_RETRIES = 3
    RETRY_DELAY = 2.0
    async with semaphore:
        for attempt in range(MAX_RETRIES):
            try:
                update_response = await client.put(
                    f"{BASE_URL}/entities/{existing_entity['id']}",
                    json=new_entity,
                    params={
                        "trigger_webhooks_flag": "true",
                        **({"plugins": plugins} if plugins else {}),
                    },
                    timeout=60,
                )
                if 200 <= update_response.status_code < 300:
                    return (
                        new_entity["filepath"],
                        FileStatus.UPDATED,
                        True,
                        update_response,
                    )
                else:
                    return (
                        new_entity["filepath"],
                        FileStatus.UPDATED,
                        False,
                        update_response,
                    )
            except Exception as e:
                logging.error(
                    f"Error while updating entity {existing_entity['id']} (attempt {attempt + 1}/{MAX_RETRIES}): {e}"
                )
                if attempt < MAX_RETRIES - 1:
                    await asyncio.sleep(RETRY_DELAY)
                else:
                    return new_entity["filepath"], FileStatus.UPDATED, False, None


async def check_and_index_entity(client, entity_id, entity_last_scan_at):
    try:
        index_response = await client.get(f"{BASE_URL}/entities/{entity_id}/index")
        if index_response.status_code == 200:
            index_data = index_response.json()
            if index_data["last_scan_at"] is None:
                return entity_last_scan_at is not None
            index_last_scan_at = datetime.fromtimestamp(index_data["last_scan_at"])
            entity_last_scan_at = datetime.fromisoformat(entity_last_scan_at)

            if index_last_scan_at >= entity_last_scan_at:
                return False  # Index is up to date, no need to update
        return True  # Index doesn't exist or needs update
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return True  # Index doesn't exist, need to create
        raise  # Re-raise other HTTP errors


async def index_batch(client, entity_ids):
    index_response = await client.post(
        f"{BASE_URL}/entities/batch-index",
        json=entity_ids,
        timeout=60,
    )
    return index_response


@lib_app.command("index")
def index(
    library_id: int,
    folders: List[int] = typer.Option(None, "--folder", "-f"),
    force: bool = typer.Option(False, "--force", help="Force update all indexes"),
    batchsize: int = typer.Option(
        4, "--batchsize", "-bs", help="Number of entities to index in a batch"
    ),
):
    print(f"Indexing library {library_id}")

    # Get the library
    response = httpx.get(f"{BASE_URL}/libraries/{library_id}")
    if response.status_code != 200:
        print(f"Failed to get library: {response.status_code} - {response.text}")
        return

    library = response.json()
    scanned_entities = set()

    # Filter folders if the folders parameter is provided
    if folders:
        library_folders = [
            folder for folder in library["folders"] if folder["id"] in folders
        ]
    else:
        library_folders = library["folders"]

    async def process_folders():
        async with httpx.AsyncClient(timeout=60) as client:
            # Iterate through folders
            for folder in library_folders:
                tqdm.write(f"Processing folder: {folder['id']}")

                # List all entities in the folder
                limit = 200
                offset = 0
                total_entities = 0  # We'll update this after the first request
                with tqdm(
                    total=total_entities, desc="Indexing entities", leave=True
                ) as pbar:
                    while True:
                        entities_response = await client.get(
                            f"{BASE_URL}/libraries/{library_id}/folders/{folder['id']}/entities",
                            params={"limit": limit, "offset": offset},
                        )
                        if entities_response.status_code != 200:
                            pbar.write(
                                f"Failed to get entities: {entities_response.status_code} - {entities_response.text}"
                            )
                            break

                        entities = entities_response.json()
                        if not entities:
                            break

                        # Update total if this is the first request
                        if offset == 0:
                            total_entities = int(
                                entities_response.headers.get(
                                    "X-Total-Count", total_entities
                                )
                            )
                            pbar.total = total_entities
                            pbar.refresh()

                        # Index each entity
                        for i in range(0, len(entities), batchsize):
                            batch = entities[i : i + batchsize]
                            to_index = []

                            for entity in batch:
                                needs_indexing = force or await check_and_index_entity(
                                    client, entity["id"], entity["last_scan_at"]
                                )
                                if needs_indexing:
                                    to_index.append(entity["id"])

                            if to_index:
                                index_response = await index_batch(client, to_index)
                                if index_response.status_code == 204:
                                    pbar.write(
                                        f"Indexed batch of {len(to_index)} entities"
                                    )
                                else:
                                    pbar.write(
                                        f"Failed to index batch: {index_response.status_code} - {index_response.text}"
                                    )

                            scanned_entities.update(
                                str(entity["id"]) for entity in batch
                            )
                            pbar.update(len(batch))

                        offset += limit

                # List all indexed entities in the folder
                offset = 0
                print(f"Starting cleanup process for folder {folder['id']}")
                while True:
                    index_response = await client.get(
                        f"{BASE_URL}/libraries/{library_id}/folders/{folder['id']}/index",
                        params={"limit": 200, "offset": offset},
                    )
                    if index_response.status_code != 200:
                        tqdm.write(
                            f"Failed to get indexed entities: {index_response.status_code} - {index_response.text}"
                        )
                        break

                    indexed_entities = index_response.json()
                    if not indexed_entities:
                        print("No more indexed entities to process")
                        break

                    # Delete indexes for entities not in scanned_entities
                    for indexed_entity in tqdm(
                        indexed_entities, desc="Cleaning up indexes", leave=False
                    ):
                        if indexed_entity["id"] not in scanned_entities:
                            tqdm.write(
                                f"Entity {indexed_entity['id']} not in scanned entities, deleting index"
                            )
                            delete_response = await client.delete(
                                f"{BASE_URL}/entities/{indexed_entity['id']}/index"
                            )
                            if delete_response.status_code == 204:
                                tqdm.write(
                                    f"Deleted index for entity: {indexed_entity['id']}"
                                )
                            else:
                                tqdm.write(
                                    f"Failed to delete index for entity {indexed_entity['id']}: {delete_response.status_code} - {delete_response.text}"
                                )

                    offset += 200

                print(f"Finished cleanup process for folder {folder['id']}")

    asyncio.run(process_folders())
    print("Indexing completed")
