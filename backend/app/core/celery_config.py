from celery import Celery
from ..core.config import settings

celery_app = Celery(
    main="booking_service_celery",
    broker=settings.redis.url,
    backend=settings.redis.url
)

celery_app.autodiscover_tasks(packages=["backend.app.core"])
from ..core.celery_tasks import send_booking_code