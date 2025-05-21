FROM sagemath-custom:latest

USER root

WORKDIR /home/sage/sage

COPY chall.py .

EXPOSE 5002

CMD ["sage","-python3","chall.py"]
