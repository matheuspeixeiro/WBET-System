# Gaze-Based-Computer-Control

**Sistema de Rastreamento Ocular Baseado em Câmera para Controle de Interfaces Computacionais**

## Descrição do Projeto

O **Gaze-Based-Computer-Control** é um sistema de tecnologia assistiva de baixo custo que permite a interação com computadores usando apenas o movimento dos olhos. Desenvolvido como projeto de TCC, o sistema utiliza uma webcam convencional e algoritmos de visão computacional para rastrear o olhar do usuário e convertê-lo em comandos de controle, como a movimentação do cursor e a seleção de itens.

A motivação principal é oferecer uma alternativa acessível para indivíduos com deficiências motoras severas, como a Esclerose Lateral Amiotrófica (ELA), que muitas vezes perdem a capacidade de usar mouses e teclados tradicionais, mas mantêm o controle dos movimentos oculares.

## Objetivos

**Desenvolver um sistema de baixo custo**: Utilizar hardware de fácil acesso, como uma webcam, para democratizar a tecnologia de rastreamento ocular.
**Permitir o controle do cursor**: Mapear os movimentos do olhar para a navegação em interfaces gráficas.
**Interpretar comandos**: Reconhecer ações voluntárias como um piscar prolongado para simular o clique do mouse.
**Criar uma interface funcional**: Desenvolver um editor de texto simples para demonstrar a usabilidade e a eficácia do sistema.

## Tecnologias Utilizadas

O projeto é construído principalmente em Python, aproveitando o poder de bibliotecas especializadas em visão computacional e processamento de imagem:

* **Python**: Linguagem de programação principal.
**OpenCV**: Biblioteca de código aberto para visão computacional, usada para a captura de vídeo da webcam e o processamento de imagens.
**Dlib**: Toolkit de machine learning com foco em detecção e análise facial, fundamental para a localização dos marcos (landmarks) do rosto e dos olhos.
**NumPy**: Biblioteca para computação numérica, utilizada para manipulação de dados e cálculos matemáticos.
**python-docx**: Biblioteca para a criação e manipulação de arquivos `.docx`.

## Funcionalidades Principais

**Rastreamento Ocular em Tempo Real**: O sistema identifica a posição do rosto e dos olhos em tempo real para determinar a direção do olhar.
**Classificação da Direção do Olhar**: Categoriza a direção do olhar em "cima", "baixo", "esquerda", "direita" e "centro" para controlar a navegação.
**Calibração Dinâmica**: O usuário realiza uma calibração inicial para personalizar a sensibilidade do rastreamento de acordo com suas características faciais e distância da câmera.
**Comando de Clique**: Um piscar prolongado é interpretado como um comando de clique do mouse.
