from .views import get_one,get_first,get_particular_column,get_last,get_countrywise_sum,get_pname_capkeep
from .views import get_captain_name, get_rhand_country, get_pdob,get_age_range,insert_new,update_one,delete_one,delete_many
from django.urls import path,include 
from django.conf.urls import url
urlpatterns=[
    url(r"^getone/(?P<player_id>\d+)$",get_one),
    path('getfirst/',get_first),
    path('getpcolumn/',get_particular_column),
    path('getlast/',get_last),
    path('getcsum/',get_countrywise_sum),
    path('getpname/',get_pname_capkeep),
    path('getcname/',get_captain_name),
    path('getrhand/',get_rhand_country),
    path('pdob/',get_pdob),
    path('agerange/',get_age_range),
    path('insert/',insert_new),
    path('update/',update_one),
    path('deleteone/',delete_one),
    path('deletemany/',delete_many)
]