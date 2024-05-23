from rest_framework.throttling import SimpleRateThrottle


class MessageRateThrottle(SimpleRateThrottle):
    scope = 'message'

    def get_cache_key(self, request, view):
        return self.cache_format % {
            'scope': self.scope,
            'ident': view.user_id
        }
