import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
from io import StringIO

# Main scraping function ( Loop )
def scrapeAllAmazonProducts(url, header):

    response = requests.get(url, headers = header)

    if response.status_code == 200:
        # this variable will have the HTML content of the Amazon page
        soup = BeautifulSoup(response.content, 'html.parser')

        # this is the parent div of all the products divs
        parent = soup.find('div', class_='p13n-gridRow _cDEzb_grid-row_3Cywl')

        if parent : 
            
            product_divs = parent.find_all('div', recursive = False)

            products_list = []

            # finding all the links of all the products divs
            for product_div in product_divs:

              # getting the link from each div
              product_link = product_div.find('a', class_='a-link-normal')['href']

              # The absolute URL
              absolute_link = f"https://www.amazon.com{product_link}"

              # scraping data from the product page and returning the product
              product = scrapeProductPage(absolute_link)

              # adding the product to the list
              products_list.append(product)       

              # creating the csv file
              CSVFile(products_list,0)

        else :
            print("Can't reach the parent component because of Amazon's confideniality problem")      

    else:
        print(f"Failed to download the main page. Status code: {response.status_code}")


# One page scraping function
def scrapeProductPage(url, header):

    response = requests.get(url, headers = header)

    # i didn't make the response == 200 check because of 404 error, so i'm working without it 

    # this variable will have the HTML content of the Amazon page
    soup = BeautifulSoup(response.content, "html.parser")

    # fields classes name
    spaneName = "a-size-large product-title-word-break"
    spaneBrand = "a-size-base a-text-bold"
    spaneRating = "a-size-base a-color-base"
    spaneReviews = "a-size-base"
    spanePrice = "a-price a-text-price a-size-medium apexPriceToPay"
    spaneDiscription = "a-unordered-list a-vertical a-spacing-mini"
    
    # extracting each field
    name = soup.find('span',  {'class': spaneName, 'id': 'productTitle'}).text.strip()
    rating = soup.find('span',  {'class': spaneRating}).text.strip()
    price = soup.find('span',  {'class': spanePrice}).text.strip()
    reviews = soup.find('span',  {'class': spaneReviews, 'id': 'acrCustomerReviewText'}).text.strip()
    description = soup.find('span',  {'class': spaneDiscription}).text.strip()
    brand = soup.find('span',  {'class': spaneBrand}).text.strip()

    # returing product 
    product = {
        'Rank': index + 1,
        'Name': name,
        'Brand': brand,
        'Price': price,
        'Rating': rating,
        'Reviews': reviews,
        'Description': description,
    }

    return product 


# DataFrame to csv function 
def CSVFile(data, test):

    if(test == 0):
        # creating a DataFrame from the list of product details
        dataf = pd.DataFrame(data)
        dataf.to_csv(r'C:\Users\Admin\Desktop\AmazonWebScrapingTest.csv', index=False)
    else :
        # means this is for testing and not for the amazon's web-site
        buffer = StringIO(data)
        reader = csv.reader(buffer, skipinitialspace=True)
        with open('test.csv', 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(reader)


# this function here is just for you to see that the amazon url don't allow me to scrape data from it, but the other sites is okay like this one
def scrapeExemple(url, header):

    response = requests.get(url, headers = header)

    # print(response.content)

    if response.status_code == 200:

        # this variable will have the HTML content of the Amazon page
        soup = BeautifulSoup(response.content, 'html.parser')

        # print(soup.prettify().encode('utf-8'))


        # this is the parent div of all the products divs
        site_title = soup.find('span', class_='mw-page-title-main').text

        print(site_title)

        # creating the csv file
        CSVFile(site_title,1)



if __name__ == "__main__":

    # Here are the url's for all owr categories, + the headers ( just for this testing )

    BROWSER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
    custom_headers = {'user-agent': BROWSER_AGENT,'accept-language': 'en-GB,en;q=0.9'}

    URL_THAT_DONT_NEED_PERMISSION_TO_ACCESS_ITS_DATA = "https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue"
    Electronics_url = 'https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics'
    Clothes_Sho_Jewel_url = 'https://www.amazon.com/Best-Sellers-Clothing,-Shoes-Jewelry/zgbs/fashion'
    Home_Kitch_url = 'https://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden'
    Health_Pers_Care_url = 'https://www.amazon.com/Best-Sellers-Health,-Fitness-Dieting/zgbs/books/10'
    
  

    print("Exemple scraping !")
    scrapeExemple(URL_THAT_DONT_NEED_PERMISSION_TO_ACCESS_ITS_DATA, custom_headers)


    print("Top 100 Best-Selling Electronics:")
    # scrapeAllAmazonProducts(Electronics_url, custom_headers)

    print("\nTop 100 Best-Selling Clothes, Shoes and Jewelries:")
    # scrapeAllAmazonProducts(Clothes_Sho_Jewel_url, custom_headers)

    print("\nTop 100 Best-Selling Home and Kitchen stuff:")
    # scrapeAllAmazonProducts(Home_Kitch_url, custom_headers)

    print("\nTop 100 Best-Selling Health and Personal Care stuff:")
    # scrapeAllAmazonProducts(Health_Pers_Care_url, custom_headers)