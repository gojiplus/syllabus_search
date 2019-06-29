from abc import abstractmethod
from flask_restful import Api, Resource
from . import app, db, Course, Session, Assessment

__all__ = ['api', 'Sessions', 'Assessments', 'Outcomes']

api = Api(app)


class _Base(Resource):
    model = None
    header = None

    @abstractmethod
    def parse_object(self, obj):
        """Method for parsing single data row"""

    def query(self, **kwargs):
        return [
            self.parse_object(obj)
            for obj in db.query(self.model).filter_by(**kwargs).all()
        ]

    def get(self, course_id):
        assert self.model
        res = self.query(course_id=course_id)
        if res:
            if self.header:
                res = self.header + res
            return res, 200
        return [], 200


class Sessions(_Base):
    model = Session
    header = ['Title', 'Type', 'Date', 'Length', 'Section', 'Location',
              'Topics', 'Teaching Strategies', 'Guest Teacher']

    def parse_object(self, obj: Session):
        return [
            obj.title or '', obj.type or '', str(obj.date or ''), obj.length or '',
            obj.section or '', obj.location or '', ', '.join(obj.topics),
            ', '.join(obj.teaching_strategies), ', '.join(obj.guest_teachers)
        ]


class Assessments(_Base):
    model = Assessment
    header = ['Title', 'Type', 'Format', 'Weight', 'Cumulative', 'Due Date']

    def parse_object(self, obj: Assessment):
        return [
            obj.title or '', obj.type or '', obj.format or '',
            obj.weight or '', obj.cumulative or '', str(obj.due_date or '')
        ]


class Outcomes(_Base):
    model = Course

    def parse_object(self, obj: Course):
        return obj.outcomes

    def query(self, **kwargs):
        id_ = kwargs.get('course_id')
        res = super(Outcomes, self).query(id=id_)
        if res and res[0]:
            return ['Course Outcomes', *res[0]]
        return []
