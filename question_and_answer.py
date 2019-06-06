#!/usr/bin/env python

shi_list = ['胍', '冶', '是']
fou_list = ['吵', '叻', '否']

data_list = [{'id': 1, 'description': '宝龙达质量管理“三不“政策是(《)。', 'answer': '不接收不合格品、不制作不合格品、不流出不合格品'},
             {'id': 2, 'description': '企业的社会责任是指企业依法经营,不生', 'answer': '否'},
             {'id': 3, 'description': '工业产品许可证制度和ISO9001质量管理', 'answer': '是'},
             {'id': 4, 'description': '纠正措施是指(“所采取的措施', 'answer': '对不合格的原因'},
             {'id': 5, 'description': '在企业中,实施质量改进的主体可以是员', 'answer': '是'},
             {'id': 6, 'description': '不合格品就是不能使用的产品。', 'answer': '否'},
             {'id': 7, 'description': 'ISO9000国际标准把产品分成了四个大', 'answer': '是'},
             {'id': 8, 'description': '合肥宝龙达信息技术有限公司成立于200', 'answer': '否'},
             {'id': 9, 'description': '确定企业的使命、愿景,制定质量战略是', 'answer': '领导作用'},
             {'id': 10, 'description': '由于管理失误、工作失职、人为原因而导', 'answer': '否'},
             {'id': 11, 'description': '教育和惩罚相结合是最有效的预防出现质', 'answer': '是'},
             {'id': 12, 'description': '影响产品质量最重要的环节是()。', 'answer': ''},
             {'id': 13, 'description': '企业质量管理中常用的检查表主要用于〔', 'answer': '数据采集'},
             {'id': 14, 'description': '未经加工、制作的天然形成的产品,如原', 'answer': '是'},
             {'id': 15, 'description': '质量方针应由组织的(制定发布。', 'answer': '最高管理者'},
             {'id': 16, 'description': '了解顾客需求和测量顾客满意度的方法,', 'answer': '是'},
             {'id': 17, 'description': '诚信是企业参与市场竞争最基本的商业道', 'answer': '是'},
             {'id': 18, 'description': '宝龙达未在2010年入选福布斯潜力榜。', 'answer': '否'},
             {'id': 19, 'description': '日本质量专家狞野认为,如果提供充分会', 'answer': '魅力特性'},
             {'id': 20, 'description': '宝龙达集团形成于2012年,涉及信息技', 'answer': '是'},
             {'id': 21, 'description': '生产现场生产速度最重要,可以适当违反', 'answer': '否'},
             {'id': 22, 'description': '我们应该有下道工序或流程就是()的', 'answer': '客户'},
             {'id': 23, 'description': '质量管理大师戴明先生在其著名的质量管', 'answer': '质量是设计和生产出来的,不是检验出来的。'},
             {'id': 24, 'description': '通常把〔)当作全面质量管理活动的“第', 'answer': '质量教育培训'},
             {'id': 25, 'description': '宝龙达质量事故按等级划分为()。', 'answer': '重大质量事故、严重质量事故、一般质量事故'},
             {'id': 26, 'description': '宝龙达最初成立的时间地点分别是?()', 'answer': '1992年、北京'},
             {'id': 27, 'description': '在我国市场上销售的进口产品,在其包装', 'answer': '否'},
             {'id': 28, 'description': '在5S管理中,对现场物品进行清理分', 'answer': '理'},
             {'id': 29, 'description': 'GB/T19001标准中,“产品“是指产品实', 'answer': '是'},
             {'id': 30, 'description': '不属于质量管理七大原则的是()。', 'answer': '现场管理'},
             {'id': 31, 'description': '宝龙达集团目前在全国分布地点为:(', 'answer': '北京、台北、深圳、合肥、武汉'},
             {'id': 32, 'description': '质量是指产品满足顾客需求。', 'answer': '否'},
             {'id': 33, 'description': '国家实行强制性质量认证的产品,未加附', 'answer': '是'},
             {'id': 34, 'description': '宝龙达质量方针是()。', 'answer': '持续追求卓越'},
             {'id': 35, 'description': '精益生产中的生产节拍是指(。', 'answer': '与顾客需求相一致的生产节卖'},
             {'id': 36, 'description': '按照卓越绩效模式,不可以对组织的管理', 'answer': '否'},
             {'id': 37, 'description': '贯彻()的原则是现代质量管理的核心', 'answer': '预防为主'},
             {'id': 38, 'description': '一家生产销售电脑的企业做出保修一年,', 'answer': '外部质量成本'},
             {'id': 39, 'description': '宝龙达质量管理者的使命是()。', 'answer': '强化全员质量意识'},
             {'id': 40, 'description': '发生严重质量事故的部门,部门和责任人', 'answer': '是'},
             {'id': 41, 'description': '对提高产品质量或杜绝质量事故做出贡献', 'answer': '否'},
             {'id': 42, 'description': '在职业健康安全管理体系中,发生了事故', 'answer': '减小因事故、事件或不符合而产生的影响'},
             {'id': 43, 'description': '2018年7月,合肥单月产量突破（ ）。', 'answer': '400k'},
             {'id': 44, 'description': '供应商绩效考核应当包括（ ）的目标。', 'answer': '质量、交付、服务'},
             {'id': 45, 'description': '精益生产中的生产节拍是指（ ）。', 'answer': '与顾客需求相一致的生产节奏'},
             {'id': 46, 'description': '宝龙达最初成立的时间地点分别是?( )', 'answer': '1992年、北京'},
             {'id': 47, 'description': '在我国市场上销售的进口产品，在其包装上可以不用中文标识标注。', 'answer': '是'},
             {'id': 48, 'description': '产品自售出之日起15日内发生性能故障,消费', 'answer': '是'}
             ]