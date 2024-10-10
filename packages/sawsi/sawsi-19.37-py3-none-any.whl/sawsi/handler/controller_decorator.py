"""
각 함수에 데코레이터를 적용하여 특정 경로로 라우팅되도록 만들기 위해 데코레이터를 정의합니다.
"""

# controller_decorator.py
controller_registry = {}

def controller(route):
    def decorator(func):
        controller_registry[route + '.' + func.__name__] = func
        return func
    return decorator
