from __future__ import absolute_import
'''
Models for subjects.
'''
#=============================================================================
# Standard library imports
#=============================================================================
from collections import OrderedDict
import datetime

#=============================================================================
# Django imports 
#=============================================================================
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

#=============================================================================
# Wilhelm imports
#=============================================================================
from apps.core.utils.django import uid, user_exists
from apps.core.utils.datetime import age_from_dob

#================================ End Imports ================================

class SubjectManager(models.Manager):

    def create_temp_subject(self, user):

        while True:
            subject_uid = uid()
            if not self.filter(uid=subject_uid):
                break

        now = datetime.datetime.today()
        subject = self.create(uid=subject_uid, 
                              user=user, 
                              temp_subject=True, 
                              created=now)

        return subject

    def user_has_subject_entry(self, user):

        try:
            self.get(user=user)
            return True
        except ObjectDoesNotExist:
            return False

    def user_does_not_have_subject_entry(self, user):
        return not self.user_has_subject_entry(user)

    def create_subject(self, user, **kwargs):

        user_does_not_exist_err = 'User "%s" does not exist.' % user.username
        user_has_subject_err = 'User "%s" already has a subject.' % user.username

        assert user_exists(user), user_does_not_exist_err
        assert self.user_does_not_have_subject_entry(user), user_has_subject_err

        subject_uid = uid()

        return Subject.objects.create(uid=subject_uid, 
                                      user=user, 
                                      **kwargs)

class Subject(models.Model):
    objects = SubjectManager()

    uid = models.CharField(primary_key=True, max_length=settings.UID_LENGTH)
    user = models.ForeignKey(User)

    temp_subject = models.BooleanField(default=False)
    created = models.DateTimeField(null=True)

    login_method = models.CharField(max_length=100, 
                                    default = 'wilhelm',
                                    blank=True, 
                                    null=True)

    @property
    def social_media_login(self):
        return self.login_method != 'wilhelm'

    ################
    # Demographics #
    ################
    date_of_birth = models.DateField(null=True, blank=True)
    right_handed = models.NullBooleanField()
    male = models.NullBooleanField()
    is_english_speaker = models.NullBooleanField(null=True, blank=True)
    native_language = models.CharField(max_length=50, blank=True, null=True)

    ############################################
    # Properties to check if demographic variable is present #
    ############################################
    @property
    def has_dob(self):
        ''' Return True if we have the subject's date of birth. '''
        return not (self.date_of_birth is None)

    @property
    def has_handedness(self):
        ''' Return True if we have the subject's handedness information.'''
        return not (self.right_handed is None)

    @property
    def has_sex(self):
        ''' Return True if we have the subject's sex. '''
        return not (self.male is None)

    @property
    def has_language(self):
        ''' Return True if we have the subject's native language info.'''
        return not (self.is_english_speaker is None and self.native_language is None)

    def has(self, variable):

        has_a = {'Date_of_Birth': self.has_dob,
                 'Handedness': self.has_handedness,
                 'Native_Language': self.has_language,
                 'Sex': self.has_sex}

        return has_a[variable]

    #######################
    # Read out properties #
    #######################
    @property
    def age(self):
        try:
            return age_from_dob(self.date_of_birth)
        except:
            return None

    @property
    def birthdate(self):
        if self.has_dob:
           return  '{dt:%B} {dt.day}, {dt.year}'.format(dt=self.date_of_birth)

    @property
    def sex(self):
        if self.has_sex:
            return 'Male' if self.male else 'Female'

    @property
    def handedness(self):
        if self.has_handedness:
            return 'Right handed' if self.right_handed else 'Left handed'

    def profile_export(self):

        """
        Export the subject's profile as a dict to be used in data exports.

        """

        export_dict = OrderedDict()

        export_dict['Subject ID'] = self.uid[:settings.UID_SHORT_LENGTH]
        export_dict['Date of birth'] = self.birthdate
        export_dict['Age'] = self.age
        export_dict['Sex'] = self.sex
        export_dict['Handedness'] = self.handedness
        export_dict['User ID'] = self.user.pk
        export_dict['Login method'] = self.login_method
        export_dict['Temporary subject'] = self.temp_subject
        export_dict['Subject created'] = self.created

        return export_dict
