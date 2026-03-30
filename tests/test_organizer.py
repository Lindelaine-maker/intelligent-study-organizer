import unittest
from study_organizer import StudyOrganizer

class TestStudyOrganizer(unittest.TestCase):

    def setUp(self):
        self.organizer = StudyOrganizer()

    def test_add_discipline(self):
        self.organizer.add_discipline('Math')
        self.assertIn('Math', self.organizer.disciplines)

    def test_add_task(self):
        self.organizer.add_discipline('Science')
        self.organizer.add_task('Science', 'Complete experiment')
        self.assertIn('Complete experiment', self.organizer.tasks['Science'])

    def test_validation_empty_discipline(self):
        with self.assertRaises(ValueError):
            self.organizer.add_discipline('')

    def test_validation_adding_task_to_nonexistent_discipline(self):
        with self.assertRaises(ValueError):
            self.organizer.add_task('Nonexistent', 'Do something')

    def test_data_persistence(self):
        self.organizer.add_discipline('History')
        self.organizer.add_task('History', 'Read chapter 1')
        self.organizer.save_data()  
        new_organizer = StudyOrganizer()
        new_organizer.load_data()
        self.assertIn('History', new_organizer.disciplines)
        self.assertIn('Read chapter 1', new_organizer.tasks['History'])

if __name__ == '__main__':
    unittest.main()