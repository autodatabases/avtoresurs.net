from django.db import models
from tecdoc.apps import TecdocConfig as tdsettings

# SET @TYP_ID = 3822; /* ALFA ROMEO 145 (930) 1.4 i.e. [1994/07-1996/12] */
# SET @STR_ID = 10630; /* Поршень в сборе; Можете использовать NULL для вывода ВСЕХ запчастей к автомобилю */
#
# SELECT	LA_ART_ID
# FROM LINK_GA_STR
# INNER JOIN LINK_LA_TYP ON LAT_TYP_ID = @TYP_ID AND	LAT_GA_ID = LGS_GA_ID
# INNER JOIN LINK_ART ON LA_ID = LAT_LA_ID
# WHERE LGS_STR_ID <=> @STR_ID
# ORDER BY LA_ART_ID
# LIMIT	100;

