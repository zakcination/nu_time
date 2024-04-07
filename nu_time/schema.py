import graphene 

from courses.schema import Query as CourseQuery

class Query(CourseQuery):
    pass 

schema = graphene.Schema(query = Query)