from rest_framework import mixins, viewsets, status

from backend.users import models, serializers


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

        return queryset.all()
