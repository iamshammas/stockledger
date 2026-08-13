from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from common.permissions import IsSuperAdminOrSeller
from reports.serializers import CurrentStockReportSerializer, DailyPurchaseReportSerializer, DailySalesReportSerializer, LowStockReportSerializer, MonthlySalesReportSerializer, ProductPurchaseReportSerializer, RetailerDuesReportSerializer, StockValuationReportSerializer
from .services import ReportService

from django.utils import timezone
from django.utils.dateparse import parse_date


class CurrentStockAPIView(GenericAPIView):
    serializer_class = CurrentStockReportSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]

    def get(self, request):
        queryset = ReportService.get_current_stock_report(request.user.tenant)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class StockValuationAPIView(GenericAPIView):
    serializer_class = StockValuationReportSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]

    def get(self, request):
        queryset = ReportService.get_stock_valuation_report(request.user.tenant)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class DailySalesAPIView(GenericAPIView):
    serializer_class = DailySalesReportSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]

    def get(self, request):
        date_str = request.query_params.get('date')
        date = parse_date(date_str) 
        if not date:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=400)
        
        report_data = ReportService.get_daily_sales_report(request.user.tenant, date)
        report_data['date'] = date  
        serializer = self.get_serializer(report_data)
        return Response(serializer.data)

class MonthlySalesAPIView(GenericAPIView):
    serializer_class = MonthlySalesReportSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]

    def get(self, request):
        year = request.query_params.get('year')
        if not year or not year.isdigit() or len(year) != 4:
            return Response({"error": "Invalid year format. Use YYYY"}, status=400)
        
        report_data = ReportService.get_monthly_sales_report(request.user.tenant, int(year))
        serializer = self.get_serializer(report_data, many=True)
        return Response(serializer.data)

class RetailerDuesAPIView(GenericAPIView):
    serializer_class = RetailerDuesReportSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]

    def get(self, request):
        report_data = ReportService.get_retailer_dues_report(request.user.tenant)
        serializer = self.get_serializer(report_data, many=True)
        return Response(serializer.data)

class PurchaseHistoryAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]
     
    def get_serializer_class(self):
        group_by = self.request.query_params.get('group_by', 'product')
        if group_by == 'date':
            return DailyPurchaseReportSerializer  
        return ProductPurchaseReportSerializer  

    def get(self, request):
        group_by = request.query_params.get('group_by', 'product')  # Default to grouping by product
        start_date = request.query_params.get('start_date')
        start_date = parse_date(start_date) if start_date else None
        end_date = request.query_params.get('end_date')

        # Validate dates
        if group_by == "date":
            if not start_date:
                return Response({"error": "start_date is required in the format YYYY-MM-DD."}, status=400)
            if not end_date:
                end_date = timezone.now().date()  # Default to today if end_date is not provided
            if start_date > end_date:
                return Response({"error": "End date cannot be before start date"}, status=400)
            
            report_data = ReportService.get_daily_purchase_report(request.user.tenant, start_date, end_date)
            
        else:
            report_data = ReportService.get_product_purchase_report(request.user.tenant)

        serializer = self.get_serializer(report_data, many=True)    
        return Response(serializer.data)

class LowStockAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdminOrSeller]

    def get(self, request):
        queryset = ReportService.get_low_stock_report(request.user.tenant)
        serializer = LowStockReportSerializer(queryset, many=True)
        return Response(serializer.data)