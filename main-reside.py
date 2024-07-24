import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

# Caminho da pasta de entrada e saída
pasta_entrada = 'img-input'
pasta_saida = 'img-output'

def redimensionar_imagem(image_path, nova_largura):
    # Carregar a imagem usando OpenCV
    imagem = cv2.imread(image_path)
    
    # Dimensões originais
    altura_original, largura_original = imagem.shape[:2]
    
    # Calcular a nova altura proporcional
    nova_altura = int((nova_largura / largura_original) * altura_original)
    
    # Redimensionar a imagem
    imagem_redimensionada = cv2.resize(imagem, (nova_largura, nova_altura), interpolation=cv2.INTER_LINEAR)
    
    return imagem_redimensionada

def melhorar_imagem_texto(imagem_cv):
    # Converter imagem de OpenCV (BGR) para PIL (RGB)
    imagem_pil = Image.fromarray(cv2.cvtColor(imagem_cv, cv2.COLOR_BGR2RGB))
    
    # Aumentar o contraste
    enhancer = ImageEnhance.Contrast(imagem_pil)
    imagem_contraste = enhancer.enhance(2.0)
    
    # Aumentar a nitidez
    enhancer = ImageEnhance.Sharpness(imagem_contraste)
    imagem_nitida = enhancer.enhance(2.0)
    
    # Aplicar filtro de borda para realçar textos
    imagem_filtrada = imagem_nitida.filter(ImageFilter.EDGE_ENHANCE)
    
    # Converter de volta para OpenCV
    imagem_final = cv2.cvtColor(np.array(imagem_filtrada), cv2.COLOR_RGB2BGR)
    
    return imagem_final

def processar_imagens_pasta(pasta_entrada, pasta_saida, nova_largura):
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
    
    for nome_arquivo in os.listdir(pasta_entrada):
        caminho_completo = os.path.join(pasta_entrada, nome_arquivo)
        
        # Verificar se é um arquivo de imagem suportado
        if nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            try:
                print(f"Processando imagem: {nome_arquivo}")
                
                # Redimensionar a imagem
                imagem_redimensionada = redimensionar_imagem(caminho_completo, nova_largura)
                
                # Melhorar a qualidade da imagem redimensionada
                imagem_melhorada = melhorar_imagem_texto(imagem_redimensionada)
                
                # Salvar a imagem resultante
                caminho_saida = os.path.join(pasta_saida, nome_arquivo)
                cv2.imwrite(caminho_saida, imagem_melhorada)
                
                print(f"Imagem salva em: {caminho_saida}")
            except Exception as e:
                print(f"Erro ao processar a imagem {nome_arquivo}: {e}")



# Nova largura desejada
nova_largura = 1500

# Processar todas as imagens na pasta de entrada
processar_imagens_pasta(pasta_entrada, pasta_saida, nova_largura)

print("Processamento de imagens concluído!")
