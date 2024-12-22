```bash
pip3 install grpcio grpcio-tools
```

```bash
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. glossary.proto
```