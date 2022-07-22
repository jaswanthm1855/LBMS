from rest_framework import generics
from rest_framework.response import Response
from library_store.views.register.serializer import RegisterSerializer, UserSerializer


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        self._register_user_details(request, user)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully. Now perform Login to get your token",
        })

    @staticmethod
    def _register_user_details(request, user):
        from library_store.interactors.register_user_details_interactor \
            import RegisterUserDetailsInteractor
        from library_store.storages.storage_implementation import StorageImplementation

        request_data = request.data
        role = request_data["role"]
        user_profile_details = {
            "user": user, "role": role,
        }

        storage = StorageImplementation()
        interactor = RegisterUserDetailsInteractor(storage=storage)
        interactor.register_user_details_wrapper(user_profile_details)
