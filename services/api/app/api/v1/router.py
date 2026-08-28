from fastapi import APIRouter

from .health import router as health_router
from .devices.router import router as devices_router
from .agents.router import router as agents_router
from .tasks.router import router as tasks_router
from .capabilities.router import router as capabilities_router
from .permissions.router import router as permissions_router
from .applications.router import router as applications_router

router = APIRouter(prefix="/api/v1")
router.include_router(health_router)
router.include_router(devices_router)
router.include_router(agents_router)
router.include_router(tasks_router)
router.include_router(capabilities_router)
router.include_router(permissions_router)
router.include_router(applications_router)
