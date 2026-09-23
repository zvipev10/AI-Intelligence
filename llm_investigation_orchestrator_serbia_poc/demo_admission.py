"""One bounded, reentrant FIFO execution slot for all application agent paths."""
import functools
import threading
import time
import uuid
from contextlib import contextmanager


class AdmissionError(RuntimeError):
    pass


class AgentAdmission:
    def __init__(self, maintenance=lambda: False, capacity=8):
        self.maintenance = maintenance
        self.capacity = capacity
        self.condition = threading.Condition()
        self.waiting = []
        self.owner = None
        self.cancelled = set()

    def status(self):
        with self.condition:
            return {"running": int(self.owner is not None), "queued": len(self.waiting), "capacity": self.capacity, "queued_ids": [t[0] for t in self.waiting]}

    def cancel(self, ticket_id):
        with self.condition:
            if any(t[0] == ticket_id for t in self.waiting):
                self.cancelled.add(ticket_id)
                self.condition.notify_all()
                return True
            return False

    def next_ticket(self):
        # Foreground priority with aging: background cannot starve beyond 30s.
        return min(self.waiting, key=lambda t: (0 if time.monotonic() - t[2] > 30 else t[1], t[2]))

    @contextmanager
    def slot(self, timeout=600, foreground=False, ticket_id=None):
        thread = threading.get_ident()
        with self.condition:
            nested = self.owner == thread
        if nested:
            yield
            return
        ticket = (ticket_id or uuid.uuid4().hex, 0 if foreground else 1, time.monotonic())
        deadline = time.monotonic() + timeout
        with self.condition:
            if self.maintenance() or len(self.waiting) >= self.capacity:
                raise AdmissionError("Agent admission paused or queue full")
            self.waiting.append(ticket)
            try:
                while self.owner is not None or self.next_ticket() is not ticket:
                    if self.maintenance() or ticket[0] in self.cancelled or time.monotonic() >= deadline:
                        raise AdmissionError("Queued work cancelled during maintenance or timeout")
                    self.condition.wait(.25)
                if self.maintenance() or ticket[0] in self.cancelled:
                    raise AdmissionError("Scenario is switching")
                self.owner = thread
            finally:
                self.waiting.remove(ticket)
                self.cancelled.discard(ticket[0])
                self.condition.notify_all()
        try:
            yield
        finally:
            with self.condition:
                self.owner = None
                self.condition.notify_all()

    def wrap(self, function):
        @functools.wraps(function)
        def wrapped(*args, **kwargs):
            if kwargs.get("instruction_only"):
                return function(*args, **kwargs)
            with self.slot():
                return function(*args, **kwargs)
        return wrapped
