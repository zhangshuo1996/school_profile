from web.utils import db


def get_recommended_unites_by_industry_codes(category, industry_codes):
    """根据行业代码推荐高校， 目前仅仅支持中类的行业，否则会获取不到数据"""
    sql = """
    select unit_id,school.name, industry_code, patent_count from unit_industry
    join school on school.id=unit_id
    where category=:category and industry_code in (%s)
    """
    words = ['"%s"' % code for code in industry_codes]
    sql = sql % ",".join(words)
    results = db.select(sql, params={'category': category}, bind='data_mining')
    # 按照industry_code排序
    results = sorted(results, key=lambda x: x['industry_code'])
    return results


def get_institutions_by_industry_codes(industry_codes, patent_count):
    """通过行业代码和专利数量限制获取学校对应的学院"""
    sql = """
    select school_id, institution_name from institution_industry
    where industry_code in (%s)
    GROUP BY school_id, institution_name HAVING sum(patent_count) > :patent_count
    ORDER BY school_id,sum(patent_count) desc
    """
    words = ['"%s"' % code for code in industry_codes]
    sql = sql % ",".join(words)
    results = db.select(sql, params={'patent_count': patent_count}, bind='data_mining')
    # 转化为 {school_id: []}
    mapping = {}
    for result in results:
        school_id, institution = result['school_id'], result['institution_name']
        if school_id not in mapping:
            mapping[school_id] = []
        mapping[school_id].append(institution)
    return mapping
