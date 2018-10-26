# coding=utf-8
import scrapy
import re
import logging
import logging.handlers
from ..items import *


class ProjectSpider(scrapy.Spider):
    """
    抓取二手房备案项目信息
    """
    name = 'project'

    start_urls = ['http://ris.szpl.gov.cn/bol/']  # project list
    allowed_domains = ['szpl.gov.cn']
    custom_settings = {
        'DOWNLOAD_DELAY': 0
        # 'LOG_FILE': './job/szpl.gov.cn.log'
    }

    @staticmethod
    def __get_first_text_value__(element):
        return element.css('::text').extract_first().strip() if element.css('::text').extract_first() else None

    @staticmethod
    def __get_text_values__(element):
        return element.css('::text').extract()

    @staticmethod
    def __concat_text_values__(element):
        return ''.join(ProjectSpider.__get_text_values__(element)).strip()

    def __init__(self):
        logger = logging.getLogger('project')
        logger.setLevel(logging.INFO)
        rotating_file_handler = logging.handlers.RotatingFileHandler('./job/szpl.gov.cn.log', maxBytes=10000000,
                                                                     backupCount=1)
        logger.addHandler(rotating_file_handler)

    # self.crawler.set_value('projects', 0)
    # self.crawler.set_value('houses', 0)
    # self.crawler.set_value('on_page', 0)
    # self.crawler.stats = self.crawler.stats
    #     logger = logging.getLogger('project')
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(crawler.stats)

    stats = {
        'projects': 0,
        'houses': 0,
        'on_page': 0
    }

    def parse(self, response):
        """
        self.crawler.stats.set_value('houses', 0)
        抓取项目列表页，通过列表中的项目链接抓取项目详情和许可证信息
        :param response:
        :return:
        """
        try:
            assert self.__get_first_text_value__(response.css('strong')) == '预售项目列表'

            update_time = response.css('table table font ::text')[1].extract()
            s = re.search('\d+/\d+/\d+', update_time)
            update_time = s.group() if s else None
            items_count = response.css('#AspNetPager1>div ::text')[3].extract()
            page_info = response.css('.PageInfo b::text').extract()
            current_page, _, total_pages = page_info
            number_pattern = re.compile(r'\d+')

            assert update_time is not None, '没有抓取到正确的更新时间'
            assert re.match('\d+', items_count) is not None
            assert number_pattern.match(current_page) and number_pattern.match(total_pages)
            # if int(current_page) > 1:
            #     return

        except (IndexError, AttributeError, AssertionError, TypeError, ValueError):
            self.logger.error('主页页面结构改变，请重新检查页面')

        else:
            # self.crawler.stats.inc_value('on_page')
            self.stats['on_page'] += 1
            page_tip = '============== parsing %(current_page)sth main page ==============' % {
                'current_page': current_page}
            self.logger.info(page_tip)
            print(page_tip)
            for row in response.css('#DataList1 table tr[bgcolor="#F5F9FC"]'):
                try:
                    pi = ProjectItem()
                    texts = row.css('td ::text').extract()
                    pi['seller'] = texts[3] if (len(texts) > 3) else None
                    pi['name'] = name = texts[2] if (len(texts) > 2) else None
                    project_id = texts[0] if (len(texts) > 0) else None
                    print('----project row---\n', texts)
                    self.logger.info('----project row---\n' + str(texts))

                    links = row.css('a::attr(href)').extract()

                    # yield pi

                    cert = links[0] if (len(links) > 1) else None  # 证书链接
                    details = links[1] if (len(links) > 1) else None  # 项目详情链接

                    # if cert:
                    #     yield response.follow(cert, callback=self.parse_cert,
                    #                           meta={'name': name, 'project_item': pi, 'page': current_page,
                    #                                 'project_id': project_id}, priority=100)

                    if details:
                        yield response.follow(details,
                                              callback=self.parse_project_detail,
                                              meta={'name': name, 'project_item': pi, 'page': current_page,
                                                    'project_id': project_id}, priority=80)
                except (IndexError, AttributeError, AssertionError, TypeError) as e:
                    self.logger.error('project' + pi['name'] + 'parse error' + format(e))

            next_page = response.xpath('//*[@id="AspNetPager1"]//a[contains(text(),"下一页")]/@href').extract_first()
            if next_page:
                s = re.search("doPostBack\('(\w+)\W+(\w+)", next_page)
                if s and s.lastindex >= 2:
                    __EVENTTARGET = s.group(1)
                    __EVENTARGUMENT = s.group(2)
                    yield scrapy.FormRequest.from_response(response,
                                                           formdata={'__EVENTTARGET': __EVENTTARGET,
                                                                     '__EVENTARGUMENT': __EVENTARGUMENT},
                                                           callback=self.parse, priority=20,
                                                           dont_click=True)

    def parse_cert(self, response):
        """
        抓取许可证详细信息
        :param response:
        :return:
        """
        try:
            assert response.css('.a2 ::text').extract()[0].strip() == '已经入库的预售或现售许可证'
            assert response.css('.a2 ::text').extract()[2].strip() == '许可证详细信息'

        except (IndexError, AttributeError, AssertionError):
            self.logger.error('证书页面结构改变，请重新检查页面')

        else:
            meta = response.meta
            page = meta.get('page')
            project_name = meta.get('name')
            project_id = meta.get('project_id')
            info = '============== parsing cert : %(project_id)sth project %(project_name)s at page %(page)s ==============' % {
                'page': page,
                'project_id': project_id,
                'project_name': project_name}
            self.logger.info(info)
            print(info)
            ci = CertItem()
            ci['url'] = response.url
            ci['name'] = name = meta.get('project_item')['name'] if meta.get('project_item') else None
            tds = response.xpath('//table//table//tr[position()>1]//td')
            info = 'parsing cert of %(project_id)sth project %(name)s at page %(page)s ' % {'name': name,
                                                                                            'project_id': project_id,
                                                                                            'page': page}
            print(info)
            self.logger.info(info)

            for index, td in enumerate(tds):
                try:
                    if (index & 1) == 0:
                        chinese_name = self.__get_first_text_value__(td)
                        if chinese_name:
                            key = ci.nameToField.get(chinese_name)
                            value = self.__get_first_text_value__(tds[index + 1])
                            if not key or not value or value.find('--') != -1:
                                continue
                            # self.logger.info(key + ' ' + value)
                            if key == 'usage' and value == '住宅':
                                house_area = self.__get_first_text_value__(tds[index + 3])
                                ci['house_area'] = house_area if house_area else None
                                count_of_houses = self.__get_first_text_value__(tds[index + 5])
                                ci['count_of_houses'] = count_of_houses if count_of_houses else None
                                continue

                            if key == 'usage' and value == '商业':
                                house_area = self.__get_first_text_value__(tds[index + 3])
                                ci['business_area'] = house_area if house_area else None
                                count_of_houses = self.__get_first_text_value__(tds[index + 5])
                                ci['count_of_business'] = count_of_houses if count_of_houses else None
                                continue
                            ci[key] = value
                except (KeyError, IndexError) as e:
                    self.logger.error(format(e))
            print('yield cert---------------------------------------\n', ci)
            self.logger.info('yield cert---------------------------------------\n' + str(ci))
            yield ci

    def parse_project_detail(self, response):
        """
        抓取项目详细信息
        :param response:
        :return:
        todo 项目去重判断，比如某小区一，二三期，设计相似度算法，用名字，开发商和地址来计算
        """
        try:
            assert self.__get_first_text_value__(response.css('strong')) == '项目详细资料'

        except (IndexError, AttributeError, AssertionError):
            self.logger.error('项目详情页面结构改变，请重新检查页面')

        else:
            # self.crawler.stats.inc_value('projects')
            self.stats['projects'] += 1
            meta = response.meta
            pi = ProjectItem()
            pi['url'] = response.url
            # todo 小区名净化或者模糊匹配 如 康达尔山海上园（二期）前海嘉里商务中心二期
            pi['name'] = project_name = meta['project_item']['name'] if meta.get('project_item') else ''
            pi['seller'] = meta['project_item']['seller'] if meta.get('project_item') else ''
            pi['buildings'] = []
            page = meta.get('page')
            project_id = meta.get('project_id')
            info = '============== parsing project: %(project_id)s of project ' \
                   '%(project_name)s at page %(page)s ==============' % {
                       'page': page,
                       'project_id': project_id,
                       'project_name': project_name}
            self.logger.info(info)
            print(info)

            tds = response.xpath('//table//table//tr[position()>1]//td')
            for index, td in enumerate(tds):
                try:
                    if (index & 1) == 0:
                        chinese_name = self.__concat_text_values__(td)
                        if chinese_name:

                            key = pi.nameToField.get(chinese_name)
                            value = self.__concat_text_values__(tds[index + 1])
                            if not key or not value or value.find('--') != -1:
                                continue
                            # self.logger.info(key + ' ' + value)
                            pi[key] = value

                except (KeyError, IndexError, AttributeError) as e:
                    self.logger.error('project' + pi['name'] + 'detail parsing error' + format(e))

            # 查找并follow每栋楼的链接
            for index, tr in enumerate(response.xpath('//table[@id="DataList1"]/tr[count(td)>1]')):
                try:
                    tds = tr.css('td')
                    building_name = tds[1].css('::text').extract_first()
                    pi['buildings'].append(building_name)
                    # building_link = tds[4].xpath('.//@href').extract_first()
                    # yield response.follow(building_link, callback=self.parse_buildings, priority=60,
                    #                       meta={'project_name': project_name,
                    #                             'building_name': building_name,
                    #                             'sale_status': 'pre_sale',
                    #                             'parse_other_units': True,
                    #                             'page': page,
                    #                             'project_id': project_id})

                except (IndexError, AttributeError) as e:
                    self.logger.error('buildings parsing error' + format(e))
            print('yield project---------------------------------------\n', pi)
            self.logger.info('yield project---------------------------------------\n' + str(pi))
            yield pi

    def parse_buildings(self, response):
        """
        解析并follow每个房间的链接
        :param response:
        :return:
        """

        # print(str(response.meta.get('building_name') or '') + response.url)
        # def __get_unit_name__(unit):
        #     unit_text = self.__get_first_text_value__(unit)
        #     s = re.search('\[(\w+)\]', unit_text)
        #     return s.group(1) if s else None

        units = response.css('#divShowBranch')
        meta = response.meta
        project_name = meta.get('project_name') or ''
        building_name = meta.get('building_name') or ''
        sale_status = meta.get('sale_status') or ''
        page = meta.get('page')
        project_id = meta.get('project_id')
        # address = ''.join(response.css('#curAddress ::text').extract())
        info = r'============== parsing building: %(sale_status)s %(building_name)s of %(project_id)sth' \
               r' project %(project_name)s at page %(page)s ===============' % {
                   'sale_status': sale_status,
                   'building_name': building_name,
                   'project_id': project_id,
                   'project_name': project_name,
                   'page': page
               }

        self.logger.info(info)
        print(info)

        houses = response.css('#updatepanel1 table:nth-child(3) a')
        for house in houses:
            try:
                house_link = house.xpath('.//@href').extract_first()
                if house_link:
                    house_link = house_link.strip()
                else:
                    continue

                status_image = house.xpath('.//img/@src').extract_first()
                if status_image:
                    status_image = status_image.strip()

                s = re.search('/(\w+)\.', status_image)
                if s:
                    status_image = s.group(1)

                status = HouseItem.imageToStatus.get(status_image)
                if not status:
                    self.logger.warning('status image: ' + status_image + ' not found')
            except (IndexError, AttributeError, TypeError) as e:
                self.logger.error('house parsing error' + format(e))
            else:
                yield response.follow(house_link, callback=self.parse_house, priority=70,
                                      meta={'project_name': project_name,
                                            'building_name': building_name,
                                            'sale_status': sale_status,
                                            'status': status,
                                            'page': page,
                                            'project_id': project_id
                                            })

        # parse other units
        if response.meta.get('parse_other_units'):
            for u in units.css('a'):
                try:
                    # unit_name = __get_unit_name__(u)
                    unit_link = u.css('::attr(href)').extract_first().strip()
                except (IndexError, AttributeError, TypeError) as e:
                    self.logger.error('unit parsing error' + format(e))
                else:
                    print('parse_other_units')
                    yield response.follow(unit_link, callback=self.parse_buildings,
                                          meta={'project_name': project_name,
                                                'building_name': building_name,
                                                'sale_status': sale_status,
                                                'parse_other_units': False,
                                                'page': page,
                                                'project_id': project_id
                                                })

        # 现售页面
        # todo 根据dom结构找到dopostback对应的参数
        if response.meta.get('sale_status') == 'pre_sale':
            response.meta['sale_status'] = 'on_sale'
            print('parse on sale')
            yield scrapy.FormRequest.from_response(response, callback=self.parse_buildings,
                                                   formdata={'__EVENTTARGET': 'imgBt2',
                                                             '__EVENTARGUMENT': None},
                                                   meta={'project_name': project_name,
                                                         'building_name': building_name,
                                                         'sale_status': 'on_sale',
                                                         'parse_other_units': True,
                                                         'page': page,
                                                         'project_id': project_id},
                                                   dont_click=True)

    def parse_house(self, response):
        house_count = self.stats['houses']
        # if int(house_count) > 100:
        #     return
        meta = response.meta
        project_name = meta.get('project_name') or ''
        building_name = meta.get('building_name') or ''
        sale_status = meta.get('sale_status') or ''
        status = meta.get('status') or ''
        page = meta.get('page')
        project_id = meta.get('project_id')
        # todo 楼名净化 如 琳珠华庭2栋
        hi = HouseItem()
        hi['url'] = response.url
        hi['project_name'] = project_name
        hi['building_name'] = building_name
        hi['sale_status'] = sale_status
        hi['status'] = status

        # todo 解析备案价格，抽取数字

        info = '============== parsing house: %(project_id)sth project %(project_name)s\'s %(building_name)s at page %(page)s,' \
               r'   %(status)s =============' % {
                   'project_id': project_id,
                   'project_name': project_name,
                   'building_name': building_name,
                   'page': page,
                   'status': status
               }
        self.logger.info(info)
        print(info)
        try:
            assert self.__get_first_text_value__(response.css('strong')) == '套房详细信息'
        except (IndexError, AttributeError, AssertionError):
            self.logger.error('套房页面结构改变，请重新检查页面')
        else:
            self.stats['houses'] += 1
            tds = response.xpath('//table//table//table//tr[count(td)>1]//td')
            for index, td in enumerate(tds):
                try:
                    if (index & 1) == 0:
                        chinese_name = self.__concat_text_values__(td)
                        if chinese_name:

                            key = hi.nameToField.get(chinese_name)
                            value = self.__concat_text_values__(tds[index + 1])
                            if not key or not value or value.find('--') != -1:
                                continue
                            hi[key] = value

                except (KeyError, IndexError, AttributeError) as e:
                    self.logger.error('house' + hi.get('project_name', '') + hi.get('building_name', '') +
                                      'detail parsing error' + format(e))
            print('yield house---------------------------------------\n', hi)
            self.logger.info('yield---------------------------------------\n' + str(hi))
            yield hi
