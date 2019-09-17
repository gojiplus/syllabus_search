from flask_restful import Api, Resource, request
from . import app, db
from .parser import get_parser
from .models import Course, Session, Assessment

__all__ = ['api', 'Sessions', 'Assessments', 'Outcomes']

api = Api(app)


class _Base(Resource):
    model = None
    parser = None

    def query(self, course_id, keyword=None):
        stmt = ()
        if self.model is Course:
            stmt += (self.model.id == course_id,)
        else:
            stmt += (self.model.course_id == course_id,)
        if keyword:
            stmt += (self.model.document.match(keyword),)
        return [
            self.parse_object(obj)
            for obj in db.query(self.model).filter(*stmt).all()
        ]

    def get(self, course_id):
        assert self.model is not None
        assert self.parser is not None
        res = self.query(course_id, request.args.get('keyword'))
        return {'data': self.parser(res)}, 200


class Sessions(_Base):
    model = Session
    parser = get_parser(model)


class Assessments(_Base):
    model = Assessment
    parser = get_parser(model)


class Outcomes(_Base):
    model = Course
    parser = lambda res: [[i] for i in res[0]] if res and res[0] else []
