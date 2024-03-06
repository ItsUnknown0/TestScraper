
import asyncio
import pyppeteer
import json
from pyppeteer import launch
from pyppeteer import errors

# Globals
websiteRootLink = "https://www.therow.com"
SearchMax = 10
Keywords = [] # WIP
pageInfo = {}
searchedLinks = []

# Functions
async def search(link : str):
    ## Launching browser and thy page
    browser = await launch()
    page = await browser.newPage()

    try:
        await page.goto(link)
    except TimeoutError as e:
        Warning(e)
        return None
    except errors.PageError as e:
        Warning(e)
        return None
    except errors.NetworkError as e:
        Warning(e)
        return None
    
    await page.waitFor(500)
    await page.setViewport({
        'width': 800,
        'height': 800,
    })

    ## Getting Elements
    pageLinks = []

    p_html = await page.querySelectorAll('a')
    head_html = await page.querySelector('head')
    title_html = await head_html.querySelector('title')

    ## Elements
    
    for item in p_html:
       property = await item.getProperty("href")
       convertedText = await property.jsonValue()
       pageLinks.append(convertedText)

    title_property = await title_html.getProperty("textContent")
    convertedTitle = await title_property.jsonValue()
    pageInfo[link] = {
        "Name/Title" : convertedTitle
    }

    searchedLinks.append(link)

    return pageLinks


async def init():
    SearchCount = 0
    outputLinks = await search(websiteRootLink)
    newLinksToSearch = outputLinks

    def addLink(links : list):
        if links == None or links.count(None): return
        for link in links:
           newLinksToSearch.append(link)
    
    def linkCheck(links : list, sCount : int):
        if sCount >= SearchMax or link in searchedLinks or link == "javascript:void(0)":
            newLinksToSearch.remove(link)
            return True
        elif link == None:
            newLinksToSearch.remove(None)
            return True

    print("Searched the root link!")

    while SearchCount < SearchMax:
        for link in outputLinks:
            # Check if link has already been searched
            if linkCheck(link,SearchCount): break
            SearchCount += 1
            print("Searched Links: " + str(len(searchedLinks)))
            print("Searching " + link + "...")
            newLinks = await search(link)
            addLink(newLinks)


# Running the main function
InitTask = asyncio.new_event_loop()
asyncio.set_event_loop(InitTask)

InitTask.run_until_complete(init())

## Save Data
with open('Outputs/sitesInfo.json', "w") as file:
    json.dump(pageInfo, file, indent=4)