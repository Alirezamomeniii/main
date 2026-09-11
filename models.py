from datetime import datetime


class User:
    def __init__(self,telegram_id,username):
        self.telegram_id  =telegram_id
        self.username=username


class Ticket:
    def __init__(self, ticket_id,user_id,title,description,
                 status="OPEN", created_at=None):
        self.id=ticket_id
        self.user_id=user_id
        self.title=title
        self.description =description
        self.status =status

        if created_at is None:
            self.created_at = datetime.now()
        elif isinstance(created_at, str):
            
            self.created_at= datetime.strptime(created_at,"%Y-%m-%d %H:%M:%S")
        else:
            self.created_at= created_at