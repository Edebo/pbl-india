# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
import json
import re

def remove_html_tags(text):
    """Remove html tags from a string"""  
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

class PlayersSpider(Spider):
    name = 'players'
    #callowed_domains = ['pbl-india.com']
    start_urls = ['https://www.pbl-india.com/']
    team_static_url="https://www.pbl-india.com/sifeeds/badminton/static/json/"
    
    def parse(self, response):       
        teams_url = response.xpath("//div[contains(@class, 'slider-item swiper-slide')]/a/@href").extract()
        teams_url.extend(response.xpath("//div[contains(@class, 'slider-item swiper-slide')]/div/a/@href").extract())
        
        for url in teams_url:
            team_id =url.split("/")[-1].split("-")[0] #get the team_id
            team_url = self.team_static_url + str(team_id) + "_team.json"           
            yield Request(team_url,callback=self.parse_team)        

    def parse_team(self,response):
        bio =json.loads(response.text)["bio"]
        # team ={
        #     "name":bio["team_name"],
        #     "short_name":bio["team_short_name"],
        #     "venue":bio["venue_name"],
        #     "rank":bio["rank"],
        #     "description":remove_html_tags(bio["writeup"]),
        #     "owner":bio["owner_name"],            
        # }

        team={
            "name":bio["team_name"]

        }

        # for x in  bio["social_details"]["social_platform"]:
        #     team[x["name"]] = x["url"]

        squad_url= self.team_static_url + str("738_") + str(bio["team_id"]) +"_squad.json"
        yield Request(url=squad_url,callback=self.parse_squad,meta=team)

    def parse_squad(self,response):
        # team={k: response.meta[k] for k in ("name", "short_name", "venue","rank","description","owner")}
        team= response.meta["name"]
        squad =json.loads(response.text)["squads"]["squad"]
        # players=[]
        # staff=[]

        for player in squad["players"]:
           yield {               
                "full name":player["full_name"],
                "nationality":player["nationality_name"],
                "gender":player["gender"],
                "world_rank":player["world_rank"],
                "category":player["category"],
                "team":team
            }
        
        # for member in squad["staff_details"]["member"]:
        #     staff.append({
        #         "full name":member["full_name"],
        #         "role":member["role_name"],
        #         "gender":member["gender"],
        #         "nationality":member["country_name"]
        #     })
        
        # team["players"]=players
        # team["staff"]=staff

        




      


        
       
        