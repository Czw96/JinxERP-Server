FROM python:3.13

COPY . /jinx_v2
WORKDIR /jinx_v2

ENV DEBUG=False
ENV HOST=*

RUN mkdir -p ./volumes/logs
RUN mkdir -p ./volumes/media
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
