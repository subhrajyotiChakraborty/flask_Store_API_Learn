from ma import ma
from marshmallow import pre_dump
from models.user import UserModel
from schemas.confirmation import ConfirmationSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    # confirmations = ma.Nested(ConfirmationSchema, many=True)

    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "confirmation")
        load_instance = True
        include_relationships = True

    @pre_dump
    def _pre_dump(self, user: UserModel, **kwargs):
        user.confirmation = [user.most_recent_confirmation]
        return user