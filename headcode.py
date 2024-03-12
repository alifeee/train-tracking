"""Find train(s) from headcode
"""

import sys
import re
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://live.rail-record.co.uk/headcode/?d=2024-03-12&a=&headcode="
HEADCODE = "2S80"

re_showing = re.compile(r"Showing (\d+) services")


@dataclass
class Train:
    """Train"""

    headcode: str
    departure_time: str
    from_location: str
    to_location: str
    href: str

    def __str__(self):
        return (
            f"{self.headcode} {self.departure_time}"
            f"{self.from_location} {self.to_location} {self.href}"
        )

    def __repr__(self):
        return (
            f"Train(headcode={self.headcode}, departure_time={self.departure_time},"
            f"from_location={self.from_location}, to_location={self.to_location}, href={self.href})"
        )


def main(headcode: str = HEADCODE):
    """main"""
    request_url = f"{BASE_URL}{HEADCODE}"
    response = requests.get(request_url, timeout=10)

    if response.status_code == 200:
        response_html = response.text
    else:
        print(f"Error: {response.status_code}")
        sys.exit(1)

    soup = BeautifulSoup(response_html, "html.parser")

    # FIND NUMBER OF RESULTS
    # find .heading-container > p
    number_found = soup.select_one(".heading-container > p")
    if not number_found:
        print("Could not find result number")
        sys.exit(1)
    number_text = number_found.get_text()
    match = re_showing.search(number_text)
    if not match:
        print("Could not find result number")
        sys.exit(1)
    result_number = int(match.group(1))
    print(f"Found {result_number} results")

    # FIND RESULTS
    # find .service-results
    results = soup.select_one(".service-results")
    if not results:
        print("Results not found")
        sys.exit(1)

    # find .service-results > .service-link
    all_results = results.select(".service-link")
    if not all_results:
        print("Result not found")
        sys.exit(1)

    for i, result in enumerate(all_results):
        href = result.get("href")
        print()
        print(f"Result {i+1}: {href}")

        # FIND DEPARTURE TIME
        # find .timing-card-times > p:nth-child(2)
        departure_time = result.select_one(".timing-card-times > p:nth-child(2)")
        if departure_time:
            print(f"Departure time: {departure_time.get_text()}")
        else:
            print("Departure time not found")

        # FIND FROM/TO
        # find (both) .timing-card-locations > p
        locations = result.select(".timing-card-locations > p")
        if locations:
            from_location = locations[0].get_text()
            to_location = locations[1].get_text()
            print(f"From: {from_location}")
            print(f"To: {to_location}")
        else:
            print("From/To not found")

        # FIND OPERATOR
        # find .operator
        operator = result.select_one(".operator > p")
        if operator:
            print(f"Operator: {operator.get_text()}")
        else:
            print("Operator not found")

        train = Train(
            headcode=HEADCODE,
            departure_time=departure_time.get_text(),
            from_location=from_location,
            to_location=to_location,
            href=href,
        )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
