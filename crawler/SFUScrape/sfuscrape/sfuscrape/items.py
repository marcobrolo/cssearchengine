from scrapy.item import Item, Field


class ProfScrape(Item):
    last_name = Field()
    first_name = Field()


class CourseScrape(Item):
    course_name = Field()
    course_desc = Field()
