from fastapi import FastAPI, HTTPException
import grpc
import sys
import os
from google.protobuf.json_format import MessageToDict

proto_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'proto'))
sys.path.insert(0, proto_path)

try:
    import glossary_pb2
    import glossary_pb2_grpc
    print("Импорт gRPC успешен")
except ImportError as e:
    print(f"Ошибка импорта gRPC: {e}")
    sys.exit()

app = FastAPI(title="Глоссарий REST API")

# Подключаемся к сервису 2
channel = grpc.insecure_channel('service2:50052')
client = glossary_pb2_grpc.GlossaryServiceStub(channel)


@app.get("/terms/")
def get_terms(skip: int = 0, limit: int = 100):
    request = glossary_pb2.GetTermsRequest(skip=skip, limit=limit)
    try:
        response = client.GetTerms(request)
        # генерируем ответ
        terms_list = [MessageToDict(term) for term in response.terms]
        return terms_list
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=e.details())


@app.get("/terms/search/")
def search_terms(keyword: str):
    request = glossary_pb2.GetTermsRequest(skip=0, limit=1000)
    try:
        response = client.GetTerms(request)
        filtered_terms = [term for term in response.terms if keyword.lower() in term.keyword.lower()]
        filtered_dict = [MessageToDict(term) for term in filtered_terms]
        return filtered_dict
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=e.details())


@app.get("/terms/{keyword}")
def get_term(keyword: str):
    request = glossary_pb2.GetTermRequest(keyword=keyword)
    try:
        response = client.GetTerm(request)
        if not response.term.id:
            raise HTTPException(status_code=404, detail="Термин не найден")
        return MessageToDict(response.term)
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail="Термин не найден")
        raise HTTPException(status_code=500, detail=e.details())


@app.post("/terms/")
def create_term(keyword: str, description: str):
    request = glossary_pb2.CreateTermRequest(keyword=keyword, description=description)
    try:
        response = client.CreateTerm(request)
        if not response.term.id:
            raise HTTPException(status_code=500, detail="Не удалось создать термин")
        return MessageToDict(response.term)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=e.details())


@app.put("/terms/{keyword}")
def update_term(keyword: str, description: str):
    request = glossary_pb2.UpdateTermRequest(keyword=keyword, description=description)
    try:
        response = client.UpdateTerm(request)
        if not response.term.id:
            raise HTTPException(status_code=404, detail="Термин не найден")
        return MessageToDict(response.term)
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail="Термин не найден")
        raise HTTPException(status_code=500, detail=e.details())


@app.delete("/terms/{keyword}")
def delete_term(keyword: str):
    request = glossary_pb2.DeleteTermRequest(keyword=keyword)
    try:
        response = client.DeleteTerm(request)
        if response.success:
            return {"detail": "Термин удален"}
        else:
            raise HTTPException(status_code=404, detail="Термин не найден")
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=e.details())
