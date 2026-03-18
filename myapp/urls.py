from django.urls import path
from myapp import views

urlpatterns = [

    path('',views.home),
    path('login_get/',views.login_get),
    path('login_post/',views.login_post),
    path('logout/', views.logout_view),


    # =========================================================
    # adminmodule
    path('adminhome/',views.adminindex),
    path('addauthority_get/',views.addauthority_get),
    path('addauthority_post/',views.addauthority_post),
    path('viewauthority/',views.viewauthority),
    path('editauthority_get/<id>',views.editauthority_get),
    path('editauthority_post/',views.editauthority_post),
    path('deleteauthority/<id>',views.deleteauthority),
    path('addbus_get/',views.addbus_get),
    path('addbus_post/',views.addbus_post),
    path('viewbus/',views.viewbus),
    path('editbus_get/<id>',views.editbus_get),
    path('editbus_post/',views.editbus_post),
    path('deletebus/<id>',views.deletebus),
    path('addroute_get/',views.addroute_get),
    path('addroute_post/',views.addroute_post),
    path('viewroute/',views.viewroute),
    path('editroute_get/<id>',views.editroute_get),
    path('editroute_post/',views.editroute_post),
    path('deleteroute/<id>',views.deleteroute),
    path('addstop_get/',views.addstop_get),
    path('addstop_post/',views.addstop_post),
    path('viewstop/',views.viewstop),
    path('editstop_get/<id>',views.editstop_get),
    path('editstop_post/',views.editstop_post),
    path('deletestop/<id>',views.deletestop),
    path('assignroute_get/',views.assignroute_get),
    path('assignroute_post/',views.assignroute_post),
    path('viewassignroute/',views.view_assignroute),
    path('addplace_get/',views.addplace_get),
    path('addplace_post/',views.addplace_post),
    path('viewplace/',views.viewplace),
    path('editplace_get/<id>',views.editplace_get),
    path('editplace_post/',views.editplace_post),
    path('deleteplace/<id>',views.deleteplace),


    # ========================================================

    path('userregister/',views.registeruser_post,name='userregister'),
    path('user_login/',views.user_login),
    path('viewbus_user/',views.viewbus_user),
    path('viewroute_user/',views.view_route_user),
    path('viewstop_user/',views.view_stop_user),
    path('viewplace_user/',views.view_place_user),
    path("send_complaint/", views.send_complaint),
    path('viewreply/<str:lid>/', views.view_complaints, name='view_complaints'),
    path('authority_complaints/',views.authority_complaints,name='authority_complaints'),
    path('authority_send_reply/',views.authority_send_reply,name='authority_send_reply'),
    path("predict_risk/",views.predict_risk_view),
    path('send_alert/',views.send_alert),
    path('forgot_password/',views.forgot_password),
    path('view_alerts/', views.view_alerts),
]
