FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    wget \
    poppler-utils \
    curl \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libblas-dev \
    liblapack-dev \
    gfortran \
    git \
    libgl1

COPY app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN pip install fastapi uvicorn httpx
RUN pip install paddleocr
RUN pip install paddlepaddle-gpu==3.0.0rc1 -i 'https://www.paddlepaddle.org.cn/packages/stable/cu118/'

# # Create the directory structure for PaddleOCR models
RUN mkdir -p /home/root/.paddleocr/whl/det/en/en_PP-OCRv3_det_infer
RUN mkdir -p /home/root/.paddleocr/whl/rec/en/en_PP-OCRv4_rec_infer
RUN mkdir -p /home/root/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer

# # Set ownership and permissions
RUN chown -R root:root /home/root/.paddleocr/
RUN chmod -R 700 /home/root/.paddleocr/

# # Download PaddleOCR models using wget
RUN wget -O /home/root/.paddleocr/whl/det/en/en_PP-OCRv3_det_infer/en_PP-OCRv3_det_infer.tar https://paddleocr.bj.bcebos.com/PP-OCRv3/english/en_PP-OCRv3_det_infer.tar
RUN wget -O /home/root/.paddleocr/whl/rec/en/en_PP-OCRv4_rec_infer/en_PP-OCRv4_rec_infer.tar https://paddleocr.bj.bcebos.com/PP-OCRv4/english/en_PP-OCRv4_rec_infer.tar
RUN wget -O /home/root/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer/ch_ppocr_mobile_v2.0_cls_infer.tar https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar

WORKDIR /app
COPY /app /app

# Expose the port for FastAPI
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
