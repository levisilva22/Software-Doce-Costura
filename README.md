E-commerce Doce Costura
Visão Geral
Este repositório contém o código fonte do projeto E-commerce Doce Costura, uma plataforma completa de comércio eletrônico com arquitetura de microserviços. O sistema inclui frontend React, gateway de API e múltiplos serviços backend para autenticação, catálogo de produtos, recomendações personalizadas e processamento de pagamentos.

Estrutura do Projeto
E-commerce/
├── api_gateway/          # Gateway de API central
├── auth_service/         # Serviço de autenticação e usuários
├── DoceCostura/          # Serviço principal de produtos e pedidos
├── frontend/             # Interface de usuário React
├── recommendation_service/ # Sistema de recomendação de produtos
└── docker-compose.yml    # Configuração dos contêineres Docker

Tecnologias Utilizadas
Backend
Django/Django REST Framework: Framework web para desenvolvimento rápido de APIs
PostgreSQL: Banco de dados relacional
Stripe: Processamento de pagamentos
Pandas/Scikit-learn: Algoritmos de recomendação
Frontend
React: Biblioteca para construção de interfaces
Material-UI: Componentes React com design responsivo
React Router: Navegação entre páginas
Axios: Cliente HTTP para requisições à API
JWT: Autenticação baseada em tokens
Infraestrutura
Docker: Contêinerização de serviços
Docker Compose: Orquestração de contêineres
Nginx: Servidor web para aplicação frontend
Funcionalidades Principais
Autenticação de usuários (cadastro, login, perfil)
Catálogo de produtos com busca e filtros
Recomendações personalizadas baseadas no comportamento do usuário
Carrinho de compras
Processamento de pagamentos com Stripe
Sistema de revisão e avaliação de produtos
Requisitos
Docker e Docker Compose
Python 3.10+
Node.js 20+
PostgreSQL