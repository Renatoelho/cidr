# CIDR: Entendendo as classes de IP no Docker

O **CIDR (Classless Inter-Domain Routing)** e as subnets são fundamentais para a alocação eficiente de **endereços IP** e segmentação de redes, eliminando as limitações das antigas classes de IP (A, B e C). No contexto do **Docker**, o CIDR é amplamente utilizado para definir redes virtuais personalizadas, permitindo que contêineres se comuniquem dentro de um mesmo subnet ou sejam isolados em diferentes redes. Ao criar um **docker network** com uma faixa CIDR específica, é possível **otimizar** a distribuição de endereços IP, melhorar a **segurança** e garantir que diferentes serviços dentro do ambiente conteinerizado possam se conectar de forma eficiente. Além disso, ao trabalhar com múltiplas faixas de IP no **Docker Compose**, é essencial compreender o mascaramento de sub-rede e roteamento entre bridges para garantir que aplicações distribuídas operem corretamente sem conflitos de endereçamento.

<!--
https://www.youtube.com/@renato-coelho
-->

## Apresentação em Vídeo

<p align="center">
  <a href="https://youtu.be/cOIcNH27gkI" target="_blank"><img src="imagens/thumbnail/thumbnail-cidr-faixas-ip-docker-github-01.png" alt="Vídeo de apresentação"></a>
</p>

![YouTube Video Views](https://img.shields.io/youtube/views/cOIcNH27gkI) ![YouTube Video Likes](https://img.shields.io/youtube/likes/cOIcNH27gkI)

### Requisitos

+ ![Docker](https://img.shields.io/badge/Docker-27.4.1-E3E3E3)
+ ![Docker-compose](https://img.shields.io/badge/Docker--compose-1.25.0-E3E3E3)
+ ![Git](https://img.shields.io/badge/Git-2.25.1%2B-E3E3E3)
+ ![Ubuntu](https://img.shields.io/badge/Ubuntu-20.04-E3E3E3)

## Conceitos de CIDR e máscara de Sub-rede

O CIDR foi introduzido para permitir uma alocação de endereços mais eficiente, substituindo as antigas classes fixas de IP (A, B e C). Ele utiliza um sufixo `/n` para indicar o tamanho da sub-rede.

### Exemplos de redes CIDR:

- `10.0.0.0/16` → 65.536 endereços (Classe A)
- `172.16.0.0/12` → 1.048.576 endereços (Classe B)
- `192.168.1.0/24` → 256 endereços (Classe C)

### Limites das faixas de IPs privados:

| Faixa de IP                    | Máscara             | Endereços totais |
|--------------------------------|---------------------|------------------|
| 10.0.0.0 → 10.255.255.255      | /8                  | 16.777.216       |
| 172.16.0.0 → 172.31.255.255    | /12                 | 1.048.576        |
| 192.168.0.0 → 192.168.255.255  | /16                 | 65.536           |


### Cálculo de Intervalos de IPs

A quantidade de endereços disponíveis em uma sub-rede pode ser calculada como:

**Quantidade de IPs = 2 ^ (32 − Máscara)**

**Exemplos:**

- Para `10.10.1.0/24`: `2 ^ (32 - 24) = 256`
- Para `10.10.1.0/26`: `2 ^ (32 - 26) = 64 - 3 (endereços reservados) = 61`

📌 **Endereços Reservados:**

- **Endereço de Rede:** O primeiro endereço (`10.10.1.0`)
- **Gateway da Rede Docker:** O endereço (`10.10.1.1`)
- **Broadcast:** O último endereço do intervalo (`10.10.1.?`)

## Criando redes customizadas no Docker

O Docker permite definir redes personalizadas com CIDR, facilitando a segmentação de aplicações.

### Exemplo de `docker-compose.yaml`:

```yaml
services:
  app:
    build:
      context: .
      dockerfile: dockerfile
    image: imagem-modelo:0.0.1
    ports:
      - 8000-8004:8000 # O intervalo de portas está ligado à quantidade de réplicas.
    volumes:
      - ./src:/src
    deploy:
      replicas: 5 # O número de réplicas está ligado à quantidade de IPs válidos.
    restart: always
    command: uvicorn app:app --host 0.0.0.0 --port 8000 --reload
    networks:
      - rede_cidr
networks:
  rede_cidr:
    driver: bridge
    ipam:
      config:
        - subnet: 10.3.0.0/29 # 8 IPs 5 válidos
```

**Execute o comando para subir as aplicações:**

```bash
docker compose -p cidr -f docker-compose.yaml up -d --build
```

📌 **Explicação:**

- Criamos uma rede `rede_cidr` com a sub-rede `10.3.0.0/29`.
- O número de **réplicas** da aplicação está diretamente ligado ao número de **IPs disponíveis**.
- O intervalo de portas (`8000-8004`) segue a quantidade de réplicas configuradas.

## Referências

Endereço de IP, **Wikipedia**. Disponível em: <https://pt.wikipedia.org/wiki/Endereço_IP>. Acesso em: 04 fev. 2025.

Classless Inter-domain Routing (CIDR), **RFC 4632**. Disponível em: <https://datatracker.ietf.org/doc/html/rfc4632>. Acesso em: 04 fev. 2025.

Networking overview, **Docker Docs**. Disponível em: <https://docs.docker.com/engine/network/>. Acesso em: 04 fev. 2025.
