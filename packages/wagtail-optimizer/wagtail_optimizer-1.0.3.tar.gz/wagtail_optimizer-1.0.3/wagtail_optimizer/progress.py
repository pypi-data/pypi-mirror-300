from decimal import Decimal
from celery import Task
from celery.result import (
    allow_join_result, states, AsyncResult,
)

import logging, re

logger = logging.getLogger("wagtail_optimizer")


PROGRESS_STATE = 'PROGRESS'


class ProgressRecorder:
    def __init__(self, task: Task):
        self.task = task
        self.current = 0
        self.total = 0
        self.description = ""

    def increment_progress(self, by=1, description=""):
        """
        Increments progress by one, with an optional description. Useful if the caller doesn't know the total.
        """
        self.set_progress(self.current + by, self.total, description)

    def set_progress(self, current, total, description=""):
        self.current = current
        self.total = total

        if description:
            self.description = description

        percent = 0
        if total > 0:
            percent = (Decimal(current) / Decimal(total)) * Decimal(100)
            percent = float(round(percent, 2))

        state = PROGRESS_STATE

        meta = {
            'pending': False,
            'current': current,
            'total': total,
            'percent': percent,
            'description': description
        }

        self.task.update_state(
            state=state,
            meta=meta
        )

        return state, meta
    
class Progress(object):

    def __init__(self, result: AsyncResult):
        """
        result:
            an AsyncResult or an object that mimics it to a degree
        """
        self.result = result

    def get_info(self):
        task_meta = self.result._get_task_meta()
        state = task_meta["status"]
        info = task_meta["result"]
        response = {'state': state}

        if state in [states.SUCCESS, states.FAILURE]:
            success = self.result.successful()
            with allow_join_result():
                response.update({
                    'complete': True,
                    'success': success,
                    'progress': _get_completed_progress(),
                    'result': self.result.get(self.result.id) if success else str(info),
                })

        elif state in [states.RETRY, states.REVOKED]:
            if state == states.RETRY:
                # in a retry sceneario, result is the exception, and 'traceback' has the details
                # https://docs.celeryq.dev/en/stable/userguide/tasks.html#retry
                traceback = task_meta.get("traceback")
                seconds_re = re.search(r"Retry in \d{1,10}s", traceback)
                if seconds_re:
                    next_retry_seconds = int(seconds_re.group()[9:-1])
                else:
                    next_retry_seconds = "Unknown"

                result = {"next_retry_seconds": next_retry_seconds, "message": f"{str(task_meta['result'])[0:50]}..."}
            else:
                result = 'Task ' + str(info)

            response.update({
                'complete': True,
                'success': False,
                'progress': _get_completed_progress(),
                'result': result,
            })

        elif state == states.IGNORED:
            response.update({
                'complete': True,
                'success': None,
                'progress': _get_completed_progress(),
                'result': str(info)
            })

        elif state == PROGRESS_STATE:
            response.update({
                'complete': False,
                'success': None,
                'progress': info,
            })

        elif state in [states.PENDING, states.STARTED]:
            response.update({
                'complete': False,
                'success': None,
                'progress': _get_unknown_progress(state),
            })

        else:
            logger.error('Task %s has unknown state %s with metadata %s', self.result.id, state, info)
            response.update({
                'complete': True,
                'success': False,
                'progress': _get_unknown_progress(state),
                'result': 'Unknown state {}'.format(state),
            })

        return response

    @property
    def is_failed(self):
        info = self.get_info()
        return info["complete"] and info["success"] is False
    
def _get_completed_progress():
    return {
        'pending': False,
        'current': 100,
        'total': 100,
        'percent': 100,
    }


def _get_unknown_progress(state):
    return {
        'pending': state == states.PENDING,
        'current': 0,
        'total': 100,
        'percent': 0,
    }
