from django.conf import settings
from app_products.models import *
from app_orders.models import *
from .views import *
import wkhtmltopdf
import pdfkit
import requests


def email_invoice():
    print('Hello Ben')
   
    url = "https://api.xero.com/api.xro/2.0/Invoices/e606ec24-3bbc-462b-a0ec-bcf7f9bfa1fa/Email"

    payload = {}
    headers = {
            'xero-tenant-id': 'e6005186-b2c1-4345-b8bf-9ff515a4dacc',
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjFDQUY4RTY2NzcyRDZEQzAyOEQ2NzI2RkQwMjYxNTgxNTcwRUZDMTkiLCJ0eXAiOiJKV1QiLCJ4NXQiOiJISy1PWm5jdGJjQW8xbkp2MENZVmdWY09fQmsifQ.eyJuYmYiOjE1OTg3MzQyNzgsImV4cCI6MTU5ODczNjA3OCwiaXNzIjoiaHR0cHM6Ly9pZGVudGl0eS54ZXJvLmNvbSIsImF1ZCI6Imh0dHBzOi8vaWRlbnRpdHkueGVyby5jb20vcmVzb3VyY2VzIiwiY2xpZW50X2lkIjoiN0I0QzRDNTU4QUU5NEVGM0JEMTkwRUJBRUMyMkE2QjMiLCJzdWIiOiJjNmJlYmYxYzFmOTY1ZGIwYTYyOTBhMjdkN2NkMzFiMyIsImF1dGhfdGltZSI6MTU5ODczMzk5MSwieGVyb191c2VyaWQiOiJhMzk0MWRiNC1lMWU4LTQxMmEtYTkwYi04ZTQ3MmQ2YTFlNjEiLCJnbG9iYWxfc2Vzc2lvbl9pZCI6ImMwZWJhNTZmNGIyMjRlZWJiYjVjMDRjYTQ0NDIyYjA3IiwianRpIjoiZGE2YjVjZWQ1MGJmMzk1MWY5NDFkOGZjYTA4MmYwOGYiLCJhdXRoZW50aWNhdGlvbl9ldmVudF9pZCI6IjhkZGVhMTRlLTA3ZjEtNDFiYS1iNmI0LTI0MDFlMzBjNjRlMiIsInNjb3BlIjpbImVtYWlsIiwicHJvZmlsZSIsIm9wZW5pZCIsImFjY291bnRpbmcudHJhbnNhY3Rpb25zIiwib2ZmbGluZV9hY2Nlc3MiXX0.UOXL3UTY7ypkwXCeFQa6CNSh_8tumPogAjVwqZkxKRqbYtTGeq4YA7SQnxlJsr_kxhxg3zqoRpT5cLfvDX_mAOXzNmZ5CdeMupgaQaiu25M2sBa9ySThy-nJZUx6d7Zm51nBvtRqOqU7YuSm2fcUcZiWVDuzpriI5HjP5ROPT7j_NkXgiu_6XFIrrcufDF6EPPlByK2Il1WfbKJDRsHBLDMjeucQ7em6e_e6dTyeGTCHG2ADBy9haE_tQAkBjkAmff_18_8Wyuq-YFOB9_nn_t7mHTNbG9WTWzeTiS9iD8xcQ4-Wz71N1cNnvxYsndsYNRMpJ3_vAE8leWEnbhHD3Q',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Cookie': 'bm_sz=7F288EAAAD09F84D3841FD8414382E71~YAAQTknRF8WNWTp0AQAANUvQOwhGQpaMz6NGKKqBuv+WeyyFbjZHuXqFjkyBmMsfgU5IQ14q5xW8hl5T2I/y5JxLzuvYT/aoTUM2Hy5hLe+9w7toxMaqs5m8/zgdeGtqCO3hAdMeT1+m0ocr/o79G9nHh3fC8IjdLQPLGNBzc81ZDiGaHwP91BJHyQ5C0Q==; _gcl_au=1.1.1669380412.1598732262; _gid=GA1.2.750418739.1598732263; _fbp=fb.1.1598732262787.1585175304; _ga_Q622B96ZEQ=GS1.1.1598732262.1.1.1598732285.0; _ga=GA1.2.882852387.1590261025; ak_bmsc=6BD992E39DAB52CD34E449B6A0152D4917D1494E584B00004CB44A5F0ECEF905~plD3KrmUpKgFfKBB0qikW2JtgyKWoxe+AAVrZvkpy1sPb2+PZKm5f9JMALdK7dbbgZf34tuE6m6YXEK9nbNipzwNCtmvfH1ocp3xG7vUv3ynbhXf2cZWoG41+kijMHUyAxY22m2xscxAGVNlF7awxY9S6d8F7tN/DKTGkuwc5/1rnqoTchy8aCkHncpgx8/lJAGcEfT/GZuSyFT7lv49kOEHwoeK+uQh3jToJg89U8ALGTfngobAPveM6+RZihe3a4Kg8xCHJ6DkJBm0wZIFTRfg==; _abck=EF4B1F408F2FAD71ECF37CAA41A8E7EB~-1~YAAQB0nRFxF7+9pzAQAAKr74OwQmZptyRHoCuesW78bb8l98EwzKCC3MN4cplVPHgrYPw8/qgUEL25mBo8RsbMpgonLdhrRb0eCU02eJ3V4YoRs2Lnu4lZbw/M1o1firJrtSB8eT4A8PiT9OgLYYrituvmGTferH9XoVAEDZsOpn5pm2VJYLuUwkb6zQv98Gjfa4DOw7LGkXXYo0isfbOvrATVkAgkssVpoqeGb2RZPb7DDHI7pgDwyGsu76D8qoZ+p3APgvj5Zhlf9YuJd+EVE+D2+UJtCO/Tv2KfQUQdW73AUauOZQKUEm9XkQDcs/aaZ6UxSh~-1~-1~-1; bm_sv=B8E0B1AE78964211587DB0AB1E9BF31A~S3CTh5365Prv0uu7SCHjX4cgEL4IB0gIBDm4A6BASMizf5MquEIa94StHyVltVaSsbl39qANhokoN4/px3wMP8Aftskz2mfr48sVOa1KxgXsEl+eNIkggQyWk1d+nHXm+4genWf4NeKWaKJFoF+Dh/53DEtCTrhLQnnljO9P2jk=; RT="z=1&dm=xero.com&si=9k40hyk7a37&ss=keg3xoql&sl=4&tt=0&obo=4&ld=10bc9&r=b5ac6cc51297fa9d9e0f832d5c9ff623&ul=10cs8&hd=10csa"'
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    print(response.text.encode('utf8'))
