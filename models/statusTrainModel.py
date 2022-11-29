from email.policy import default
import mongoengine as me


class StatusTrain(me.Document):
    status = me.StringField()
    dateEnd = me.DateTimeField()
    dateStart = me.DateTimeField()
    seen = me.BooleanField()
    title = me.StringField()

    def to_json(self):
        return {
            "status": self.username,
            "dateEnd": self.dateEnd,
            "dateStart": self.dateStart,
            "seen": self.seen,
            "title": self.title

        }
