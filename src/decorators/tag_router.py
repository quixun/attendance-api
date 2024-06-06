from fastapi import APIRouter


def tag_router(tag: str):
    def decorator(router_setup_function):
        def wrapper(*args, **kwargs):
            router = router_setup_function(*args, **kwargs)
            for route in router.routes:
                route.tags = [tag]
            return router
        return wrapper
    return decorator
