#!/usr/bin/env python3

import re, os, csv, sys
import pickle, datetime, time
from tempfile import mkstemp
from typing import Dict, Union
from lxml import html
from collections import OrderedDict
from urllib.request import urlopen
from argparse import ArgumentParser
from app.utils import getpath
from app import db, Base
from app.models import *


dateparse = datetime.datetime.strptime


def msplit(string: str, separators='/,;&'):
    def findsep(s: str):
        try:
            return next(filter(lambda i: i in s, separators))
        except StopIteration:
            return None

    if string:
        sep = findsep(string)
        if sep:
            ret = []
            for item in string.split(sep):
                item = item.strip()
                if item:
                    if findsep(item):
                        ret.extend(msplit(item))
                        continue
                    ret.append(item)
            return ret
        return [string]
    return []


def fix_csv(file):
    print('  + fixing encoding errors if any...')
    with open(file, 'rb') as fp:
        content = fp.read()

    while True:
        try:
            content.decode()
            break
        except UnicodeDecodeError as exc:
            pos = int(str(exc).split('in position')[-1].split(':')[0].strip())
            content = content[:pos] + content[pos+1:]

    _, dpath = mkstemp()
    with open(dpath, 'wb') as fp:
        fp.write(content)

    return dpath


class Degrees:
    url = 'http://www.sgs.utoronto.ca/facultyandstaff/Pages/Degrees-Honorifics.aspx'

    file = getpath('.degrees')

    manually_added = {
        'Dr': 'Doctorate',
        'PharmD': 'Doctor of Pharmacy',
        'BScPharm': 'Bachelor of Science in Pharmacy',
        'ACPR': 'Accredited Canadian Pharmacy Residency',
        'BCPP': 'Board Certified Psychiatric Pharmacist'
    }

    @staticmethod
    def normalize(string: str):
        return ''.join(string.split()).replace('.', '').lower()

    def __init__(self):
        self.data = None  # type: Union[Dict[str, str], None]

        if os.path.exists(self.file):
            with open(self.file, 'rb') as fp:
                self.data = pickle.load(fp)
        else:
            self.query_upstream()

        assert self.data is not None
        self._refs = set(self.normalize(s) for s in self.data.keys())

    def contains(self, degree: str, normalize=True):
        if normalize:
            haystack = self._refs
            degree = self.normalize(degree)
        else:
            haystack = self.data
        return degree in haystack

    def query_upstream(self):
        print('Downloading degrees from %r...' % self.url)

        resp = urlopen(self.url)
        tree = html.fromstring(resp.read().decode())
        tables = tree.cssselect('div#contentColumn table')

        data = {}
        for table in tables:
            tbody = table.cssselect('tbody')[0]
            for idx, tr in enumerate(tbody.getchildren()):
                if idx == 0:
                    continue
                abbr, full = [i.text_content().replace('\u200b', '').strip()
                              for i in tr.getchildren()]
                data[abbr] = ' '.join(full.split())

        data.update(self.manually_added)
        self.data = data

        with open(self.file, 'wb') as fp:
            pickle.dump(data, fp)


class Parser:
    file = None
    has_header = True
    data_asdict = False

    def __init__(self, file=None, autofix=False):
        self.data = None
        self.autofix = autofix
        self.parse_file(file or self.file)

    def parse_data(self, data):
        if not self.data_asdict:
            self.data = data
            return

        result = OrderedDict()
        for item in data:
            key = item.pop('key')
            if key not in result:
                result[key] = []
            result[key].append(item)
        self.data = result

    def parse_row(self, row):
        pass

    def parse_file(self, file):
        assert file and os.path.isfile(file)

        print('Parsing %r...' % file)
        if self.autofix:
            file = fix_csv(file)

        data = []
        with open(file, newline='', encoding='utf8') as fp:
            for idx, row in enumerate(csv.reader(fp)):
                if self.has_header and idx == 0:
                    continue
                data.append(self.parse_row(row))
            self.parse_data(data)

        if self.autofix and os.path.isfile(file):
            os.remove(file)

        print('  + done.')


class CourseCSV(Parser):
    file = getpath('data/courses.csv')

    def __init__(self, *args, **kwargs):
        self.degrees = Degrees()
        super(CourseCSV, self).__init__(*args, **kwargs)

    def parse_instructors(self, string: str):
        result, name = OrderedDict(), None
        for part in msplit(string):
            if name and self.degrees.contains(part):
                result[name].append(part)
                continue
            name, result[part] = part, []
        return result

    def parse_row(self, row):
        return {
            'key': row[1].lower() or None,
            'name': row[0] or None,
            'full_name': row[1] or None,
            'year': int(row[2]) if row[2] else None,
            'term': row[3].capitalize() or None,
            'faculty': row[4] or None,
            'categories': msplit(row[5]),
            'credits': float(row[6]) if row[6] else None,
            'instructors': self.parse_instructors(row[7]),
            'tas': msplit(row[8]),
            'outcomes': [i for i in row[11:] if i]
        }


class SessionCSV(Parser):
    data_asdict = True
    file = getpath('data/sessions.csv')
    find_objectives = re.compile(r'"([^"]+)"').findall
    find_num = re.compile(r'\d+').findall

    def parse_row(self, row):
        def getmin(s):
            found = self.find_num(s)
            if found:
                return int(found[0])
            return None

        return {
            'key': row[1].lower() or None,
            'title': row[6] or None,
            'section': row[7] or None,
            'location': row[8] or None,
            'guest_teachers': msplit(row[9]),
            'type': row[10].capitalize() or None,
            'length': getmin(row[11]),
            'date': dateparse(row[12], '%Y-%m-%d').date() if row[12] else None,
            'teaching_strategies': msplit(row[13]),
            'instruction_type': row[14].capitalize() or None,
            'topics': msplit(row[15], ';'),
            'objectives': self.find_objectives(row[16])
        }


class AssessmentCSV(SessionCSV):
    file = getpath('data/assessments.csv')

    def parse_row(self, row):
        return {
            'key': row[1].lower() or None,
            'title': row[6] or None,
            'type': row[7].capitalize() or None,
            'format': row[8] or None,
            'weight': int(row[9]) if row[9] else None,
            'cumulative': row[10] or None,
            'due_date': dateparse(row[11], '%y-%m-%d').date() if row[11] else None,
            'objectives': self.find_objectives(row[12])
        }


def get_args():
    parser = ArgumentParser()

    parser.add_argument('-c', '--course', metavar='FILE',
                        help='path to courses.csv, default is \'data/courses.csv\'')

    parser.add_argument('-s', '--session', metavar='FILE',
                        help='path to sessions.csv, default is \'data/sessions.csv\'')

    parser.add_argument('-a', '--assessment', metavar='FILE',
                        help='path to assessments.csv, default is \'data/assessments.csv\'')

    parser.add_argument('-f', '--fix-encoding', action='store_true', default=False,
                        help='fix the errors of character encoding automatically')

    # parser.add_argument('-r', '--refresh', action='store_true', default=False,
    #                     help='clean-up to refresh the database before import')

    args = parser.parse_args()
    args.refresh = True

    return args


def cleanup():
    confirm = input('You\'re about to clean up database by running this task. '
                    'Type "YES" to confirm: ')
    if confirm != 'YES':
        sys.exit()

    print('Cleaning up database...')
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
        if '_' not in table.name:
            seq = '%s_seq' % table.name
            db.execute('ALTER SEQUENCE %s RESTART WITH 1;' % seq)
    db.commit()


def create_categories(categories):
    ret = []
    for name in categories:
        cat = db.query(Category).filter_by(name=name).one_or_none()
        if not cat:
            cat = Category(name=name)
            db.add(cat)
            db.commit()
        ret.append(cat)
    return ret


def create_instructors(instructors):
    ret = []
    for name, degrees in instructors.items():
        instructor = db.query(Instructor).filter_by(name=name).one_or_none()
        if not instructor:
            instructor = Instructor(name=name, degrees=degrees)
            db.add(instructor)
            db.commit()
        ret.append(instructor)
    return ret


def main():
    args = get_args()

    # Cleanup db
    if args.refresh:
        cleanup()

    # Parsing files
    courses_csv = CourseCSV(file=args.course, autofix=args.fix_encoding)
    sessions_csv = SessionCSV(file=args.session, autofix=args.fix_encoding)
    assess_csv = AssessmentCSV(file=args.assessment, autofix=args.fix_encoding)

    print('Importing...')
    time.sleep(1)

    # Import data
    for data in courses_csv.data:
        key = data.pop('key')
        print('* Course:', data['full_name'])

        # Construct sessions
        sessions = sessions_csv.data.get(key)
        if sessions:
            sessions = [Session(**i) for i in sessions]
            print('  -> %d sessions found' % len(sessions))

        # Construct assessments
        assessments = assess_csv.data.get(key)
        if assessments:
            assessments = [Assessment(**i) for i in assessments]
            print('  -> %d assessments found' % len(assessments))

        # Construct course
        categories = create_categories(data.pop('categories'))
        instructors = create_instructors(data.pop('instructors'))
        course = Course(**data, categories=categories, instructors=instructors,
                        sessions=sessions or [], assessments=assessments or [])

        # Insert to db
        print('  -> saving...')
        db.add(course)
        if sessions:
            db.add_all(sessions)
        if assessments:
            db.add_all(assessments)
        db.commit()

    print('Done.')


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        print('Error: %s' % exc)
        sys.exit(1)
