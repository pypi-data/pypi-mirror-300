from typing import Optional

from bi_etl.notifiers.notifier_base import NotifierBase


class LogNotifier(NotifierBase):
    def __init__(self, *, name: Optional[str] = None):
        super().__init__(name=name)

    def send(self, subject, message, sensitive_message=None, attachment=None, throw_exception=False):
        if subject is not None:
            self.log.info(subject)
        if message is not None:
            self.log.info(message)
        if sensitive_message is not None and self.config_section.include_sensitive:
            self.log.info(sensitive_message)
