from flask_restful import Api, Resource, request
from .parser import get_parser
from .utils import search
from . import app, Course, Session, Assessment

__all__ = ['api', 'Sessions', 'Assessments', 'Outcomes']

api = Api(app)


class _Base(Resource):
    model = None
    parser = None

    def get(self, course_id):
        assert self.model is not None
        assert self.parser is not None
        keyword = request.args.get('keyword')
        found = search(self.model, course_id=course_id, keyword=keyword) or []
        return {'data': self.__class__.parser(found)}, 200


class Sessions(_Base):
    model = Session
    parser = get_parser(model)


class Assessments(_Base):
    model = Assessment
    parser = get_parser(model)


class Outcomes(_Base):
    model = Course

    @staticmethod
    def parser(data):
        return [
            [course.id, outcome]
            for course in data
            for outcome in course.outcomes
        ] if data else []
