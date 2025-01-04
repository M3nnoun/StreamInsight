import requests
import json
import time
import pandas as pd

def parser(data):
    """
    parse is function to extract the data from the json response,and return a dataframe
    """
    extracted_data = []
    for item in data['data']['popularTitles']['edges']:
        node = item.get("node", {})
        content = node.get("content", {}) or {}
        watchNowOffer = node.get("watchNowOffer", {}) or {}
        packege = watchNowOffer.get("package", {}) or {}
        extracted_data.append({
            "id": node.get("id", "N/A"),  # Default to "N/A" if key is missing or None
            "title": content.get("title", "N/A"),
            "fullPath": content.get("fullPath", "N/A"),
            "imdbScore": content.get("scoring", {}).get("imdbScore", "N/A"),
            "monetizationType": watchNowOffer.get("monetizationType", "N/A"),
            "presentationType": watchNowOffer.get("presentationType", "N/A"),
            "currency": watchNowOffer.get("currency", "N/A"),
            "retailPrice": watchNowOffer.get("retailPrice", "N/A"),
            "retailPriceValue": watchNowOffer.get("retailPriceValue", "N/A"),
            "availableTo": watchNowOffer.get("availableTo", "N/A"),
            "provider": packege.get('clearName', "N/A"),
        })
    return pd.DataFrame(extracted_data)

def getData(lastCursor=""):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    url = "https://apis.justwatch.com/graphql"
    query = {
        "operationName": "GetPopularTitles",
        "variables": {
        "first": 100,
        "platform": "WEB",
        "popularTitlesSortBy": "POPULAR",
        "sortRandomSeed": 0,
        "offset": None,
        "creditsRole": "DIRECTOR",
        "after": lastCursor,
        "popularTitlesFilter": {
        "ageCertifications": [],
        "excludeGenres": [],
        "excludeProductionCountries": [],
        "objectTypes": [],
        "productionCountries": [],
        "subgenres": [],
        "genres": [],
        "packages": [
            "aat",
            "aep",
            "aho",
            "amp",
            "atp",
            "cra",
            "cru",
            "dnp",
            "fuv",
            "hlu",
            "itu",
            "koc",
            "mxx",
            "nfx",
            "pct",
            "ply",
            "pmp",
            "ppa",
            "pst",
            "szt",
            "yot"
        ],
        "excludeIrrelevantTitles": False,
        "presentationTypes": [],
        "monetizationTypes": [],
        "searchQuery": ""
        },
        "watchNowFilter": {
        "packages": [
            "aat",
            "aep",
            "aho",
            "amp",
            "atp",
            "cra",
            "cru",
            "dnp",
            "fuv",
            "hlu",
            "itu",
            "koc",
            "mxx",
            "nfx",
            "pct",
            "ply",
            "pmp",
            "ppa",
            "pst",
            "szt",
            "yot"
        ],
        "monetizationTypes": []
        },
        "language": "en",
        "country": "US",
        "allowSponsoredRecommendations": {
        "pageType": "VIEW_POPULAR",
        "placement": "POPULAR_VIEW",
        "language": "en",
        "country": "US",
        "applicationContext": {
            "appID": "3.9.2-webapp#154bce3",
            "platform": "webapp",
            "version": "3.9.2",
            "build": "154bce3",
            "isTestBuild": False
        },
        "appId": "3.9.2-webapp#154bce3",
        "platform": "WEB",
        "supportedFormats": ["IMAGE", "VIDEO"],
        "supportedObjectTypes": [
            "MOVIE",
            "SHOW",
            "GENERIC_TITLE_LIST",
            "SHOW_SEASON"
        ],
        "alwaysReturnBidID": True,
        "testingModeForceHoldoutGroup": True,
        "testingMode": True
        }
    },
        "query": """
    query GetPopularTitles($country: Country!, $popularTitlesFilter: TitleFilter, $watchNowFilter: WatchNowOfferFilter!, $popularAfterCursor: String, $popularTitlesSortBy: PopularTitlesSorting! = POPULAR, $first: Int! = 40, $language: Language!, $platform: Platform! = WEB, $sortRandomSeed: Int! = 0, $profile: PosterProfile, $backdropProfile: BackdropProfile, $format: ImageFormat) {
    popularTitles(
        country: $country
        filter: $popularTitlesFilter
        after: $popularAfterCursor
        sortBy: $popularTitlesSortBy
        first: $first
        sortRandomSeed: $sortRandomSeed
    ) {
        totalCount
        pageInfo {
        startCursor
        endCursor
        hasPreviousPage
        hasNextPage
        __typename
        }
        edges {
        ...PopularTitleGraphql
        __typename
        }
        __typename
    }
    }

    fragment PopularTitleGraphql on PopularTitlesEdge {
    cursor
    node {
        id
        objectId
        objectType
        content(country: $country, language: $language) {
        title
        fullPath
        scoring {
            imdbScore
            __typename
        }
        posterUrl(profile: $profile, format: $format)
        ... on ShowContent {
            backdrops(profile: $backdropProfile, format: $format) {
            backdropUrl
            __typename
            }
            __typename
        }
        __typename
        }
        likelistEntry {
        createdAt
        __typename
        }
        dislikelistEntry {
        createdAt
        __typename
        }
        watchlistEntry {
        createdAt
        __typename
        }
        watchNowOffer(country: $country, platform: $platform, filter: $watchNowFilter) {
        id
        standardWebURL
        package {
            packageId
            clearName
            __typename
        }
        retailPrice(language: $language)
        retailPriceValue
        lastChangeRetailPriceValue
        currency
        presentationType
        monetizationType
        availableTo
        __typename
        }
        ... on Movie {
        seenlistEntry {
            createdAt
            __typename
        }
        __typename
        }
        ... on Show {
        seenState(country: $country) {
            seenEpisodeCount
            progress
            __typename
        }
        __typename
        }
        __typename
    }
    __typename
    }""",
    }

    response = requests.post(url, json=query,headers=headers)

    return response

json_response =getData().json()

#has next
has_next=json_response.get('data').get('popularTitles').get('pageInfo').get('hasNextPage')
##the last cursor
json_response.get('data').get('popularTitles').get('pageInfo').get('endCursor')
data_df=parser(json_response)
while(has_next):
    # time.sleep(30)
    lastCursor=json_response.get('data').get('popularTitles').get('pageInfo').get('endCursor')
    response=getData(lastCursor)
    json_response =response.json()
    parser(json_response)
    data_df = pd.concat([data_df, parser(json_response)], ignore_index=True)
    has_next=json_response.get('data').get('popularTitles').get('pageInfo').get('hasNextPage')
    print(has_next)
    print(data_df.shape)
    print("exporting currente data")
    data_df.to_csv('data3.csv',index=False)
