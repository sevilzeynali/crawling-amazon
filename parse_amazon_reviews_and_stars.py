#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
start_time_doing_corpus = time.time()
from lxml import html 
import requests
import json
import unicodedata
from lxml import etree


#browse the list of asins
with open('asins_dvd_amazon') as file_of_asins:
    list_of_asins = file_of_asins.read().splitlines()
#open a file to write the comments of articles 
file_of_amazon_comments=open('comments_dvd_amazon','w')

#open a file to write the stars for each comment
file_of_amazon_ratings=open('stars_dvd_amazon','w')

#log file to save all asins do by the program
file_of_asins_done=open('log','w')

#begin to do the queries for each asin on amazon
dict_asins_page_number={}

for asin in list_of_asins: 
    list_pages=[]
    page_response = requests.get('https://www.amazon.fr/product-reviews/'+ asin)
    parser = html.fromstring(page_response.content)
    reviews_html = parser.xpath('//div[@class="a-section review"]')
    for review in reviews_html:
        next_page=review.xpath('//*[@id="cm_cr-pagination_bar"]/ul/li/a/text()')
        for i in next_page:
            if i!="Suivant" and i!="→" and i not in list_pages:
                list_pages.append(i)
    if len(list_pages)!=0:
        dict_asins_page_number[asin]=int(list_pages[-1])
    else:
        dict_asins_page_number[asin]=1
for asin,page_number in dict_asins_page_number.items():
    for page in range(1,dict_asins_page_number[asin]+1):
        print("I am doing "+asin+" "+str(page))    
        page_response = requests.get('https://www.amazon.fr/product-reviews/'+ asin+'/ref=cm_cr_getr_d_paging_btm_2?pageNumber='+str(page))
        parser = html.fromstring(page_response.content)
        reviews_html = parser.xpath("//div[@class='a-section review aok-relative']")
        print(reviews_html)       
    #     for review in reviews_html:
    #         commentaire=review.xpath('.//div[@data-hook="review-collapsed"]//text()')
    #         print(commentaire)
#             comment=review.xpath('.//span[@data-hook="review-body"]/text()')
#             print(comment)
#             star=review.xpath('.//a[@class="a-link-normal"]/@title')            
#             file_of_amazon_comments.write(''.join(comment).rstrip())
#             file_of_amazon_comments.write('\n')
#             for rate in star:
#                 rate=bytes(rate,encoding='utf-8')
#                 rate=rate.decode("utf-8")
#             if rate=="1,0 sur 5\xa0étoiles":
#                 file_of_amazon_ratings.write("__label__NEG"+"\n")
#             if rate=="2,0 sur 5\xa0étoiles":
#                 file_of_amazon_ratings.write("__label__NEG"+"\n") 
#             if rate=="3,0 sur 5\xa0étoiles":
#                 file_of_amazon_ratings.write("__label__NEUT"+"\n")
#             if rate=="4,0 sur 5\xa0étoiles":
#                 file_of_amazon_ratings.write("__label__POS"+"\n")
#             if rate=="5,0 sur 5\xa0étoiles":
#                 file_of_amazon_ratings.write("__label__POS"+"\n") 
#             if rate=="":
#                 file_of_amazon_ratings.write("__label__NON"+"\n")         
#     file_of_asins_done.write(asin+"\n")      

# interval_corpus_creation= time.time() - start_time_doing_corpus
# print(interval_corpus_creation)

# //*[@id="customer_review-R3B67N8YWKSZ0A"]/div[4]/span/span/text()
# //*[@id="customer_review-R1UC8JG42R46JL"]/div[4]/span/span/text()
