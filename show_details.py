import keepa
import pandas as pd

# Acess Key for the API
accesskey = ''
api = keepa.Keepa(accesskey)

# 

PriceType = [
        "AMAZON",
        "NEW",
        "USED",
        "SALES",
        "LISTPRICE",
        "COLLECTIBLE",
        "REFURBISHED",
        "NEW_FBM_SHIPPING",
        "LIGHTNING_DEAL",
        "WAREHOUSE",
        "NEW_FBA",
        "COUNT_NEW",
        "COUNT_USED",
        "COUNT_REFURBISHED",
        "COUNT_COLLECTIBLE",
        "EXTRA_INFO_UPDATES",
        "RATING",
        "COUNT_REVIEWS",
        "BUY_BOX_SHIPPING",
        "USED_NEW_SHIPPING",
        "USED_VERY_GOOD_SHIPPING",
        "USED_GOOD_SHIPPING",
        "USED_ACCEPTABLE_SHIPPING",
        "COLLECTIBLE_NEW_SHIPPING",
        "COLLECTIBLE_VERY_GOOD_SHIPPING",
        "COLLECTIBLE_GOOD_SHIPPING",
        "COLLECTIBLE_ACCEPTABLE_SHIPPING",
        "REFURBISHED_SHIPPING",
        "EBAY_NEW_SHIPPING",
        "EBAY_USED_SHIPPING",
        "TRADE_IN",
        "RENTAL"
    ]

def setupimagelinks(images):
    print("Enter the images " ,images)
    if images:
        image = ', '.join(["https://images-na.ssl-images-amazon.com/images/I/"+x for x in images.split(',')])
        return image
    else:
        return images


def getPrice(index_file):
    '''Getting the price of the product'''
    if index_file == None or index_file == '' or index_file == -1:
        return None
    else:
        return index_file/100



def GetAmazonAvailability(x):
    '''We need to see the availability

    '''
    return None
def CalculateFbaFees(fees):
    total_fees = 0
    if fees:
        for key, value in fees.items():
            if value != -1:
                total_fees += value
                
        return total_fees/100

def get_drop_percent(current_rank, average_rank):
    '''We need to get the drop percent'''
    ans  = 100 - (current_rank/average_rank) * 100
    return ans


def subcategorysalesranks(x):
    included_categories = []
    if x:
        for key, value in x.items():
            if value[-1] != -1:
                included_categories.append([key, value[-1]])
        if included_categories:
            joined_categories = '; '.join(["#{}| Top 1% | {}".format(x[1], x[0]) for x in included_categories])
    return joined_categories
  
def max_min_rank(x):
    try:
        ans = x[1]
    except:
        ans = None
    return ans
def parse_product(product):
    try:
        data = {
                'Locale':'com',
                'Image':setupimagelinks(product.get('imagesCSV')),
                'Title':product.get('title'),
                'SalesRankCurrent':product.get('stats').get('current')[PriceType.index('SALES')],
                'SalesRank90Avg':product.get('stats').get('avg90')[PriceType.index('SALES')],
                'SalesRank90daysDropPercentage':get_drop_percent(product.get('stats').get('current')[PriceType.index('SALES')],product.get('stats').get('avg90')[PriceType.index('SALES')] ),
                'SalesRankDropsLast30days':product.get('stats').get('salesRankDrops30'),
                'SalesRankDropsLast90days':product.get('stats').get('salesRankDrops90'),
                'SalesRankDropsLast180days':product.get('stats').get('salesRankDrops180'),
                "SalesRankReference" :product.get('salesRankReference'),
                # need to change
                "SalesRankSubcategory" :subcategorysalesranks(product.get('salesRanks')), # sales rank is finded but the category name is not found for now
                
                'ReviewRating':product.get('csv')[PriceType.index('RATING')][-1]/10,
                'ReviewCount':product.get('csv')[PriceType.index('COUNT_REVIEWS')][-1], # PLEASE CHECK THIS TO VERFIY THE REVIEWS
                'Asin':product.get('asin'),
                
            
            

                'AmazonCurrent':product.get('stats').get('current')[PriceType.index('AMAZON')], # need to change
                'Amazon90':product.get('stats').get('avg90')[PriceType.index('AMAZON')], # need to change
                'LastPriceChange':product.get('lastPriceChange'),# changet to dateandtime
                
                
                
            
                "NewFbaCurrent":getPrice(product.get('stats').get('current')[PriceType.index('NEW_FBA')]), # need to change
                "NewFba90":getPrice(product.get('stats').get('avg90')[PriceType.index('NEW_FBA')]),
                "AmazonDropPercent90":"", # not needed
                "AmazonLowest":max_min_rank(product.get('stats').get('min')[PriceType.index('AMAZON')]), # ne
                "AmazonHighest":max_min_rank(product.get('stats').get('max')[PriceType.index('AMAZON')]), # ne
                "AmazonOOSPercent90" : product.get('stats').get('outOfStockPercentage90')[PriceType.index('AMAZON')],
                "AmazonAvailability":GetAmazonAvailability(product['offers']), #can't bee seen on the csv file but may be needed
                "NewFbaDropPercent90":"", # ignore
                "FbaFees" : CalculateFbaFees(product.get('fbaFees')), # NE
                "NewOffersCurrent":product.get('stats').get('current')[PriceType.index('COUNT_NEW')],
                "NewOffers90":product.get('stats').get('avg90')[PriceType.index('COUNT_NEW')],
                "BuyBoxCurrent":getPrice(product['stats'].get('buyBoxPrice')),
                "BuyBox90":getPrice(product.get('stats').get('avg90')[PriceType.index('BUY_BOX_SHIPPING')]),
                "BuyBoxSeller":product['stats'].get('buyBoxSellerId'), ## we will get the seller ID but can't say which 
                "CategoriesRoot":product.get('categoryTree')[0].get('name'),
                "CategoriesSub":product.get('categoryTree')[len(product.get('categoryTree'))-1].get('name'),
                "CategoriesTree":' > '.join([x.get('name') for x in product.get('categoryTree')]),
                "ProductCodesEAN":', '.join(product.get('eanList')),
                "ProductCodesUPC":', '.join(product.get('upcList')),
                "ProductCodesPartNumber":product.get('partNumber'),
                "ParentAsin":product.get('parentAsin'),
                "Manufacturer":product.get('manufacturer'),
                "Brand":product.get("brand"),
                "Model":product.get("model"),
            }
        return data

    except Exception as e:
        print(e)
        print("Error")
        return None
    

def main(asin_list):
    products = api.query(asin_list, stats=90, offers=20, history=True, rating=True, buybox=True)
    data_list = []
    for product in products:
        print("Running the product >>>", product.get('asin'))
        data = parse_product(product)
        if data:
            data_list.append(data)
            try:
                df = pd.DataFrame(data_list)
            except Exception as e:
                print("Getting error while uploading ",e)
            df.to_csv('output_sample.csv')


if __name__ == '__main__':
    asin_list = ['B08JNDNGNL']
    main(asin_list)




# functions descripe



