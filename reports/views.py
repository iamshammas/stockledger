from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from reports.serializers import CurrentStockSerializer
from .services import ReportService


class CurrentStockAPIView(GenericAPIView):
    serializer_class = CurrentStockSerializer

    def get(self, request):
        queryset = ReportService.get_current_stock_report(request.user.tenant)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)