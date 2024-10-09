import logging
import os
import tempfile
import threading
import time
import uuid
from queue import Queue
from typing import Optional, Union
from concurrent.futures import ThreadPoolExecutor

from ..apis.maxim import MaximAPI

maximLogger = logging.getLogger("MaximSDK")


class LogWriterConfig:
    def __init__(self, base_url, api_key, repository_id, auto_flush=True, flush_interval: Optional[int] = 10, is_debug=False):
        self.base_url = base_url
        self.api_key = api_key
        self.repository_id = repository_id
        self.auto_flush = auto_flush
        self.flush_interval = flush_interval
        self.is_debug = is_debug
        maximLogger.setLevel(logging.DEBUG if is_debug else logging.INFO)


class LogWriter:
    def __init__(self, config: LogWriterConfig):
        self.is_running = True
        self.id = str(uuid.uuid4())
        self.config = config
        self.maxim_api = MaximAPI(config.base_url, config.api_key)
        self.queue = Queue()
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.is_debug = config.is_debug
        self.logs_dir = os.path.join(
            tempfile.gettempdir(), f"maxim-sdk/{self.id}/maxim-logs")
        self.__flush_thread = None
        os.makedirs(self.logs_dir, exist_ok=True)
        if self.config.auto_flush:
            if self.config.flush_interval:
                maximLogger.debug(
                    f"Starting flush thread with interval {self.config.flush_interval} seconds")
                self.__flush_thread = threading.Timer(
                    int(self.config.flush_interval), self.flush)
                self.__flush_thread.start()
            else:
                raise ValueError(
                    "flush_interval is set to None.flush_interval has to be a number")

    def is_running_on_lambda(self):
        return 'AWS_LAMBDA_FUNCTION_NAME' in os.environ

    def write_to_file(self, logs):
        try:
            filename = f"logs-{time.strftime('%Y-%m-%dT%H:%M:%SZ')}.log"
            filepath = os.path.join(self.logs_dir, filename)
            maximLogger.debug(f"Writing logs to file: {filename}")
            with open(filepath, 'w') as file:
                for log in logs:
                    file.write(log.serialize() + "\n")
            return filepath
        except Exception as e:
            maximLogger.error(f"Failed to write logs to file. We will keep it in memory. Error: {e}")
            return None

    def flush_log_files(self):
        try:
            if os.path.exists(self.logs_dir) == False:
                return
            files = os.listdir(self.logs_dir)
            for file in files:
                with open(os.path.join(self.logs_dir, file), 'r') as f:
                    logs = f.read()
                try:
                    self.maxim_api.pushLogs( self.config.repository_id, logs)
                    os.remove(os.path.join(self.logs_dir, file))
                except Exception as e:
                    if self.is_debug:
                        raise Exception(e)
        except Exception as e:
            maximLogger.error(f"Failed to access filesyste. Error: {e}")

    def flush_logs(self, logs):
        try:
            # Pushing old logs first
            self.flush_log_files()
            # Pushing new logs
            logs_to_push = "\n".join(
                [log.serialize() for log in logs])
            self.maxim_api.pushLogs(self.config.repository_id, logs_to_push)
            maximLogger.debug("Flush complete")
        except Exception as e:
            if self.is_running_on_lambda():
                maximLogger.debug("As we are running on lamda - we will keep logs in memory for next attempt")
                for log in logs:
                    self.queue.put(log)
                    maximLogger.debug("Logs added back to queue for next attempt")
            else:
                self.write_to_file(logs)
                maximLogger.error(
                    f"Failed to push logs to server. Writing logs to file. Error: {e}")

    def commit(self, log):
        self.queue.put(log)

    def flush(self):
        if self.is_running == False:
            return
        # Scheduling next call
        if self.config.flush_interval:
            self.__flush_thread = threading.Timer(
                int(self.config.flush_interval), self.flush)
            self.__flush_thread.start()
        items = []
        while not self.queue.empty():
            items.append(self.queue.get())
        if len(items) == 0:
            self.flush_log_files()
            maximLogger.debug("No logs to flush")
            return
        maximLogger.debug(
            f"Flushing logs to server {time.strftime('%Y-%m-%dT%H:%M:%S')}")
        if self.is_debug:
            for item in items:
                maximLogger.debug(f"{item.serialize()}")
        self.executor.submit(self.flush_logs, items)

    def cleanup(self):
        self.flush()
        self.is_running = False
        if self.__flush_thread:
            self.__flush_thread.cancel()
        self.executor.shutdown(wait=True)
