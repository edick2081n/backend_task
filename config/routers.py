from rest_framework.routers import DefaultRouter
from pictures import views

router = DefaultRouter()
router.register('images', views.FigureViewSet)
#router.register('resize/', views.FigureChangeViewSet)

