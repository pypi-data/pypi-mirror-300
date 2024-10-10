"""
controller_registry에 등록된 함수들을 라우팅합니다.
"""

# router.py
import inspect
from sawsi.handler.controller_decorator import controller_registry
from sawsi.shared import error_util


def router(cmd: str, body: dict, headers: dict, allowed_cmd_prefixes: list):
    """
    :param cmd:
    :param body:
    :param headers:
    :param allowed_cmd_prefixes: EX: ['user', 'admin']
    :return:
    """
    # prefix 검사
    if not any(cmd.startswith(prefix) for prefix in allowed_cmd_prefixes):
        raise error_util.SYSTEM_NO_SUCH_CMD(f"Command prefix not allowed: {cmd}")

    if cmd in controller_registry:
        func = controller_registry[cmd]

        # 함수의 파라미터 목록을 추출
        signature = inspect.signature(func)
        # 함수의 매개변수 중 body에 있는 것만 필터링
        filtered_body = {k: v for k, v in body.items() if k in signature.parameters}

        return func(**filtered_body)
    else:
        # CMD에 해당하는 컨트롤러가 없으면 에러 발생
        raise error_util.SYSTEM_NO_SUCH_CMD
