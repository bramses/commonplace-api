from sqlalchemy import text, bindparam
from sqlalchemy.sql import and_, or_
from pydantic import BaseModel

class Filter(BaseModel):
    published: bool = False
    from_date: str = None
    to_date: str = None
    source_types: list = None
    tags: list = None
    transformations: list = None

    def to_sql(self):
        conditions = []
        params = {}
        if self.published is not None:
            conditions.append(text("published = :published"))
            params['published'] = int(self.published)
        if self.from_date is not None:
            conditions.append(text("date >= :from_date"))
            params['from_date'] = self.from_date
        if self.to_date is not None:
            conditions.append(text("date <= :to_date"))
            params['to_date'] = self.to_date
        if self.source_types is not None:
            conditions.append(or_(*[text("source_types = :source_type" + str(i)) for i in range(len(self.source_types))]))
            params.update({'source_type' + str(i): source_type for i, source_type in enumerate(self.source_types)})
        if self.tags is not None:
            conditions.append(or_(*[text("tags = :tag" + str(i)) for i in range(len(self.tags))]))
            params.update({'tag' + str(i): tag for i, tag in enumerate(self.tags)})
        if self.transformations is not None:
            conditions.append(or_(*[text("transformations = :transformation" + str(i)) for i in range(len(self.transformations))]))
            params.update({'transformation' + str(i): transformation for i, transformation in enumerate(self.transformations)})

        return and_(*conditions), params
    

'''
where_clause, params = filter.to_sql()
result = connection.execute(select([my_table]).where(where_clause), **params)
'''