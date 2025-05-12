# E-commerce Doce Costura
## Visão Geral
Este repositório contém o código fonte do projeto E-commerce Doce Costura, uma plataforma completa de comércio eletrônico com arquitetura de microserviços. O sistema inclui frontend React, gateway de API e múltiplos serviços backend para autenticação, catálogo de produtos, recomendações personalizadas e processamento de pagamentos.

## Tecnologias Utilizadas
### Backend
- Django/Django REST Framework: Framework web para desenvolvimento rápido de APIs
- PostgreSQL: Banco de dados relacional
- Stripe: Processamento de pagamentos
- Pandas/Scikit-learn: Algoritmos de recomendação

### Frontend
- React: Biblioteca para construção de interfaces
- Material-UI: Componentes React com design responsivo
- React Router: Navegação entre páginas
- Axios: Cliente HTTP para requisições à API
- JWT: Autenticação baseada em tokens
- Infraestrutura

# Como utilizar instalar e executar
Para instalar é necessário ter o docker e o docker-comopose pre-instalados
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

Em seguida basta clonar o repositório:
```bash
    sudo git clone https://github.com/levisilva22/Software-Doce-Costura.git
```
Executar os comandos docker-compose para construir os conteiners
```bash
  sudo docker-compose -build
  sudo docker-compose up
```

Tudo pronto, os serviços estaram rodando nas portas configuradas no arquivo docker-compose.yaml.
