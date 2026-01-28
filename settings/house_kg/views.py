from rest_framework import viewsets, status, views
from .permissions import IsSellerForProperty, IsBuyerForReview
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filter import PropertyFilter, UserFilterSet
from rest_framework.filters import OrderingFilter, SearchFilter
import joblib
from django.conf import settings
import os

class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

class LoginView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

class LogoutView(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['username', 'status']
    filterset_class = UserFilterSet

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_class = [IsSellerForProperty, IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['title', 'description']
    filterset_class = PropertyFilter

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsBuyerForReview, IsAuthenticated]

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]

class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticated]

model_path = os.path.join(settings.BASE_DIR, 'model (1).pkl')
model = joblib.load(model_path)

scaler_path = os.path.join(settings.BASE_DIR, 'scaler (1).pkl')
scaler = joblib.load(scaler_path)

neighborhoods = [
    'Blueste', 'BrDale', 'BrkSide', 'ClearCr', 'CollgCr', 'Crawfor',
    'Edwards', 'Gilbert', 'IDOTRR', 'MeadowV', 'Mitchel', 'NAmes',
    'NPkVill', 'NWAmes', 'NoRidge', 'NridgHt', 'OldTown', 'SWISU',
    'Sawyer', 'SawyerW', 'Somerst', 'StoneBr', 'Timber', 'Veenker'
]

class PricePredict(views.APIView):

    def post(self, request):
        serializer = PricePredictSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            new_neighborhood = data.pop('Neighborhood')
            neighborhood1or_0 = [1 if new_neighborhood == i else 0 for i in neighborhoods]

            features = list(data.values()) + neighborhood1or_0
            scaled_data = scaler.transform([features])
            predict = model.predict(scaled_data)[0]

            return Response({'predict': predict}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)