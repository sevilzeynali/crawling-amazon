#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
start_time_doing_corpus = time.time()
from lxml import html 
import requests

#opening the list of asins file and putting them in a list
with open('asins_dvd_amazon') as file_of_asins:
    list_of_asins = file_of_asins.read().splitlines()

#open a file to write the comments of articles 
file_of_amazon_comments=open('comments_dvd_amazon','w')

#open a file to write the stars for each comment
file_of_amazon_ratings=open('stars_dvd_amazon','w')

#log file to save all asins do by the program
file_of_asins_done=open('log','w')

#begin to do the queries for each asin on amazon
#in this dictionary we stock the asins as keys and the number of pages of comments for each asins as value  
dict_asins_page_number={}

for asin in list_of_asins: 
    list_pages=[]
    page_response = requests.get('https://www.amazon.fr/product-reviews/'+ asin)
    parser = html.fromstring(page_response.content)
    #getting reviews
    reviews_html = parser.xpath('//div[@class="a-section review"]')#attention this path can be change when amazon change the site html 
    for review in reviews_html:
        #getting the number of pages for each asin
        next_page=review.xpath('//*[@id="cm_cr-pagination_bar"]/ul/li/a/text()')#attention this path can be change when amazon change the site html 
        for i in next_page:
            if i!="Suivant" and i!="→" and i not in list_pages:
                list_pages.append(i)
    if len(list_pages)!=0:
        dict_asins_page_number[asin]=int(list_pages[-1])#the last element of the list_page is the number of page per asin
    else:
        dict_asins_page_number[asin]=1

for asin,page_number in dict_asins_page_number.items():
    for page in range(1,dict_asins_page_number[asin]+1):
        print("I am doing "+asin+" "+str(page))    
        page_response = requests.get('https://www.amazon.fr/product-reviews/'+ asin+'/ref=dpx_acr_txt?showViewpoints='+str(page))#attention this path can be change when amazon change the site html 
        parser = html.fromstring(page_response.content)
        reviews_html = parser.xpath('//div[@class="a-section review aok-relative"]')#attention this path can be change when amazon change the site html      
        for review in reviews_html:
            comment=review.xpath('.//span[@data-hook="review-body"]/span/text()')#attention this path can be change when amazon change the site html 
            star=review.xpath('.//a[@class="a-link-normal"]/@title')#attention this path can be change when amazon change the site html             
            file_of_amazon_comments.write(''.join(comment).rstrip())#writting the comments in a file
            file_of_amazon_comments.write('\n')
            for rate in star:
                rate=bytes(rate,encoding='utf-8')
                rate=rate.decode("utf-8")
            #writting stars as labels in a file
            if rate=="1,0 sur 5\xa0étoiles":
                file_of_amazon_ratings.write("__label__NEG"+"\n")#if one star label is negative
            if rate=="2,0 sur 5\xa0étoiles":
                file_of_amazon_ratings.write("__label__NEG"+"\n")#if 2 stars label is negative
            if rate=="3,0 sur 5\xa0étoiles":
                file_of_amazon_ratings.write("__label__NEUT"+"\n")#if 3 stars label is neutral
            if rate=="4,0 sur 5\xa0étoiles":
                file_of_amazon_ratings.write("__label__POS"+"\n")#if 4 stars label is positive
            if rate=="5,0 sur 5\xa0étoiles":
                file_of_amazon_ratings.write("__label__POS"+"\n")#if 5 stars label is positive 
            if rate=="":
                file_of_amazon_ratings.write("__label__NON"+"\n")#if 0 star label is NON        
    
    file_of_asins_done.write(asin+"\n")#we write the asins that we treated in our log      

interval_corpus_creation= time.time() - start_time_doing_corpus
print(interval_corpus_creation)
