"""Find train(s) from headcode
"""

import sys
import re
from dataclasses import dataclass
from typing import List, Optional
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://live.rail-record.co.uk/headcode/?d=2024-03-12&a=&headcode="
HEADCODE = "2S80"

re_showing = re.compile(r"Showing (\d+) services")

HEADCODE_FIRST_NUMBER_MEANINGS = {
    "1": "Indicates an express train with limited stops, with exceptions (test trains, 1Z99 rescue trains)",
    "2": "Indicates a slow train with frequent stops, with exceptions (2Z02 Caroline and 2Qxx test trains)",
    "3": "Test trains (followed by a Q), priority ECS and railhead conditioning trains",
    "4": "Fast freight usually 75mph max",
    "5": "Empty coaching stock moves",
    "6": "General freight with a max speed of 60mph",
    "7": "Slower freight with a max speed of 45mph",
    "8": "Severely limited trains and rail head conditioning trains",
    "9": "Services that are subject to special operating requirements on certain parts of the network",
}


@dataclass
class Train:
    """Train"""

    headcode: str
    departure_time: Optional[str] = None
    from_location: Optional[str] = None
    to_location: Optional[str] = None
    operator: Optional[str] = None
    href: Optional[str] = None

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

    def pprint(self):
        """pretty print"""
        print(
            f"""headcode: {self.headcode}
departure_time: {self.departure_time}
from_location: {self.from_location}
to_location: {self.to_location}
operator: {self.operator}
headcode meaning: {HEADCODE_FIRST_NUMBER_MEANINGS.get(self.headcode[0], "Unknown")}
href: {self.href}"""
        )


def get_trains(headcode) -> List[Train]:
    """Get trains for a headcode

    Args:
        headcode (str): Headcode

    Raises:
        requests.exceptions.RequestException: Request exception

    Returns:
        List[Train]: List of trains
    """
    request_url = f"{BASE_URL}{headcode}"
    response = requests.get(request_url, timeout=10)

    if response.status_code == 200:
        response_html = response.text
    else:
        raise requests.exceptions.RequestException(f"Error: {response.status_code}")

    soup = BeautifulSoup(response_html, "html.parser")

    # FIND RESULTS
    # find .service-results
    results = soup.select_one(".service-results")
    if not results:
        raise ValueError("Results not found")

    # find .service-results > .service-link
    all_results = results.select(".service-link")
    if not all_results:
        raise ValueError("Result not found")

    trains = []
    for result in all_results:
        train = Train(
            headcode=HEADCODE,
        )

        href = result.get("href")
        if href:
            train.href = href

        # FIND DEPARTURE TIME
        # find .timing-card-times > p:nth-child(2)
        departure_time = result.select_one(".timing-card-times > p:nth-child(2)")
        if departure_time:
            train.departure_time = departure_time.get_text()

        # FIND FROM/TO
        # find (both) .timing-card-locations > p
        locations = result.select(".timing-card-locations > p")
        if locations:
            from_location = locations[0].get_text()
            to_location = locations[1].get_text()
            train.from_location = from_location
            train.to_location = to_location

        # FIND OPERATOR
        # find .operator
        operator = result.select_one(".operator > p")
        if operator:
            train.operator = operator.get_text()

        trains.append(train)

    return trains


def main(headcode: str = HEADCODE):
    """main"""
    trains = get_trains(headcode)
    for train in trains:
        print()
        train.pprint()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
