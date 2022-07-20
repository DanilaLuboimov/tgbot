from .general_request import get_response

import re


def get_properties(city_id: str, check_in: str, check_out: str, price_min: str,
                   price_max: str, user_filter: str, city_name: str,
                   landmark_ids: str | None = None,
                   distance_min: float | None = None,
                   distance_max: float | None = None,
                   ) -> tuple:
    url = "https://hotels4.p.rapidapi.com/properties/list"
    querystring = {
        "destinationId": city_id,
        "pageNumber": "1",
        "pageSize": "25",
        "checkIn": check_in,
        "checkOut": check_out,
        "adults1": "1",
        "priceMin": price_min,
        "priceMax": price_max,
        "sortOrder": user_filter,
        "locale": "en_US",
        "currency": "USD",
        "accommodationIds": "12,1"
    }

    # if landmark_ids is not None:
    #     querystring["landmarkIds"] = landmark_ids

    hotels_json = get_response(url=url, querystring=querystring)
    print(hotels_json["data"]["body"]["searchResults"]["results"])
    hotels_list = list()
    days_spent = 1

    for i in hotels_json["data"]["body"]["searchResults"]["results"]:
        if len(i["ratePlan"]["price"]["fullyBundledPricePerStay"]) > 15:
            stop = re.search(r" ", i["ratePlan"]["price"][
                                       "fullyBundledPricePerStay"][7::])
            full_price = i["ratePlan"]["price"]["fullyBundledPricePerStay"][
                         7:7 + stop.span(0)[0]:]
            nights = re.search(r"[\d]+", stop.string)
            days_spent = int(nights[0])
        else:
            full_price = i["ratePlan"]["price"]["fullyBundledPricePerStay"][
                         7::]

        city_centre = re.search(r"City Centre", city_name)
        if city_centre is None:
            city_centre = \
                f'До центра города: ' \
                f'{round(float(i["landmarks"][0]["distance"][:-6:]) / 0.621, 2)} км'
        else:
            city_centre = "Отель находится в центральном районе города"

        hotels_list.append([i["name"],
                            full_price,
                            str(i["id"]),
                            i["address"]["streetAddress"],
                            city_centre,
                            ])

    print(hotels_list)
    if landmark_ids is not None:
        for hotel in hotels_list[:]:
            distance = re.search(r"\b[\d.]+\b", hotel[4])

            if not distance_min <= float(distance[0]) <= distance_max:
                hotels_list.remove(hotel)

            if float(price_min) <= float(hotel[1]) / days_spent <= float(
                    price_max):
                hotels_list.remove(hotel)

    return hotels_list, days_spent
