from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class NoThrottleSpectacularAPIView(SpectacularAPIView):
    permission_classes = (AllowAny,)
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class NoThrottleSpectacularSwaggerView(SpectacularSwaggerView):
    permission_classes = (AllowAny,)
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

class NoThrottleSpectacularRedocView(SpectacularRedocView):
    permission_classes = (AllowAny,)
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
