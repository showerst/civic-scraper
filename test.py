from civic_scraper.platforms import CivicPlusSite, LegistarSite, GranicusSite, PrimeGovSite
from civic_scraper.base.cache import Cache
import logging

logging.basicConfig(level="DEBUG")

url = "https://santafe.primegov.com/portal/search"
site = PrimeGovSite(url)
assets_metadata = site.scrape()

assets_metadata.to_os('/home/showerst/work/showerst-github/civic-scraper/assets')
# for asset in assets_metadata:
#     print(asset)
#     asset.download('./assets')
