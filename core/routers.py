from menu.handlers import start_router, menu_callback_router, menu_state_router
from admin.routers import admin_callback_router, admin_panel_router

routers = [
    admin_callback_router,
    admin_panel_router,
    start_router,
    menu_callback_router,
    menu_state_router,

]