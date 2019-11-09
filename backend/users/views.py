from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.users import models, serializers, choices


class ProfileViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):

    # pylint: disable=no-member

    queryset = models.Profile.objects.all()
    serializer_class = serializers.base.ProfileSerializer


class LicenseViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):

    # pylint: disable=no-member

    queryset = models.License.objects.all()
    serializer_class = serializers.base.LicenseSerializer


class DriverViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):

    # pylint: disable=no-member

    queryset = models.Driver.objects.all()
    serializer_class = serializers.base.DriverSerializer


class FeeViewSet(mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):

    # pylint: disable=no-member

    queryset = models.Fee.objects
    serializer_class = serializers.base.FeeSerializer

    def get_queryset(self):
        queryset = self.queryset

        serializer = serializers.query.FeeQuerySerializer(
            data=self.request.query_params)

        if not serializer.is_valid():
            return queryset.all()

        is_paid = serializer.validated_data.get('is_paid', None)
        if is_paid is not None:
            queryset = queryset.filter(is_paid=is_paid)

        driver_id = serializer.validated_data.get('driver_id', None)
        if driver_id:
            queryset = queryset.filter(driver_id=driver_id)

        return queryset.all()


class UserViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    queryset = models.User.objects.all()
    serializer_class = serializers.base.UserSerializer

    @action(methods=['POST'], detail=False, url_path='initial-signup')
    def validate_initial_signup(self, request):
        serializer = serializers.request.SignUpInitialValidation(
            data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = models.User.objects.create_user(serializer.validated_data.get(
            'username'), serializer.validated_data.get('password'))

        return Response({
            "message": "Sign up was successful!",
            "user": serializers.base.UserSerializer(user).data
        }, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def login(self, request):
        # pylint: disable=no-member

        serializer = serializers.request.LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data.pop('username')
        password = serializer.validated_data.pop('password')

        is_authenticated = True
        try:
            user = models.User.objects.get(username=username)

            if not user.check_password(password):
                is_authenticated = False

        except models.User.DoesNotExist:
            is_authenticated = False

        if not is_authenticated:
            return Response(
                'Username, email, or password is invalid.',
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            serializers.base.UserSerializer(user).data,
            status=status.HTTP_200_OK
        )


class ViolationViewSet(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):

    # pylint: disable=no-member

    queryset = models.Violation.objects.all()
    serializer_class = serializers.base.ViolationSerializer

    def create(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)

        if serializer.is_valid():
            description = serializer.validated_data.get('description')
            driver = serializer.validated_data.get('driver')

            is_violation = True

            for notif_type in choices.STATUS_TYPES_LIST:
                if notif_type in description:
                    is_violation = False
                    break

            models.Notification.objects.create(
                driver=driver,
                description=description,
                notification_type=choices.VIOLATION if is_violation else choices.STATUS
            )

            super().create(*args, **kwargs)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class VehicleViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    # pylint: disable=no-member

    queryset = models.Vehicle.objects
    serializer_class = serializers.base.VehicleSerializer

    def get_queryset(self):
        queryset = self.queryset

        serializer = serializers.query.VehicleQuerySerializer(
            data=self.request.query_params)

        if not serializer.is_valid():
            return queryset.all()

        driver_id = serializer.validated_data.get('driver_id', None)
        if driver_id:
            queryset = queryset.filter(driver_id=driver_id)

        return queryset.all()


class NotificationViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):

    # pylint: disable=no-member

    queryset = models.Notification.objects
    serializer_class = serializers.base.NotificationSerializer

    def get_queryset(self):
        queryset = self.queryset

        serializer = serializers.query.NotificationQuerySerializer(
            data=self.request.query_params)

        if not serializer.is_valid():
            return queryset.all()

        driver_id = serializer.validated_data.get('driver_id', None)
        if driver_id:
            queryset = queryset.filter(driver_id=driver_id)

        is_viewed = serializer.validated_data.get('is_viewed', None)
        if is_viewed:
            queryset = queryset.filter(is_viewed=is_viewed)

        notification_type = serializer.validated_data.get(
            'notification_type', None)
        if notification_type:
            queryset = queryset.filter(notification_type=notification_type)

        return queryset.all()

    @action(detail=True, url_path='viewed', methods=['POST'])
    def is_viewed_true(self, request, pk):
        try:
            notif = models.Notification.objects.get(id=pk)
            notif.is_viewed = True
            notif.save()
        except models.Notification.DoesNotExist:
            return Response({'Notification not found!'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)
