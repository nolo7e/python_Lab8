import grpc
from concurrent import futures
import time
import sys
import os

proto_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'proto'))
sys.path.insert(0, proto_path)

from sqlmodel import Session
from database import engine
import models
import crud

try:
    import glossary_pb2
    import glossary_pb2_grpc
    print("Импорт gRPC успешен")
except ImportError as e:
    print(f"Ошибка импорта gRPC: {e}")
    sys.exit()

models.SQLModel.metadata.create_all(bind=engine)


class GlossaryServiceServicer(glossary_pb2_grpc.GlossaryServiceServicer):
    def GetTerms(self, request, context):
        print(f"GetTerms request = {request}")
        with Session(engine) as db:
            terms = crud.get_terms(db)
            terms_pb = [glossary_pb2.Term(id=term.id, keyword=term.keyword, description=term.description) for term in terms]
            return glossary_pb2.GetTermsResponse(terms=terms_pb)

    def GetTerm(self, request, context):
        print(f"GetTerm request.keyword = {request.keyword}")
        with Session(engine) as db:
            term = crud.get_term(db, request.keyword)
            if term:
                term_pb = glossary_pb2.Term(id=term.id, keyword=term.keyword, description=term.description)
                return glossary_pb2.GetTermResponse(term=term_pb)
            else:
                context.set_details('Термин не найден')
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return glossary_pb2.GetTermResponse()

    def CreateTerm(self, request, context):
        print(f"CreateTerm request.keyword = {request.keyword}, request.description = {request.description}")
        with Session(engine) as db:
            try:
                term_create = crud.TermCreate(keyword=request.keyword, description=request.description)
                term = crud.create_term(db, term_create)
                term_pb = glossary_pb2.Term(id=term.id, keyword=term.keyword, description=term.description)
                return glossary_pb2.CreateTermResponse(term=term_pb)
            except Exception as e:
                context.set_details(str(e))
                context.set_code(grpc.StatusCode.INTERNAL)
                return glossary_pb2.CreateTermResponse()

    def UpdateTerm(self, request, context):
        print(f"UpdateTerm request.keyword = {request.keyword}, request.description = {request.description}")
        with Session(engine) as db:
            term_update = crud.TermUpdate(description=request.description)
            term = crud.update_term(db, request.keyword, term_update)
            if term:
                term_pb = glossary_pb2.Term(id=term.id, keyword=term.keyword, description=term.description)
                return glossary_pb2.UpdateTermResponse(term=term_pb)
            else:
                context.set_details('Термин не найден')
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return glossary_pb2.UpdateTermResponse()

    def DeleteTerm(self, request, context):
        print(f"DeleteTerm request.keyword = {request.keyword}")
        with Session(engine) as db:
            success = crud.delete_term(db, request.keyword)
            if success:
                return glossary_pb2.DeleteTermResponse(success=True)
            else:
                context.set_details('Термин не найден')
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return glossary_pb2.DeleteTermResponse(success=False)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(GlossaryServiceServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("gRPC сервер запущен на порту 50052")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
