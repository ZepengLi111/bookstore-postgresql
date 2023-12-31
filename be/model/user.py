import jwt
import time
import logging
import sqlalchemy
from be.model import error
from be.model import db_conn

# encode a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }

def jwt_encode(user_id: str, terminal: str) -> str:
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal, "timestamp": time.time()},
        key=user_id,
        algorithm="HS256",
    )
    return encoded.encode("utf-8").decode("utf-8")

# decode a JWT to a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }
def jwt_decode(encoded_token, user_id: str) -> str:
    decoded = jwt.decode(encoded_token, key=user_id, algorithms="HS256")
    return decoded
 

class User(db_conn.DBConn):
    token_lifetime: int = 3600  # 3600 second

    def __init__(self):
        db_conn.DBConn.__init__(self)

    def __check_token(self, user_id, db_token, token) -> bool:
        try:
            if db_token != token:
                return False
            jwt_text = jwt_decode(encoded_token=token, user_id=user_id)
            ts = jwt_text["timestamp"]
            if ts is not None:
                now = time.time()
                if self.token_lifetime > now - ts >= 0:
                    return True
        except jwt.exceptions.InvalidSignatureError as e:
            logging.error(str(e))
            return False

    def register(self, user_id: str, password: str) -> (int, str):
        try:
            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            self.session.add(db_conn.User(id=user_id, password=password, token=token, terminal=terminal, balance=0))
            self.session.commit()
        
        except sqlalchemy.exc.SQLAlchemyError as e:
            self.session.rollback()
            return 528, "SQL error: {}".format(str(e)),
        except Exception as e:
            self.session.rollback()
            return 530, "Internal server error: {}".format(str(e)),

        return 200, "ok"

    def check_token(self, user_id: str, token: str) -> (int, str):
        user = self.fetch_user(user_id)

        if user is None:
            return error.error_authorization_fail()
        db_token = user.token
        if not self.__check_token(user_id, db_token, token):
            return error.error_authorization_fail()
        return 200, "ok"

    def check_password(self, user_id: str, password: str) -> (int, str):
        user = self.fetch_user(user_id)
        if user is None:
            return error.error_authorization_fail()

        if password != user.password:
            return error.error_authorization_fail()
        return 200, "ok"

    def login(self, user_id: str, password: str, terminal: str) -> (int, str, str):
        token = ""
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message, ""

            token = jwt_encode(user_id, terminal)
            user = self.fetch_user(user_id)
            if user is None:
                return error.error_authorization_fail()

            user.token = token
            user.terminal = terminal
            self.session.commit()
        
        except sqlalchemy.exc.SQLAlchemyError as e:
            self.session.rollback()
            return 528, "SQL error: {}".format(str(e)), ""
        except Exception as e:
            self.session.rollback()
            return 530, "Internal server error: {}".format(str(e)), ""

        return 200, "ok", token

    def logout(self, user_id: str, token: str) -> (int, str):
        try:
            code, message = self.check_token(user_id, token)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            dummy_token = jwt_encode(user_id, terminal)

            user = self.fetch_user(user_id)
            if user is None:
                return error.error_authorization_fail()

            user.token = dummy_token
            user.terminal = terminal
            self.session.commit()

        except sqlalchemy.exc.SQLAlchemyError as e:
            self.session.rollback()
            return 528, "SQL error: {}".format(str(e))
        except Exception as e:
            self.session.rollback()
            return 530, "Internal server error: {}".format(str(e))

        return 200, "ok"

    def unregister(self, user_id: str, password: str) -> (int, str):
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message

            user = self.fetch_user(user_id)
            if user is None:
                return error.error_authorization_fail()

            # TODO DO NOT DELETE
            self.session.delete(user)
            self.session.commit()
 
        except sqlalchemy.exc.SQLAlchemyError as e:
            self.session.rollback()
            return 528, "SQL error: {}".format(str(e))
        except Exception as e:
            self.session.rollback()
            return 530, "Internal server error: {}".format(str(e))

        return 200, "ok"

    def change_password(
        self, user_id: str, old_password: str, new_password: str
    ) -> bool:
        try:
            code, message = self.check_password(user_id, old_password)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)

            user = self.fetch_user(user_id)
            if user is None:
                return error.error_authorization_fail()

            user.password = new_password
            user.token = token
            user.terminal = terminal
            self.session.commit()

        except sqlalchemy.exc.SQLAlchemyError as e:
            self.session.rollback()
            return 528, "SQL error: {}".format(str(e))
        except Exception as e:
            self.session.rollback()
            return 530, "Internal server error: {}".format(str(e))

        return 200, "ok"
