FROM python:3.11-alpine

LABEL maintainer="Nomaan Khan <scholar@ihfc-iitd>"
LABEL description="Sovereign AI Stack (SAS) - Core REST Engine & Security Kernel"

WORKDIR /app

# Copy Core codebase
COPY . /app/NomaanOS-Core/

# Set Python search path across unified modules
ENV PYTHONPATH="/app/NomaanOS-Core:/app/NomaanOS-ShieldSOC:/app/NomaanOS-EvidenceLedger:/app/NomaanOS-GhostNode"

EXPOSE 8080

CMD ["python", "/app/NomaanOS-Core/api_server.py"]
