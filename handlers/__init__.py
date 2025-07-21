from aiogram import Router

from .auth import router as auth_router
from .houses import router as house_router


router = Router()



router.include_router(auth_router)
router.include_router(house_router)