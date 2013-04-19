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

class Prof(Item):
    last_name = Field()
    first_name = Field()
    helpfulness = Field()
    clarity = Field()
    easiness = Field()
    course_rating = Field()

class ProfComments(Item):
    comment = Field()
    prof_first_name = Field()
    prof_last_name = Field()

class ProfLink(Item):
    first_name = Field()
    last_name = Field()
    profile_page = Field()
    home_page = Field()
    