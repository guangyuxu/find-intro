# Find Intro Opportunities

## Architecture
https://lucid.app/lucidchart/c78284cb-46c7-4d89-a066-67c386c36b00/edit?viewport_loc=-253%2C-479%2C2514%2C1401%2C0_0&invitationId=inv_1af5f79d-8c3e-41c5-b855-d2b28a0b532f

## Policy
1. Search matched companies
(1). extract company ICP to structured data
(2). Vectorize Search + LLM Match/Rerank

2. Pre extract function and seniority of connection job title


## Assumeption
* Conflict of company names, dealing manually, to be enhanced based on the real case



## Install in Kubernetes 

### 1. Install Kubernetes Cluster or Minikube at pc
https://kubernetes.io/

### 2. Install helm
https://helm.sh/

### 3. OPENAI_API
* OPENAI_API_KEY: madatory
* OPENAI_API_BASE: Optioinal

### 4. Jupyter lab
Make sure you have installed Jupyter lab at your local

### 5. Install Mysql POD
* Install
```shell
cd find-intro/deployment/kubernetes
kubectl apply -f mysql

kubectl get pods | grep mysql
kubectl exec -it mysql-6d7f5d5944-kqwvx -- /bin/bash
mysql -p
input password
partnerhq
CREATE USER 'findintro'@'%' IDENTIFIED BY 'findintro';
CREATE DATABASE findintro;
GRANT ALL PRIVILEGES ON *.* TO 'findintro'@'%' WITH GRANT OPTION;
exit
exit
```
* Validation
```shell
kubectl port-forward service/mysql 3306:3306
# verify the database setup
mysql -h 127.0.0.1 -P 3306 -u findintro -pfindintro findintro
```
### 6. Data Pipeline
Setence transformer data from MySQL to Qdrant
1. pip install pymysql pandas numpy sqlalchemy
2. start jupyter lab in find-intro/script
3. run loaddata.ipynb step by step


### 7. Install Vector DB, Qdrant
https://qdrant.tech/documentation/quick-start/
* Install
```shell
cd find-intro/deployment/kubernetes
kubectl apply -f qdrant
```
* Validation
```shell
kubectl port-forward service/qdrant 6333:6333
curl localhost:6333/collections
> {"result":{"collections":[]},"status":"ok","time":0.000021125}%
```

* REST API: localhost:6333
* Web UI: localhost:6333/dashboard
* GRPC API: localhost:6334

### 8. Create vector collection
* Create
```shell
curl -X PUT http://localhost:6333/collections/companies \
     -H "Content-Type: application/json" \
     -d '{
            "vectors": {
                "size": 384,
                "distance": "Cosine"
            }
        }'
```
* Validation
```shell
curl http://localhost:6333/collections/companies
```

### 9. Build & Run Service POD
PORT: 8080
* Build
```shell
cd find-intro/find-intro-service
docker buildx build --platform linux/amd64,linux/arm64 -t guangyuxu/find-intro-service --push .
```
* Deploy
```shell
# NOTE: export the openapo api key first, and replace the key in find-intro-service.yaml
cd find-intro/deployment/kubernetes/find-intro-service
export OPENAI_API_KEY="my_value"
# Specific the alternative proxy openai host
export OPENAI_API_BASE="alternative openai host" 
envsubst < find-intro-service.yaml > find-intro-service-instance.yaml
kubectl apply -f find-intro-service-instance.yaml
rm find-intro-service-instance.yaml
```
* Verification
```shell
kubectl port-forward service/find-intro-service 8080:8080
```
### 10. Pipeline -> Sentence Transformer to Vector
This process may tons of minutes and depends on your pc setup
Call the API to transform all the data from MySQL into Qdrant
[PUT]http://127.0.0.1:8080/api/v1/load-all

## Search
[POST] http://localhost:8080/api/company/search
```json
{
    "limit":  10,
    "company_name":  "NewsCatcher",
    "job_titles":  "VP/Head/Manager of Product, Founder, CEO/CTO, VP/ Head of Engineering",
    "company_description":  "A generative AI company willing to spend $50,000+/year on structured real-time news data, Based in the US is preferred, 10+ employees"
}
```
