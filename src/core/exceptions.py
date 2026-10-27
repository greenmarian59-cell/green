"""Domen xatolari.

Servis qatlami HTTP haqida bilmaydi — u shunchaki mos xatoni ko'taradi,
`src.main` dagi handler esa uni `status_code` bo'yicha HTTP javobga o'giradi.
"""


class AppError(Exception):
    """Barcha domen xatolari uchun asosiy klass.

    Attributes:
        status_code: Javobning HTTP status kodi.
        detail: Foydalanuvchiga ko'rsatiladigan xabar.
    """

    status_code: int = 500
    detail: str = "Internal server error"

    def __init__(self, detail: str | None = None) -> None:
        # `detail` berilmasa, klassdagi default xabar ishlatiladi.
        self.detail = detail or type(self).detail
        super().__init__(self.detail)


class NotFoundError(AppError):
    """So'ralgan resurs topilmadi."""

    status_code = 404
    detail = "Not found"


class ConflictError(AppError):
    """Amal joriy holat bilan ziddiyatda (dublikat, band resurs va h.k.)."""

    status_code = 409
    detail = "Already exists"


class UnauthorizedError(AppError):
    """Autentifikatsiya o'tmadi — login yoki token yaroqsiz."""

    status_code = 401
    detail = "Invalid credentials"


class ForbiddenError(AppError):
    """Kim ekanligi aniq, lekin bu amalga ruxsati yo'q."""

    status_code = 403
    detail = "Forbidden"
