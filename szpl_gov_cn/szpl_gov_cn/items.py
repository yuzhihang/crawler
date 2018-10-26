# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CertItem(scrapy.Item):
    """
    许可证详情
    http://ris.szpl.gov.cn/bol/certdetail.aspx?id=
    """
    nameToField = {
        '许可证号': 'cert_no',
        '项目名称': 'name',
        '发展商': 'developer',
        '所在位置': 'position',
        '栋数': 'count_of_buildings',
        '地块编号': 'field_no',
        '房产证编号': 'house_cert_no',
        '批准面积': 'approval_area',
        '土地出让合同': 'contract',
        '批准日期': 'approval_date',
        '发证日期': 'issue_date',
        '住宅面积': 'house_area',
        '住宅套数': 'count_of_houses',
        '商业面积': 'business_area',
        '商业套数': 'count_of_business',
        '备注': 'remark',
        '用途': 'usage'
    }

    url = scrapy.Field()
    cert_no = scrapy.Field()  # 许可证号
    name = scrapy.Field()  # 项目名称
    developer = scrapy.Field()  # 发展商
    position = scrapy.Field()  # 所在位置
    count_of_buildings = scrapy.Field()  # 栋数
    field_no = scrapy.Field()  # 地块编号/宗地号
    house_cert_no = scrapy.Field()  # 房产证编号
    approval_area = scrapy.Field()  # 批准面积
    contract = scrapy.Field()  # 土地出让合同
    approval_date = scrapy.Field()  # 批准日期
    issue_date = scrapy.Field()  # 发证日期（开始销售日期）
    house_area = scrapy.Field()  # 住宅面积
    count_of_houses = scrapy.Field()  # 住宅套数
    business_area = scrapy.Field()  # 商业面积
    count_of_business = scrapy.Field()  # 商业套数
    remark = scrapy.Field()  # 备注
    usage = scrapy.Field()  # 用途


class ProjectItem(scrapy.Item):
    """
    项目详情
    http://ris.szpl.gov.cn/bol/projectdetail.aspx?id=
    """
    nameToField = {
        '项目名称': 'name',
        '卖方': 'seller',
        '宗地号': 'field_no',
        '宗地位置': 'position',
        '受让日期': 'acquire_date',
        '所在区域': 'district',
        '权属来源': 'acquire_source',
        '批准机关': 'approval_authority',
        '合同文号': 'contract',
        '使用年限': 'years_of_usage',
        '用地规划许可证': 'field_permit',
        '房屋用途': 'house_usage',
        '土地用途': 'field_usage',
        '宗地面积': 'field_area',
        '总建筑面积': 'total_building_area',
        '预售总套数': 'count_of_pre_sale_houses',
        '预售总面积': 'pre_sale_area',
        '现售总套数': 'count_of_on_sale_house',
        '现售总面积': 'count_of_on_sale_area',
        '备注': 'remark'
    }

    url = scrapy.Field()
    seller = scrapy.Field()  # 卖方信息
    name = scrapy.Field()  # 项目名称
    field_no = scrapy.Field()  # 地块编号/宗地号
    position = scrapy.Field()  # 宗地位置
    acquire_date = scrapy.Field()  # 受让日期
    district = scrapy.Field()  # 所在区域
    acquire_source = scrapy.Field()  # 权属来源
    approval_authority = scrapy.Field()  # 批准机关
    contract = scrapy.Field()  # 合同文号
    years_of_usage = scrapy.Field()  # 使用年限
    field_permit = scrapy.Field()  # 用地规划许可证
    house_usage = scrapy.Field()  # 房屋用途
    field_usage = scrapy.Field()  # 土地用途
    field_area = scrapy.Field()  # 宗地面积
    total_building_area = scrapy.Field()  # 总建筑面积
    count_of_pre_sale_houses = scrapy.Field()  # 预售总套数
    pre_sale_area = scrapy.Field()  # 预售总面积
    count_of_on_sale_house = scrapy.Field()  # 现售总套数
    count_of_on_sale_area = scrapy.Field()  # 现售总面积
    buildings = scrapy.Field()  # 楼栋列表
    remark = scrapy.Field()  # 备注


class HouseItem(scrapy.Item):
    """
    房子详情
    http://ris.szpl.gov.cn/bol/housedetail.aspx?id=

    “期房待售”， 指房屋为期房，可以销售但尚未售出。 b1_2
    现房待售 b1_1
    待售 b1
    未批准 b4
    已签现售合同 b5
    “已签认购书” 指房屋已经签订认购书，但尚未签订正式的预售或现售合同。 b10
    “已签预售合同”，指房屋为期房，已售出并签订预售合同。b3
    “已备案”， 指签订的买卖合同已在产权登记部门备案。b2
    “初始登记”，指房屋已进入初始登记的状态。b123
    “安居房”，指房屋为安居型商品房。b1_3
    “自动锁定”，指开发商未及时办理合同备案，导致售房系统自动锁定，暂时无法使用。bz1
    “管理局锁定”， 指房屋处于限制状态或开发商存在违规行为，导致售房系统被管理局锁定。bz3_n
    “委员会锁定”， 指房屋处于限制状态或开发商存在违规行为，导致售房系统被委员会锁定。bz2_n
    “市局锁定”， 指房屋处于限制状态或开发商存在违规行为，导致售房系统被委员会锁定。bz2
    “分局锁定”， 指房屋处于限制状态或开发商存在违规行为，导致售房系统被委员会锁定。bz3
    “司法查封”，指房屋被司法机关锁定。 b6_1
    已查封或抵押  b6
    系统锁死 b7
    暂缓销售 b8
    已办房地产证 b9
    设定担保 b11
    已签合同 b12
    """

    imageToStatus = {
        'b1': '待售',
        'b1_1': '现房待售',
        'b1_2': '期房待售',
        'b1_3': '安居房',
        'b2': '已备案',
        'b3': '已签预售合同',
        'b4': '未批准',
        'b5': '已签现售合同',
        'b6': '已查封或抵押',
        'b6_1': '司法查封',
        'b7': '系统锁死',
        'b8': '暂缓销售',
        'b9': '已办房地产证',
        'b10': '已签认购书',
        'b11': '设定担保',
        'b12': '已签合同',
        'b123': '初始登记',
        'bz1': '自动锁定',
        'bz2': '市局锁定',
        'bz2_n': '委员会锁定',
        'bz3': '分局锁定',
        'bz3_n': '管理局锁定'
    }

    nameToField = {
        '座号': 'unit',
        '户型': 'room_type',
        '合同号': 'contract_no',
        '备案价格': 'record_price',
        '楼层': 'floor',
        '房号': 'room_no',
        '用途': 'usage',
        '建筑面积': 'total_area',
        '户内面积': 'in_room_area',
        '分摊面积': 'common_area'
    }

    url = scrapy.Field()
    project_name = scrapy.Field()  # 项目名称
    building_name = scrapy.Field()  # 楼名
    unit = scrapy.Field()  # 座号/单元
    room_type = scrapy.Field()  # 户型
    contract_no = scrapy.Field()  # 合同号
    record_price = scrapy.Field()  # 备案价格 40746元/平方米(按建筑面积计)
    floor = scrapy.Field()  # 楼层
    room_no = scrapy.Field()  # 房号
    usage = scrapy.Field()  # 用途
    total_area = scrapy.Field()  # 建筑面积
    in_room_area = scrapy.Field()  # 户内面积
    common_area = scrapy.Field()  # 公摊面积
    sale_status = scrapy.Field()  # 销售状态：预售/现售
    status = scrapy.Field()  # 房子状态
