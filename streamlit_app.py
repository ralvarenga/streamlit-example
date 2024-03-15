import cv2
from pyzbar.pyzbar import decode
import numpy as np
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        super().__init__()

    def transform(self, frame):
        image = frame.to_ndarray(format="bgr24")
        barcodes = read_barcodes(image)
        
        for barcode in barcodes:
            # Desenhando um retângulo ao redor do código de barras
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 5)
            # Obtendo os dados do código de barras
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type
            # Exibindo os dados na interface
            st.write(f"Tipo de código de barras: {barcode_type}")
            st.write(f"Dados do código de barras: {barcode_data}")

        return image

def read_barcodes(image):
    # Convertendo a imagem para escala de cinza
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Decodificando os códigos de barras na imagem
    barcodes = decode(gray_img)
    return barcodes

def main():
    st.title('Leitor de Código de Barras via Webcam')

    webrtc_ctx = webrtc_streamer(
        key="example",
        video_transformer_factory=VideoTransformer,
        async_transform=True,
    )

if __name__ == "__main__":
    main()
