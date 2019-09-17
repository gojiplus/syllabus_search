from .models import Course, Session, Assessment

__all__ = [
    'get_header',
    'get_parser',
    'Parser'
]

__headers__ = {
    Course: [
        'ID', 'Name', 'Categories', 'Year', 'Term', 'Credits',
        'Faculty', 'Instructors', 'TAs', 'No. Assess.', 'No. Sessions'
    ],
    Session: [
        'CID', 'Title', 'Type', 'Date', 'Length', 'Section',
        'Location', 'Topics', 'Teaching Strategies', 'Guest Teacher'
    ],
    Assessment: [
        'CID', 'Title', 'Type', 'Format', 'Weight', 'Cumulative', 'Due Date'
    ]
}


def get_parser(model, with_header=False):
    return Parser(model, with_header)


def get_header(model):
    return __headers__.get(model)


class Parser:
    def __init__(self, model, with_header=False):
        assert model in (Course, Session, Assessment)
        self.model = model
        self.header = None
        if with_header:
            self.header = __headers__[model]

    @property
    def parser(self):
        name = self.model.__name__.lower()
        return getattr(self.__class__, '_' + name)

    def __call__(self, data):
        iterator = (self.parser(i) for i in data)
        if self.header:
            return [self.header, *iterator]
        return list(iterator)

    @staticmethod
    def _course(obj: Course):
        tas = ', '.join(i for i in obj.tas)
        cats = ', '.join(c.name for c in obj.categories)
        instructors = ', '.join(
            '{}{}'.format(i.name, ' ({})'.format(', '.join(i.degrees)) if i.degrees else '')
            for i in obj.instructors
        )
        return [
            obj.id, obj.name, cats, obj.year, obj.term, obj.credits,
            obj.faculty, instructors, tas, obj.num_assessments, obj.num_sessions
        ]

    @staticmethod
    def _session(obj: Session):
        return [
            obj.course_id, obj.title or '', obj.type or '',
            str(obj.date or ''), obj.length or '', obj.section or '',
            obj.location or '', ', '.join(obj.topics),
            ', '.join(obj.teaching_strategies), ', '.join(obj.guest_teachers)
        ]

    @staticmethod
    def _assessment(obj: Assessment):
        return [
            obj.course_id, obj.title or '', obj.type or '', obj.format or '',
            obj.weight or '', obj.cumulative or '', str(obj.due_date or '')
        ]
