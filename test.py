import requests

url = "https://apis.justwatch.com/graphql"
query = {
    "operationName": "GetPopularTitles",
    "variables": {
    "first": 100,
    "platform": "WEB",
    "popularTitlesSortBy": "POPULAR",
    "sortRandomSeed": 0,
    "offset": "null",
    "creditsRole": "DIRECTOR",
    "after": "",
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
      "testingModeForceHoldoutGroup": False,
      "testingMode": False
    }
  },
    "query": """
 query GetPopularTitles(
  $allowSponsoredRecommendations: SponsoredRecommendationsInput
  $backdropProfile: BackdropProfile
  $country: Country!
  $first: Int!
  $format: ImageFormat
  $language: Language!
  $platform: Platform!
  $after: String
  $popularTitlesFilter: TitleFilter
  $popularTitlesSortBy: PopularTitlesSorting!
  $profile: PosterProfile
  $sortRandomSeed: Int
  $watchNowFilter: WatchNowOfferFilter!
  $offset: Int
  $creditsRole: CreditRole!
) {
  popularTitles(
    allowSponsoredRecommendations: $allowSponsoredRecommendations
    country: $country
    filter: $popularTitlesFilter
    first: $first
    sortBy: $popularTitlesSortBy
    sortRandomSeed: $sortRandomSeed
    offset: $offset
    after: $after
  ) {
    __typename
    edges {
      cursor
      node {
        ...PopularTitleGraphql
        __typename
      }
      __typename
    }
    pageInfo {
      startCursor
      endCursor
      hasPreviousPage
      hasNextPage
      __typename
    }
    sponsoredAd {
      ...SponsoredAd
      __typename
    }
    totalCount
  }
}

fragment PopularTitleGraphql on MovieOrShow {
  __typename
  id
  objectId
  objectType
  content(country: $country, language: $language) {
    title
    fullPath
    scoring {
      imdbVotes
      imdbScore
      tmdbPopularity
      tmdbScore
      tomatoMeter
      certifiedFresh
      jwRating
      __typename
    }
    interactions {
      votesNumber
      __typename
    }
    dailymotionClips: clips(providers: [DAILYMOTION]) {
      sourceUrl
      externalId
      provider
      __typename
    }
    posterUrl(profile: $profile, format: $format)
    backdrops(profile: $backdropProfile, format: $format) {
      backdropUrl
      __typename
    }
    isReleased
    credits(role: $creditsRole) {
      name
      personId
      __typename
    }
    runtime
    genres {
      translation(language: $language)
      shortName
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
  watchlistEntryV2 {
    createdAt
    __typename
  }
  customlistEntries {
    createdAt
    __typename
  }
  freeOffersCount: offerCount(
    country: $country
    platform: $platform
    filter: { monetizationTypes: [FREE, ADS] }
  )
  watchNowOffer(country: $country, platform: $platform, filter: $watchNowFilter) {
    ...WatchNowOffer
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
    tvShowTrackingEntry {
      createdAt
      __typename
    }
    seenState(country: $country) {
      seenEpisodeCount
      progress
      __typename
    }
    __typename
  }
}

fragment WatchNowOffer on Offer {
  id
  standardWebURL
  streamUrl
  package {
    id
    icon
    packageId
    clearName
    shortName
    technicalName
    iconWide
    hasRectangularIcon(country: $country, platform: $platform)
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

fragment SponsoredAd on SponsoredRecommendationAd {
  bidId
  holdoutGroup
  campaign {
    name
    backgroundImages {
      imageURL
      size
      __typename
    }
    countdownTimer
    creativeType
    disclaimerText
    externalTrackers {
      type
      data
      __typename
    }
    hideDetailPageButton
    hideImdbScore
    hideJwScore
    hideRatings
    hideContent
    posterOverride
    promotionalImageUrl
    promotionalVideo {
      url
      __typename
    }
    promotionalTitle
    promotionalText
    promotionalProviderLogo
    promotionalProviderWideLogo
    watchNowLabel
    watchNowOffer {
      ...WatchNowOffer
      __typename
    }
    node {
      ... on MovieOrShowOrSeason {
        content(country: $country, language: $language) {
          fullPath
          posterUrl
          title
          scoring {
            imdbScore
            jwRating
            __typename
          }
          genres {
            shortName
            translation(language: $language)
            __typename
          }
          backdrops(format: $format, profile: $backdropProfile) {
            backdropUrl
            __typename
          }
          isReleased
          __typename
        }
        objectId
        objectType
        __typename
      }
      ... on MovieOrShow {
        watchlistEntryV2 {
          createdAt
          __typename
        }
        __typename
      }
    }
    __typename
  }
  __typename
}

 """,
}

response = requests.post(url, json=query)
print(response.text)
