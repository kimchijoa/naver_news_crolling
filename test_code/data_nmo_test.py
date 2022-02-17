import time
import sys
from datetime import date, datetime
sys.path.append("/naver_news_crolling/func/")
import data_normalization_run as nmo
test_date = "2022-02-15"

result = nmo.nmo_run(test_date)

#print(result[0])
print(result[1])