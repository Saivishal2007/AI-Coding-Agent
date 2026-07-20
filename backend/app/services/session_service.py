from uuid import UUID
from app.models.session import ChatSession, SessionMessage


class SessionService:

    def __init__(self):

        self.sessions: dict[str, ChatSession] = {}

    def get(self, session_id: UUID):

        sid = str(session_id)

        if sid not in self.sessions:

            self.sessions[sid] = ChatSession(id=sid)

        return self.sessions[sid]

    def add(

        self,

        session_id: UUID,

        role: str,

        content: str,

    ):

        session = self.get(session_id)

        session.messages.append(

            SessionMessage(

                role=role,

                content=content,

            )

        )

    def history(

        self,

        session_id: UUID,

    ):

        return [

            {

                "role": m.role,

                "content": m.content,

            }

            for m in self.get(session_id).messages

        ]

    def clear(

        self,

        session_id: UUID,

    ):

        sid = str(session_id)

        self.sessions.pop(sid, None)