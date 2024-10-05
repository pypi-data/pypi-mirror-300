from core.logging import log_function_call


class MyService:
    def __init__(self, config_service):
        self.config_service = config_service

    def get_config(self):
        return self.config_service.get_config()

    @log_function_call(log_level="info")
    def get_fibonacci(self, x):
        if x == 0:
            return 0
        elif x == 1:
            return 1
        a, b = 0, 1
        for _ in range(2, x + 1):
            a, b = b, a + b
        return b
