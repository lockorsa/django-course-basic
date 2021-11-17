from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator


class AccessMixin:
    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CallableMixin:
    def __call__(self, request, *args, **kwargs):
        self.setup(request, *args, **kwargs)
        return self.dispatch(request, *args, **kwargs)
