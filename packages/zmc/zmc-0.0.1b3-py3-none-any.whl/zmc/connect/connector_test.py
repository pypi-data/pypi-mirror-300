import asyncio
import threading
import pytest

from .connector import Connector as ConnectorBase


class Connector(ConnectorBase):

    def start_task_from_connector_thread(self, task):

        async def execute_task():
            self._execute_in_new_thread(task)

        asyncio.run_coroutine_threadsafe(
            execute_task(),
            self.__connector_loop,
        )

    async def _send_component_data(self, component):
        pass

    async def _start_connector(self):
        self.is_connected = True
        self.server_thread_id = threading.get_ident()

    async def _stop_connector(self):
        """Stops the mock 'connector'."""


@pytest.fixture
def mock_connector(mocker):
    connector_instance = Connector()
    connector_instance.start_connector()
    yield connector_instance
    connector_instance.stop_connector()


@pytest.mark.timeout(1)
def test_tasks_run_on_separate_threads(mock_connector):
    task_started = threading.Event()
    continue_task = threading.Event()
    task_completed = threading.Event()

    main_thread_id = threading.get_ident()
    task_thread_id = None

    def task():
        task_started.set()
        nonlocal task_thread_id
        task_thread_id = threading.get_ident()

        continue_task.wait()
        task_completed.set()

    mock_connector.start_task_from_connector_thread(task)

    assert task_started.wait(timeout=1)
    assert task_thread_id is not None

    # Assert main/server/task are all operating on different threads.
    assert task_thread_id != main_thread_id
    assert task_thread_id != mock_connector.server_thread_id
    assert main_thread_id != mock_connector.server_thread_id

    assert not task_completed.is_set()

    continue_task.set()
    assert task_completed.wait(timeout=1)


def test_task_exception_handling(mock_connector, mocker):
    exception_handled = threading.Event()
    mock_exception_handler = mocker.Mock()

    def exception_handler(exception):
        mock_exception_handler(exception)
        exception_handled.set()

    mock_connector._handle_thread_exception = exception_handler

    def task():
        raise ValueError("Test exception")

    mock_connector.start_task_from_connector_thread(task)

    assert exception_handled.wait(timeout=1)

    mock_exception_handler.assert_called_once()
    exception = mock_exception_handler.call_args[0][0]
    assert isinstance(exception, ValueError)
    assert str(exception) == "Test exception"


# TODO: Implement the rest of the tests for the Connector class
