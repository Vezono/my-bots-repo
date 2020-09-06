from openMystatAPI import api


class Student:
    def __init__(self, username, password):
        self.api = api.StudentApi(username, password)

    @property
    def name(self):
        return self.api.user_info['full_name']

    @property
    def group(self):
        return self.api.user_info['group_name']

    @property
    def stream(self):
        return self.api.user_info['stream_name']

    @property
    def level(self):
        return self.api.user_info['level']

    @property
    def photo_url(self):
        return self.api.user_info['photo']

    @property
    def crystalls(self):
        return self.api.user_info['gaming_points'][0]['points'] - self.api.user_info['spent_gaming_points'][0]['points']

    @property
    def coins(self):
        return self.api.user_info['gaming_points'][1]['points'] - self.api.user_info['spent_gaming_points'][1]['points']

    @property
    def achieves_count(self):
        return self.api.user_info['achieves_count']

    @property
    def address(self):
        return self.api.profile_data['address']

    @property
    def birth_date(self):
        return self.api.profile_data['date_birth']

    @property
    def study(self):
        return self.api.profile_data['study']

    @property
    def email(self):
        return self.api.profile_data['email']

    @property
    def phone_number(self):
        return self.api.profile_data['phones'][0]['phone_number']

    @property
    def links(self):
        return self.api.profile_data['links']

    @property
    def relatives(self):
        return self.api.profile_data['relatives']

    @property
    def azure(self):
        return self.api.profile_data['azure']
