# Introduction

Magic-BI is a fully automated Chat-BI tool based on AI, which uses a fine-tuned large model + intelligent body approach to achieve high accuracy and low reasoning cost. However, it requires model fine-tuning, which may have a higher usage 
threshold and additional costs. It is recommended to use an 8B+ open-source model for fine-tuning in expert mode.

In explorer mode, Magic-BI will automatically learn the corresponding data pattern. Magic-BI is open-sourced and can be deployed privately or semi-privately, which maximizes user privacy protection while lowering the usage threshold.

Currently supported data types include: SQL databases, text, images, and business systems.

** SQL Databases

For SQL-type data, Magic-BI supports three modes: beginner mode, expert mode, and explorer mode.

Beginner mode uses a universal large model + RAG + intelligent body approach, which has the advantage of low usage threshold but disadvantages of lower accuracy and higher reasoning cost. It is recommended to use a 70B+ or 400B+ 
open-source large model or other cloud services in beginner mode.

In explorer mode, Magic-BI will automatically learn the data pattern. The learning results can be used for both beginner mode and explorer mode. In explorer mode, it is recommended to use a 400B+ open-source large model or other cloud 
services.

** Text

For text-type data, Magic-BI uses a universal large model + RAG approach.

## Images
For image-type data, we use multi-modal RAG technology to parse and provide conversation services.

## Business Systems
For business system data, we use Agent technology to parse and provide conversation services.

Users can converse with one or multiple types of data simultaneously.

# Running Environment
Magic-BI can run on Ubuntu 22.04, RTX 4090, CUDA 12+, and PyTorch 2.0+. Other environments have not been strictly tested, but similar environments should also work. If you encounter any issues while using Magic-BI, please contact us 
through the following channels.

# Installation
Magic-BI supports two installation methods: Docker and source code compilation. We recommend using the Docker method for deployment.
## Docker
To deploy using Docker, install Docker on your system and enable GPU support. Execute the following two commands to complete the setup:
1. `cd $Magic-BI`
2. `docker compose -f deployment/docker-compose.yml up -d`

## Source Code Compilation
### Magic-BI
Enter the Magic-BI directory and execute the command `pip3 install -e .`

### Dependencies
Execute the following two commands to complete the setup:
1. `cd $Magic-BI`
2. `docker compose -f deployment/docker-compose.yml up -d`
`docker compose -f deployment/docker-compose-component.yml up -d`

# Client
Magic-BI supports two types of clients: WEB GUI and Restful API. If you want to use Magic-BI directly, access it through the web page; if you want to integrate Magic-BI into your system or use only part of its functionality, access it 
through the Restful API.
## WEB GUI
Execute the command `python3 -m magic_bi.main --config config/magic_bi.yml` to start the system. Access the system by entering `http://$url:6688` in your browser. Currently supported web browsers are Chrome and Firefox.
## Restful API
Execute the command `python3 -m magic_bi.main --config config/magic_bi.yml` to start the system. Use an API tool or another system to call Magic-BI. The API documentation can be found at xxx.

# Models
## Large Models
Currently, we mainly use large models (language and multi-modal) through OpenAI API-compatible methods, supporting general models and fine-tuned models. Text, images, and business systems currently use general large models; for SQL 
databases, fine-tuned models perform better than general large models.

The corresponding `base_url`, `model`, and `api_key` are configured in `config/magic_bi.yml`.
### General Large Models
Text, images, and business systems currently use general large models; for SQL databases, Magic-BI mainly provides Chat-BI services using RAG technology.
#### Local Large Models
Local large models can be deployed through ollama or vllm, providing services in an OpenAI API-compatible way.
#### Large Model Services
Almost all large model services provide services through the OpenAI API.
### Fine-tuned Large Models
Fine-tuned large models are currently mainly used for SQL databases. The fine-tuning method is detailed at xxx.

# Auxiliary Data
Auxiliary data is used to enhance Magic-BI's response effect. It comes in two forms: RAG and fine-tuned data.
## RAG Data
RAG data is added by users to help improve Magic-BI's response effect. Please refer to xxx for the specific addition method.
## Fine-tuned Data
Fine-tuned data is used to fine-tune language models, enhancing Magic-BI's response effect. The generation and fine-tuning methods can be found at xxx.