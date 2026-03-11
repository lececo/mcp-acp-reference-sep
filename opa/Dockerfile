FROM openpolicyagent/opa:latest

COPY policies /policies
COPY data /data

CMD ["run", "--server", "--addr", ":8181", "/policies", "/data"]
