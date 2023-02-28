
class PAgeCount:
    def __init__(self, pagecount):
     self.pagecount = pagecount

    def __repr__(self):
        return 'PageCount(page_count=%s)' % self.pagecount


    @classmethod
    def get_paginated_search(cls,page,limit,value) -> "PAgeCount":
         return cls.query.filter(cls.title.like((f'%{value}%')) | cls.body.like(f'%{value}%') | cls.created_at.like(f'%{value}%') | cls.updated_at.like(f'%{value}%')).paginate(page, per_page=limit).pages