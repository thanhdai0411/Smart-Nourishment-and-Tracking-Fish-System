from email.policy import default
import mongoengine as me


class StatusTrain(me.Document):
    status = me.StringField()
    dateEnd = me.StringField()
    dateStart = me.StringField()
    username = me.StringField()
    action = me.StringField()
    name_fish = me.StringField()
    

    def to_json(self):
        return {
            "status": self.status,
            "dateEnd": self.dateEnd,
            "dateStart": self.dateStart,
            "username": self.username,
            "action": self.action,
            "name_fish": self.name_fish,
        }
