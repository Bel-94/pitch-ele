import unittest
from app.models import Pitch,User,Comment
from app import db

class Pitch(unittest.TestCase):
    def setUp(self):
        self.new_user = User(username="Test",password = 'codes')
        self.new_pitch = Pitch(pitch_title = 'Test',content = 'Test',category = 'Test',author = self.new_user)
        self.new_comment = Comment(content = 'Test',category = 'Test',author = self)

    def teardown(self):
        Pitch.query.delete()
        User.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_pitch.pitch_title,'Test')
        self.assertEquals(self.new_pitch.content,'Test')
        self.assertEquals(self.new_pitch.category,'Test')
        self.assertEquals(self.new_pitch.author,self.new_user)
        self.assertEquals(self.new_pitch.comments,self.new_comment)
        self.assertEquals(self.new_pitch.likes,self.new_like)
        self.assertEquals(self.new_pitch.dislikes,self.new_dislike)

    
    def test_save_pitch(self):
        self.new_pitch.save_pitch()
        self.assertTrue(len(Pitch.query.all())>0)

    def test_get_pitch(self):
        self.new_pitch.save_pitch()
        got_pitches = Pitch.get_pitch(1)
        self.assertTrue(len(got_pitches) == 1)


    class UserModelTest(unittest.TestCase):
        
     def setUp(self):
        self.new_user = User(password = 'codes')

    def test_password_setter(self):
        '''
        ascertains that when password is being hashed and the pass_secure contains a value.
        '''
        self.assertTrue(self.new_user.pass_secure is not None)

    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password

    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('codes'))