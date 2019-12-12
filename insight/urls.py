from django.urls import path

from insight.views import InsightExport, InsightImport, InsightHome, InsightList, InsightMonths, InsightUpdate

urlpatterns = [

     # Edit View
    path('<int:pk>/', InsightUpdate.as_view(), name='insight-update'),

    # List View
    path('list', InsightList.as_view(), name='insight-list'),

    # Import View
    path('import', InsightImport.as_view(), name='insight-import'),

    # List View
    path('export', InsightExport.as_view(), name='insight-export'),

    # Home View
    path('', InsightHome.as_view(), name='insight-home'),

    # Months View
    path('months', InsightMonths.as_view()),

    # Add View
    # path('add', InsightCreate.as_view(), name='insight-add'),
    # Delete View
    # path('<int:pk>/delete/', InsightDelete.as_view(), name='insight-delete'),
    # Day View
    # path('<int:year>-<int:month>-<int:day>', InsightDay.as_view()),

]
