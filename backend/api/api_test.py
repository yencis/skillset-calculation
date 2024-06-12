from dotenv import load_dotenv
import os
import requests
import util_io
import osu_api

oapi = osu_api.OSUAPI()

#print(oapi.get_user_score(10852203, "best", 1).json())
print(oapi.edit_post(9454329))
