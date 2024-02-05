from googleapiclient.discovery import build
import googleapiclient.errors

#api_key = 'AIzaSyAD__0JEeF2NVkJMm4H9hxGe-mTPi0EGtY'
api_key = 'AIzaSyAx7z4m-Jo502ob3rcaz_UFY89L4pZVrLs'

youtube = build(
                'youtube',
                'v3',
                developerKey=api_key
                )

# Channel-IDs from 10 Youtube Channels
krishnaik = 'UCNU_lfiiWBdtULKOw6X0Dig'
Traveltarot = 'UCha3HCONXrDQrlyn5rGj71g'
Robertasgym = 'UCDUlDJcPPOOQK-3UrxEyhAQ'
fittuber = 'UCYC6Vcczj8v-Y5OgpEJTFBw'
mindbodynature = 'UClVjg4ALRonkQsMbb4I3S0g'
mysticmusing = 'UCr5Dl7bcUkbMJyK-6J6pZhQ'
techTFQ = 'UCnz-ZXXER4jOvuED5trXfEA'
gobimathan = 'UCQYl7XDlq30WJaUO6H77pOQ'
TheCyberZeel = 'UCKjFQcRLQcwfGWbFKQljouA'
eMasterClassAcademy = 'UCtfTf1nNJQ4PbUDqj-Q48rw'

channel_list = [krishnaik, Traveltarot, Robertasgym, fittuber, mindbodynature,
                mysticmusing, techTFQ, gobimathan, TheCyberZeel, eMasterClassAcademy]