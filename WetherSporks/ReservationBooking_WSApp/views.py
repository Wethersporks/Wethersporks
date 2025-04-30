from django.shortcuts import render

# Create your views here.

def index(request):
    """ Home-Page """
    
    if "time" in request.GET:
        time_selected = request.GET["time"]
        quantity = request.GET["guestCount"]
        date = request.GET["date"]

        print(f"Time Picked: {time_selected} for {quantity} people on {date}")


    elif "date" in request.GET:
        date_selected = request.GET["date"]
        return render(request, "ReservationBooking/Index.html", {"date_selected":date_selected})



    return render(request, "ReservationBooking/Index.html")