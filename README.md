测试：

主页
scrapy parse --spider=project -c parse 'http://ris.szpl.gov.cn/bol/' -d 3
------------
项目
远洋新天地水岸花园 多栋楼
scrapy parse --spider=project -c parse_project_detail  'http://ris.szpl.gov.cn/bol/projectdetail.aspx?id=35472' -d 3
多单元
scrapy parse --spider=project -c parse_project_detail 'http://ris.szpl.gov.cn/bol/projectdetail.aspx?id=35692' -d 5

中海鹿丹名苑（A区） 楼多房少
scrapy parse --spider=project -c parse_project_detail 'http://ris.szpl.gov.cn/bol/projectdetail.aspx?id=34333'

琳珠华庭 113套房
scrapy parse --spider=project -c parse_project_detail 'http://ris.szpl.gov.cn/bol/projectdetail.aspx?id=34252'

万科蛇口公馆 房少
scrapy parse --spider=project -c parse_project_detail 'http://ris.szpl.gov.cn/bol/projectdetail.aspx?id=34212' -d 10
-----------



销售许可证
scrapy parse --spider=project -c parse_cert -d 2'http://ris.szpl.gov.cn/bol/certdetail.aspx?id=35692'

------------
楼栋
多个unit
scrapy parse --spider=project -c parse_buildings 'http://ris.szpl.gov.cn/bol/building.aspx?id=32123&presellid=35692'
单个unit
scrapy parse --spider=project -c parse_buildings 'http://ris.szpl.gov.cn/bol/building.aspx?id=31964&presellid=35252'
------

房子

scrapy parse --spider=project -c parse_house 'http://ris.szpl.gov.cn/bol/housedetail.aspx?id=1587290'

--------
运行
scrapy crawl <project name>