import numpy as np
import matplotlib.pyplot as plt
from craigslist_scraper import scraper
from skimage import io
import sqlite3

def images(data):
    """
    Return the list of image urls from a craigslist object.
    """
    thumbs = data.soup.find(id='thumbs')
    return [a.attrs['href'] for a in thumbs.contents]


def expected_price(new_price, miles, expected_miles=140_000):
    """
    Return the expected price based on the new price and number of miles driven so far.

    This also works with np.Array types
    """
    return (expected_miles - miles) / expected_miles * new_price


def scrape_craigslist(url: str):
    """
    Get important craigslist information
    
    Returns: [miles, price, [image_urls]]
    """
    cl = scraper.scrape_url(url)
    miles = int(cl.attrs['odometer'])
    price = cl.price
    urls = images(cl)

    # fix price for when cents don't get accounted for properly
    if price > 100_000:
        price = price / 100
        
    # likely miles is in thousands, fix
    if miles < 1_000 and price < 10_000:
        miles = miles * 1000

    return [miles, price, urls]


def plot_price_info(m, p_real, estimated_price, estimated_miles):
    """
    Plot the price information. The graph, current milage and cost, and the potential savings.
    """
    # fair price
    miles = np.linspace(0, estimated_miles)
    price_curve = expected_price(estimated_price, miles, estimated_miles)
    p_hat = expected_price(estimated_price, m, estimated_miles)
            
    # plot prices
    fig, axs = plt.subplots(1,3, figsize=(10,2))
    fig.dpi = 120
    
    axs[0].plot(miles, price_curve)
    axs[0].scatter(m, p_hat, label='fair cost', c='orange')
    axs[0].scatter(m, p_real, label='real cost', c='red')
    
    axs[0].set_title('Cost of car')
    axs[0].set_xlabel('Milage')
    axs[0].set_ylabel('Price')
    axs[0].grid()
    axs[0].legend()
    
    for i in range(1,3):
        axs[i].axis('off')
    
    axs[1].text(0.5, 0.5, f"{m} miles\n@\n${p_real}", size=18, ha='center', va='center')
    
    if p_real > p_hat:
        added_cost = int(p_real - p_hat)
        axs[2].text(0.5, 0.5, f"${added_cost} added", size=18, ha='center', va='center')
    else:
        savings = int(p_hat - p_real)
        axs[2].text(0.5, 0.5, f"${savings} saved", size=18, ha='center', va='center')


def image_gallery(urls, max_imgs=4):
    """
    Show off the images from craigslist.
    """
    n = min(len(urls), max_imgs)
    fig, axs = plt.subplots(1,n)
    fig.dpi = 350
    for i in range(n):
        axs[i].axis('off')
        axs[i].imshow(io.imread(urls[i]))
    

def describe(url: str, estimated_price=25_000, estimated_miles=140_000, label='Subaru Forester'):
    """
    Show off the car!
    """
    m, p_real, img_urls = scrape_craigslist(url)
    plot_price_info(m, p_real, estimated_price, estimated_miles)
    image_gallery(img_urls)