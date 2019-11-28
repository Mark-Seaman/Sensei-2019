from django.urls import path

from insight.views import InsightCreate, InsightDay, InsightDelete, InsightHome, InsightList, InsightUpdate

urlpatterns = [

    # Add View
    path('add', InsightCreate.as_view(), name='insight-add'),

    # Edit View
    path('<int:pk>/', InsightUpdate.as_view(), name='insight-update'),

    # Delete View
    path('<int:pk>/delete/', InsightDelete.as_view(), name='insight-delete'),

    # Day View
    path('<int:year>-<int:month>-<int:day>', InsightDay.as_view()),

    # List View
    path('list', InsightList.as_view(), name='insight-list'),

    # Home View
    path('', InsightHome.as_view(), name='insight-list'),
]
