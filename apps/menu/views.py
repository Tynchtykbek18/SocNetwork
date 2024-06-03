import requests
from bs4 import BeautifulSoup
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Dish, Menu
from .serializers import MenuSerializer


class MenuDetailAPI(generics.ListAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def parsing(request):
    try:
        url = "https://beslenme.manas.edu.kg/"
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        extract_menu_data(soup)
        return Response({"status": "OK"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"status": f"ERROR {e}"}, status=status.HTTP_400_BAD_REQUEST)


def extract_menu_data(soup):
    title = soup.find("h4", class_="mbr-section-title mbr-fonts-style align-center mb-0 display-2").text.strip()
    date = soup.find("h5", class_="mbr-section-subtitle mbr-fonts-style align-center mb-0 mt-2 display-5").text.strip()

    Menu.objects.all().delete()
    menu = Menu.objects.create(title=title, date=date)

    portions = soup.find_all("div", class_="row mt-4")

    for portion in portions:
        items = portion.find_all("div", class_="item features-image сol-12 col-md-6 col-lg-3")
        for item in items:
            img_src = item.find("img")["src"]
            dish_name = item.find("strong").text.strip()
            dish_link = item.find("a")["href"]
            calorie = (
                item.find("h6", class_="item-subtitle mbr-fonts-style mt-1 display-7")
                .text.strip()
                .split(":")[1]
                .strip()
            )

            Dish.objects.create(
                menu=menu,
                dish_name=dish_name,
                img_src=img_src,
                dish_url=dish_link,
                calorie=calorie,
            )
