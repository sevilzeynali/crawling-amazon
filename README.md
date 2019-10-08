# parse-amazon-reviews-and-stars: browsing amazon to get product reviews and stars

parse-amazon-reviews-and-stars is a  python program for crawling amazon french site to get product reviews and stars . This dataset can be used to train a sentiment analyser with deep learning tools like [fasttext](https://fasttext.cc/).

## Getting asins
You need to have a file of asins of products that you want to get the reviews about. This can be found in amazon site.
For getting asins you can open [french amazon site](https://www.amazon.fr/). Then in "parcourir les catégories" you can choose one category of article. Then you can enable inspect with right click in the middle of your amazon page.
then you can open the console of the inspect.
you can type this commande line on the console:
```
for (var i=0;i<2000;i++) try{console.log (document.getElementById("result_"+i).getAttribute("data-asin"));}catch(e){}
```
then you can get all the asins for all article in one amazon page.
You can copy this in a file.
We have a file of 4 dvd asins stocked in asins_dvd_amazon for test.

## Installing and requirements
you need to install [lxml](https://lxml.de/installation.html) python library.
```
sudo apt-get install python3-lxml
```
you need to install [requests](http://docs.python-requests.org/en/master/user/install/).
```
pipenv install requests
```
## How does it work
You need only to put the paths of you files:

Here you put the asins file name
```
with open('asins_dvd_amazon') as file_of_asins:
list_of_asins = file_of_asins.read().splitlines()
```
This is the path to put the reviews. One review per line.
```
file_of_amazon_comments=open('comments_dvd_amazon','w')
```
This is the path to a file to save stars label.
```
file_of_amazon_ratings=open('stars_dvd_amazon','w')
```
Here is a file of logs to save all asins you did.
```
file_of_asins_done=open('log','w')
```

