# analytics-api | API para processamento de dados

Basicamente, este projeto segue o seguinte fluxo:
 - Ingestão de dados: upload para o S3.
 - Processamento de dados: AWS Lambda processa os dados do CSV, sumariza e salva no PostgreSQL.
 - Notificação: AWS SNS envia uma notificação quando o upload é realizado.
 - Filas: AWS SQS gerencia as mensagens entre o Lambda e o PostgreSQL.
 - Armazenamento: RDS com PostgreSQL para armazenar os dados processados.

Localmente, utilizei o Localstack para simular alguns serviços, como S3, SNS e SQS.  
O PostgreSQL foi executado em um container Docker.

## Executando o projeto
Configure um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```dotenv
# Localstack
AWS_ACCESS_KEY_ID=000000000000000
AWS_SECRET_ACCESS_KEY=000000000000000
AWS_SESSION_TOKEN=000000000000000
AWS_REGION=us-east-1
ENDPOINT_URL=http://localhost:4566

# PostgreSQL
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/analytics
```
Suba o Localstack e o PostgreSQL com o comando:
```bash
docker-compose up -d
```
Com isso, o Localstack estará configurado, com os dois arquivos necessários, com base na pasta [#localstack/ready.d/.files](./localstack/ready.d/.files).

Execute o arquivo [#run.py](./run.py) para simular o handler local e importá-los para o banco de dados PostgreSQL.
```bash
python run.py --event-file ./events/sqs_put_s3.json
```

Execute a API com o comando:
```bash
uvicorn src.api.main:app --reload --port 8080
```
e acesse a API em [http://localhost:8080/docs](http://localhost:8080/docs) para testar as APIs.


### IaC - Terraform e AWS SAM
Utilizei duas ferramentas de IaC para criar alguns recursos na nuvem:
 - Terraform para criar o banco de dados S3, SNS, SQS e IAM (permissões).
 - AWS SAM para criar os recursos do Lambda.
Para criar os recursos, utilize o Terraform.
```bash
cd terraform
terraform init
terraform apply
```

### Testes
Utilizei pytest para criar testes unitários e de integração para a API.
Para executá-los:
```bash
pytest
```
Também incluí testes REST com Insomnia, que podem ser encontrados na pasta [#docs/](./docs/insomnia_rest.yaml).
Importe-os no Insomnia e execute os testes.


### Recursos utilizados
Para transparência, deixo aqui todas as referências utilizadas.
#### Artigos.
 - https://github.com/aws-samples/aws-lambda-hexagonal-architecture?tab=readme-ov-file
 - https://github.com/awslabs/aws-lambda-web-adapter/blob/main/examples/fastapi/tests/unit/test_handler.py
 - https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-concepts.html
 - https://stackoverflow.com/questions/45732459/retrieve-delimiter-infered-by-read-csv-in-pandas
 - https://docs.aws.amazon.com/sns/latest/dg/sns-sqs-as-subscriber.html
 - https://docs.localstack.cloud/getting-started/installation/#helm

#### LLMs.
 - https://chatgpt.com/share/683515b5-2588-800a-91e4-170a90dfae7b
 - https://g.co/gemini/share/f21f493c4bee
 - https://g.co/gemini/share/5e1ba674be93
