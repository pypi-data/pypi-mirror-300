import asyncio
import aiohttp
import time
import os
from datetime import datetime
from typing import Dict, Any
import pytz
from urllib.parse import quote
from botrun_ask_folder.constants import MAX_CONCURRENT_PROCESS_FILES
from botrun_ask_folder.embeddings_to_qdrant import has_collection_in_qdrant
from botrun_ask_folder.util.timestamp_encryp import (
    encrypt_timestamp,
    get_current_timestamp,
)
from .emoji_progress_bar import EmojiProgressBar
from .botrun_drive_manager import botrun_drive_manager
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

API_URL = os.getenv("BOTRUN_ASK_FOLDER_FAST_API_URL") + "/api/botrun/botrun_ask_folder"
API_TIMEOUT = 60
CHECK_INTERVAL = 20
BOTRUN_ASK_FOLDER_JWT_STATIC_TOKEN = os.getenv("BOTRUN_ASK_FOLDER_JWT_STATIC_TOKEN")
FOLDER_STATUS_ENC_KEY = os.getenv("FOLDER_STATUS_ENC_KEY")


async def process_folder_from_restapi(folder_id: str, force: bool = False):
    qdrant_host = os.getenv("QDRANT_HOST", "qdrant")
    qdrant_port = int(os.getenv("QDRANT_PORT", 6333))
    qdrant_api_key = os.getenv("QDRANT_API_KEY", "")
    collection_existed = await has_collection_in_qdrant(
        f"{folder_id}",
        qdrant_host,
        qdrant_port,
        qdrant_api_key,
    )
    headers = {"Authorization": f"Bearer {BOTRUN_ASK_FOLDER_JWT_STATIC_TOKEN}"}
    async with aiohttp.ClientSession() as session:
        # Start processing the folder
        process_url = f"{API_URL}/process-folder-job"
        data = {
            "folder_id": folder_id,
            "force": force,
            "embed": True,
            "qdrant_host": qdrant_host,
            "qdrant_port": qdrant_port,
            "qdrant_api_key": qdrant_api_key,
        }

        time1 = time.time()
        print(f"開始執行資料 {folder_id} 匯入工作 {get_timestamp()}")
        async with session.post(
            process_url, json=data, headers=headers, timeout=API_TIMEOUT
        ) as response:
            initial_response = await response.json()
            if initial_response.get("status") == "success":
                print(
                    f"條列所有 {folder_id} 的檔案, job_id: {initial_response.get('job_id')} {get_timestamp()}"
                )
            else:
                print(
                    f"資料 {folder_id} 匯入工作失敗: 得到訊息 {initial_response} {get_timestamp()}"
                )
                return

        # Initialize EmojiProgressBar
        # progress_bar = EmojiProgressBar(total=1)  # Initialize with 1, will update later
        # progress_bar.set_description(
        #     f"{folder_id} 資料匯入中，檢查狀態更新時間：{get_timestamp()}"
        # )

        # Check status periodically
        status_url = f"{API_URL}/folder-status"
        action_started_at_datetime = datetime.now(pytz.timezone("Asia/Taipei"))
        action_started_at = action_started_at_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # URL encode the parameters
        encoded_folder_id = quote(folder_id)

        enc_data = encrypt_timestamp(action_started_at_datetime)

        check_url = f"{API_URL}/folder_status_web?folder_id={encoded_folder_id}&enc_data={enc_data}&action_started_at={action_started_at}"

        print(f"請點擊此連結檢查匯入狀態：{check_url}")
        while True:
            await asyncio.sleep(CHECK_INTERVAL)

            try:
                async with session.post(
                    status_url,
                    json={
                        "folder_id": folder_id,
                        "action_started_at": action_started_at,
                    },
                    headers=headers,
                    timeout=API_TIMEOUT,
                ) as response:
                    status = await response.json()
                if status.get("status") == "WAITING":
                    # print(f"{folder_id} 初始化中，檢查狀態更新時間：{get_timestamp()}")
                    continue
                total_files = status.get("total_files", 0)
                # embedded_files = status.get("embedded_files", 0)

                if total_files > 0 and status.get("status") != "DONE":
                    # print(
                    #     f"{folder_id} 資料匯入中，檢查狀態更新時間：{get_timestamp()}"
                    # )
                    pass

                if status.get("status") == "DONE":
                    print(f"{folder_id} 資料匯入完成，可以開始使用 {get_timestamp()}")
                    time2 = time.time()
                    total_seconds = int(time2 - time1)
                    minutes, seconds = divmod(total_seconds, 60)
                    time_str = f"{minutes:02d}:{seconds:02d}"
                    print(
                        f"資料匯入完成，花費時間：{time_str}，共處理 {total_files} 個檔案"
                    )
                    if not collection_existed:
                        botrun_drive_manager(
                            f"波{folder_id}", f"{folder_id}", force=force
                        )
                    elif force:
                        botrun_drive_manager(
                            f"波{folder_id}", f"{folder_id}", force=force
                        )
                    return
                elif status.get("status") == "FAILED":
                    print(
                        f"{folder_id} 資料匯入有發生錯誤，請連繫我們最貼心的客服夥伴們喔！"
                    )
                    return

            except asyncio.TimeoutError:
                print(f"檢查匯入工作 {folder_id} 逾時 {get_timestamp()}")
            except Exception as e:
                print(f"檢查匯入工作 {folder_id} 失敗: {str(e)} {get_timestamp()}")


def process_folder(folder_id: str, force: bool = False) -> Dict[str, Any]:
    return asyncio.run(process_folder_from_restapi(folder_id, force))


def get_timestamp():
    return datetime.now(pytz.timezone("Asia/Taipei")).strftime("%Y-%m-%d %H:%M:%S")
