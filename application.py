import json

import boto3
from flask import Flask, render_template, request

application = Flask(__name__)


def conectar_dynamo():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('posts')
    return table


def scan():
    table = conectar_dynamo()

    response = table.scan()
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return data


def put_item(data):
    table = conectar_dynamo()

    table.put_item(
        Item={
            'id': data['id'],
            'content': data['content'],
            'title': data['title']
        }
    )
    return 'Concluido com sucesso!'


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/consultar', methods=['GET'])
def consultar():
    return json.dumps(scan(), default=str)


@application.route('/incluir', methods=['POST'])
def incluir():
    body = request.json
    res = put_item(body)
    return res


if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=False)
