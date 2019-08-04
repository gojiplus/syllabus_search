from abc import abstractmethod
from flask_restful import Api, Resource, request
from . import app, db, Course, Session, Assessment

__all__ = ['api', 'Sessions', 'Assessments', 'Outcomes']

api = Api(app)


class _Base(Resource):
    model = None
    header = None

    @abstractmethod
    def parse_object(self, obj):
        """Method for parsing single data row"""

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
        assert self.model
        res = self.query(course_id, request.args.get('keyword'))
        if self.header:
            res = self.header + res
        return {'data': res}, 200


class Sessions(_Base):
    model = Session

    def parse_object(self, obj: Session):
        return [
            obj.title or '', obj.type or '', str(obj.date or ''), obj.length or '',
            obj.section or '', obj.location or '', ', '.join(obj.topics),
            ', '.join(obj.teaching_strategies), ', '.join(obj.guest_teachers)
        ]


class Assessments(_Base):
    model = Assessment

    def parse_object(self, obj: Assessment):
        return [
            obj.title or '', obj.type or '', obj.format or '',
            obj.weight or '', obj.cumulative or '', str(obj.due_date or '')
        ]


class Outcomes(_Base):
    model = Course

    def parse_object(self, obj: Course):
        return obj.outcomes

    def query(self, course_id, keyword=None):
        res = super(Outcomes, self).query(course_id)
        if res and res[0]:
            return [[outcome] for outcome in res[0]]
        return []
