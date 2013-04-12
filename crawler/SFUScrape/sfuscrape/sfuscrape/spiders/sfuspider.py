from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from sfuscrape.items import *


urls = [
        "https://portal.cs.sfu.ca/outlines/",
        "https://portal.cs.sfu.ca/outlines/1131/",
        "https://portal.cs.sfu.ca/outlines/1127/",
        "https://portal.cs.sfu.ca/outlines/1124/",
        "https://portal.cs.sfu.ca/outlines/1121/",
        "https://portal.cs.sfu.ca/outlines/1117/",
        "https://portal.cs.sfu.ca/outlines/1114/",
        "https://portal.cs.sfu.ca/outlines/1111/",
        "https://portal.cs.sfu.ca/outlines/1107/",
        "https://portal.cs.sfu.ca/outlines/1104/",
        "https://portal.cs.sfu.ca/outlines/1101/",
        "https://portal.cs.sfu.ca/outlines/1097/",
        "https://portal.cs.sfu.ca/outlines/1094/",
        "https://portal.cs.sfu.ca/outlines/1091/",
        "https://portal.cs.sfu.ca/outlines/1087/",
        "https://portal.cs.sfu.ca/outlines/1084/",
        "https://portal.cs.sfu.ca/outlines/1081/",
        "https://portal.cs.sfu.ca/outlines/1077/",
        "https://portal.cs.sfu.ca/outlines/1074/",
        "https://portal.cs.sfu.ca/outlines/1071/",
        "https://portal.cs.sfu.ca/outlines/1067/",
        "https://portal.cs.sfu.ca/outlines/1064/",
        "https://portal.cs.sfu.ca/outlines/1061/",
        "https://portal.cs.sfu.ca/outlines/1057/",
        "https://portal.cs.sfu.ca/outlines/1054/",
        "https://portal.cs.sfu.ca/outlines/1051/",
        "https://portal.cs.sfu.ca/outlines/1047/"
    ]


class ProfSpider(BaseSpider):
    name = "profspider"
    allowed_domains = ["cs.sfu.ca"]
    start_urls = urls

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        rows = hxs.select('//tr[@id="highlight_row"]')
        items = set()
        profs = []
        for row in rows:
            tds = row.select('td')
            professor = tds[5].select('text()').extract()[0].strip().split(' ')
            items.add((professor[0], professor[1],))

        for item in items:
            p = ProfScrape()
            p['first_name'] = item[0]
            p['last_name'] = item[1]
            profs.append(p)
        return profs


class CourseSpider(ProfSpider):
    name = "coursespider"

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        rows = hxs.select('//tr[@id="highlight_row"]')
        items = set()
        courses = []
        for row in rows:
            tds = row.select('td')
            courseprefix = tds[0].select('text()').extract()[0].strip()
            coursenumber = tds[1].select('text()').extract()[0].strip()
            course = courseprefix + coursenumber
            coursedesc = tds[3].select('text()').extract()[0].strip()
            items.add((course, coursedesc))

        for item in items:
            course = CourseScrape()
            course['course_name'] = item[0]
            course['course_desc'] = item[1]
            courses.append(course)
        return courses
