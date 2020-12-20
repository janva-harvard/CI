from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Flight, Passenger
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404
# Create your views here.


def index(req):
    return render(req, "flights/index.html", {
        "flights": Flight.objects.all()
    })


def flight(req, flight_id):
    try:
        flight = Flight.objects.get(id=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight not found.")
    return render(req, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    })


def book(request, flight_id):
    if request.method == "POST":
        try:
            passenger = Passenger.objects.get(
                pk=int(request.POST["passenger"]))
            flight = Flight.objects.get(pk=flight_id)
        except KeyError:
            return HttpResponseBadRequest("Bad Request: no flight chosen")
        except Flight.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: flight does not exist")
        except Passenger.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: passenger does not exist")
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flights:flight", args=(flight_id,)))
