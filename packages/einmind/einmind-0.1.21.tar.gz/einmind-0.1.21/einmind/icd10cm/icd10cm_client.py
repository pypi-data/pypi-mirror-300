import time
from einmind.icd10cm.schemas import Prediction, TaskStatus, TaskStates
from pydantic import HttpUrl
from einmind.api_handler import APIHandler
from datetime import datetime, timedelta


class ICD10CMClient:
    def __init__(
            self,
             base_url: HttpUrl = None,
             api_key: str=None
    ):
        self.api_handler: APIHandler = APIHandler(
            base_url=base_url,
            api_key=api_key
        )

    def code_term(self, term, time_out=20):
        assert time_out > 1, "time_out: must be higher than 1"

        payload = {'term': term}
        response = self.api_handler.post('sdk/icd10cm/term_coding/create_task', payload)

        if response.status_code != 200:
            raise Exception(f"Failed to create task: {response.text}")

        task_id = response.json().get('task_id')
        return self._monitor_task(task_id, time_out=time_out)

    def _monitor_task(self, task_id: str, time_out: int) -> TaskStatus:
        start_time = datetime.now()

        while True:
            response = self.api_handler.get(f'sdk/icd10cm/term_coding/get_task?task_id={task_id}')

            if response.status_code != 200:
                raise Exception(f"Failed to monitor task: {response.text}")

            task_status = response.json().get('task_status')
            if task_status == TaskStates.COMPLETED:
                top_prediction_data = response.json().get('top_prediction')
                top_prediction = Prediction(
                    code=top_prediction_data['code'],
                    title=top_prediction_data['title'],
                    confidence=top_prediction_data['confidence'],
                )
                task_status = TaskStatus(
                    task_state=TaskStates.COMPLETED,
                    task_failed_msg=None,
                    prediction=top_prediction

                )
                return task_status

            elif task_status == TaskStates.FAILED:
                task_fail_rsn = response.json().get('task_fail_rsn')
                task_status = TaskStatus(
                    task_state=TaskStates.FAILED,
                    task_failed_msg=task_fail_rsn,
                    prediction=None
                )
                return task_status

            # Check if the timeout has been reached
            if datetime.now() - start_time > timedelta(seconds=time_out):
                task_status = TaskStatus(
                    task_state=TaskStates.FAILED,
                    task_failed_msg=f"Task timed out after {time_out} seconds.",
                    prediction=None
                )
                return task_status

            time.sleep(1)
