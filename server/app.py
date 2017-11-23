import sys

from sanic import Sanic
from sanic.response import json as sanic_json, html
import json

from jinja2 import Environment, PackageLoader, select_autoescape

from recommendation import RecommendIndex

env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml', 'tpl']),
    enable_async=True
)


async def get_template(tpl, **kwargs):
    template = env.get_template(tpl)
    content = await template.render_async(kwargs)
    return html(content)

app = Sanic(__name__)
app.static('/static', './static')

ri = RecommendIndex()
ri_main_path = '../data'

import os
path = os.getcwd()

ri.index(
    '../data/shop_to_shop.csv',
    '../data/shop_to_topic.csv'
)



@app.route("/")
async def root(request):
    return sanic_json({"bns root": "test"})


@app.route("/bns")
async def bns(request):

    # default
    data = {
        'query' : '',
        'result' : {},
        'weights': {'shop_to_shop': 10, 'shop_to_topic': 30, 'neighbors': 60}
    }

    # Get Values from request
    if request.raw_args:
        data['query'] = request.raw_args['query']
        shop_to_shop = int(request.raw_args['shop_to_shop'])
        shop_to_topic = int(request.raw_args['shop_to_topic'])
        neighbors = int(request.raw_args['neighbors'])

        data.update(json.loads(data['query']))
        data.update( {
            'weights': {'shop_to_shop': shop_to_shop, 'shop_to_topic': shop_to_topic, 'neighbors': neighbors}
        } )


    # get results from recommendation module
    data['result'] = ri.recommend_processor(data)

    # data reorganization
    data['result']['shopname_list'] = [ shop_unit[0] for shop_unit in data['result']['shop'] ]
    data['result']['shopweight_list'] = [ shop_unit[1] for shop_unit in data['result']['shop'] ]

    data['result']['topic_list'] = [ {'name':topic_unit[0], 'y':topic_unit[1]} for topic_unit in data['result']['topic'] ]

    # generate template from result data
    content = await get_template('bns.html', **data)
    return content


@app.route("/report")
async def report(request):

    # Get Values from request

    data = {
        'query' : ''
    }

    # get results from recommendation module

    # generate template from result data
    content = await get_template('test.template.html', **data)
    return content

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    app.run(port=port)
