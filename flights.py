import base64
from datetime import date
import webbrowser


def google_flights_url(origin, destination, departure_date, return_date):
    """Build a round-trip Google Flights results URL for three-letter IATA codes."""
    airport_prefix = bytes.fromhex("08011203")

    def make_leg(departure, arrival, travel_date):
        return (
            b"j\x07" + airport_prefix + departure.encode("ascii")
            + b"\x12\x0a" + travel_date.encode("ascii")
            + b"r\x07" + airport_prefix + arrival.encode("ascii")
        )

    outbound = make_leg(origin, destination, departure_date)
    inbound = make_leg(destination, origin, return_date)
    search = b"\x08\x1c\x10\x02\x1a" + bytes([len(outbound)]) + outbound
    search += b"\x1a" + bytes([len(inbound)]) + inbound
    search += bytes.fromhex("700182010b08ffffffffffffffffff0140014801980101")
    tfs = base64.urlsafe_b64encode(search).decode("ascii").rstrip("=")
    return f"https://www.google.com/travel/flights/search?tfs={tfs}&hl=en&curr=USD"


print("Google Flights Search")
origin = input("Departure airport code (example: DEN): ").strip().upper()
destination = input("Arrival airport code (example: JFK): ").strip().upper()
departure_date = input("Departure date (YYYY-MM-DD): ").strip()
return_date = input("Return date (YYYY-MM-DD): ").strip()

if not (origin.isalpha() and len(origin) == 3 and destination.isalpha() and len(destination) == 3):
    raise SystemExit("Airport codes must each be three letters, such as DEN or JFK.")

try:
    departure = date.fromisoformat(departure_date)
    returning = date.fromisoformat(return_date)
except ValueError:
    raise SystemExit("Use a real date in YYYY-MM-DD format, such as 2026-10-15.")

if returning < departure:
    raise SystemExit("The return date must be on or after the departure date.")

url = google_flights_url(origin, destination, departure_date, return_date)
print(
    f"\nSearching round-trip flights from {origin} to {destination} "
    f"({departure_date} to {return_date})..."
)
webbrowser.open(url)
