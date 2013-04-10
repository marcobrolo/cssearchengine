# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class TutorialItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class DmozItem(Item):
    title = Field()
    link = Field()
    desc = Field()

class RateMyProfItem(Item):
    prof_name = Field()
    prof_link = Field()

class ProfItem(Item):
    last_name = Field()
    first_name = Field()
    quality = Field()
    course_name = Field()
    course_code = Field()
    helpfulness = Field()
    clarity = Field()
    easiness = Field()
    comments = Field()