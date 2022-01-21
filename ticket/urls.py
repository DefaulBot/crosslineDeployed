from django.urls import path
from ticket import views
urlpatterns =[
    path('purchase/', views.purchaseTicket,name="purchase-ticket"),
    path('purchase/QR/cancel/',views.cancelTicket),
    path('purchase/getlocations/',views.getLocation,name="getlocations"),
    path('purchase/makeTicketPurchase/', views.makeTicketPurchase,name="make-ticket-purchase"),
    path('purchase/QR/', views.generateQR,name="generate-ticket-QR"),
    path('Scan/', views.scan_ticket,name="scan-user-ticket"),
    path('purchase/QR/is_ticketChanged/', views.is_ticketChanged,name="is-ticket-changed"),
    path('history/', views.ticketHistory,name="ticket-history"),
]
