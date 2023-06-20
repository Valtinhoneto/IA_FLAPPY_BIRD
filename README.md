# IA_FLAPPY_BIRD

Flappy Bird AI
Este é um projeto de implementação de uma inteligência artificial para jogar o jogo Flappy Bird utilizando a biblioteca Pygame e a biblioteca NEAT (NeuroEvolution of Augmenting Topologies).

#Descrição
O Flappy Bird AI é um programa que utiliza algoritmos genéticos e redes neurais para treinar uma inteligência artificial capaz de jogar o jogo Flappy Bird de forma autônoma. O objetivo do jogo é controlar um pássaro para evitar que ele colida com os canos que se movem em sua direção. A inteligência artificial aprende a jogar o jogo por meio de tentativa e erro, buscando maximizar sua pontuação.

#Funcionamento
O programa utiliza a biblioteca NEAT para evoluir uma população de redes neurais. Cada rede neural representa um pássaro no jogo. As redes neurais recebem informações sobre a posição do pássaro, a distância até o próximo cano e a distância até o topo e a base do cano. Com base nessas informações, a rede neural toma uma decisão sobre quando o pássaro deve pular. As redes neurais com melhor desempenho, ou seja, aquelas que conseguem obter pontuações mais altas, são selecionadas para reprodução, gerando uma nova geração de redes neurais com pequenas variações. Esse processo de seleção e reprodução é repetido várias vezes até que a inteligência artificial seja capaz de jogar o jogo de forma eficiente.

#Instalação
Para executar o programa, é necessário ter o Python instalado em seu sistema. Além disso, é preciso instalar as bibliotecas Pygame e NEAT. Você pode instalá-las executando os seguintes comandos no terminal:

#Copy code
pip install pygame
pip install neat-python
Após instalar as bibliotecas, baixe o código-fonte do projeto e execute o arquivo flappy_bird_ai.py com o Python.

#Controles
A inteligência artificial joga o jogo de forma autônoma e não requer interação do usuário. O programa irá exibir na tela a pontuação atual e a geração em que a IA está.

#Contribuição
Sinta-se à vontade para contribuir com o projeto fazendo melhorias, corrigindo erros ou adicionando novos recursos. Basta fazer um fork do repositório, fazer as alterações desejadas e enviar um pull request.

#Licença
Este projeto está licenciado sob a MIT License. Sinta-se à vontade para usar, modificar e distribuir o código conforme necessário.
