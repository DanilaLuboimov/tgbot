from .general_request import get_response

import re


def get_properties(city_id: str, check_in: str, check_out: str, price_min: str,
                   price_max: str, user_filter: str, city_name: str,
                   landmark_ids: str | None = None,
                   distance_min: float | None = None,
                   distance_max: float | None = None,
                   ) -> list:
    """
    Функция формирует список отелей, подходящий по заданным критериям.
    Каждый элемент списка состоит из
    (Название отеля, Полной стоимости за заданный период,
    id отеля, Фактический адрес, Расстояние от центра города,
    Количество ночей в заданном периоде)

    :param city_id: id отеля
    :type city_id: str
    :param check_in: дата въезда
    :type check_in: str
    :param check_out: дата выезда
    :type check_out: str
    :param price_min: минимальная цена за ночь
    :type price_min: str
    :param price_max: максимальная цена за ночь
    :type price_max: str
    :param user_filter: фильтр для поиска отелей через api
    :type user_filter: str
    :param city_name: название города
    :type city_name: str
    :param landmark_ids: используется для проверки, как флаг
    :type landmark_ids: [str, None]
    :param distance_min: минимальная дистанция до центра города
    :type distance_min: [float, None]
    :param distance_max: максимальная дистанция до центра города
    :type distance_max: [float, None]
    :return: list
    """
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

    hotels_json = get_response(url=url, querystring=querystring)

    hotels_list = list()
    days_spent = 1

    for i in hotels_json["data"]["body"]["searchResults"]["results"]:
        if len(i["ratePlan"]["price"]["fullyBundledPricePerStay"]) > 15:
            stop = re.search(r" ", i["ratePlan"]["price"][
                                       "fullyBundledPricePerStay"][7::])
            full_price = i["ratePlan"]["price"]["fullyBundledPricePerStay"][
                         7:7 + stop.span(0)[0]:]
            nights = re.findall(r"[\d]+", stop.string)
            if len(nights) == 2:
                days_spent = int(nights[1])
            elif len(nights) == 3:
                days_spent = int(nights[2])
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
                            full_price.replace(",", "", 1),
                            str(i["id"]),
                            i["address"]["streetAddress"],
                            city_centre,
                            days_spent
                            ])

    if landmark_ids is not None:
        for hotel in hotels_list[:]:
            distance = re.search(r"\b[\d.]+\b", hotel[4])

            if not distance_min <= float(distance[0]) <= distance_max:
                hotels_list.remove(hotel)
            elif not float(price_min) <= float(hotel[1]) / hotel[5] <= float(
                    price_max):
                hotels_list.remove(hotel)

    return hotels_list
