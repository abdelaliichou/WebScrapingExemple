I encountered an obstacle while attempting to scrape data from the Amazon website. Despite implementing the necessary code,
the site's security measures restricted access to the data. Despite this setback, I ensured the implementation of code that
would have worked efficiently if the site had allowed data extraction. Additionally, I have included a test function labeled
<scrapeExample> to demonstrate the functionality of the method using alternative URLs, excluding Amazon.

# CODE EXPLAINATION : 

When the main is running, it will call the <scrapeAllAmazonProducts> function passing the url, and the header to it.

The <scrapeAllAmazonProducts> function will firstly get the response from the url using http request, after that it will use the 
soup library to find the parent div that holds all the children divs, where each one of those children is a div of a product.

After that, we gonna loop through all thos children, and get the link of that specific product, concatenate it with the amazon 
site and passing this new url to the <scrapeProductPage> function which will do the same as the previous function, but instead it 
will get only the name, price, brand, reviews, description, rating from on single product page. after that it will return a product 
OBJECT which will be added by the first function to the <products_list> list.

Finally we are calling the <CSVFile> function passing to it the <products_list> so it creats a DataFrame then a CSV file containing
all the products we got from the amazon url.

# Note : 
You will find the <scrapeExample> function , it's just for test and for showing you that the principle is working well with the principal
functions, there's only the permission problem from amazon's url .
