import sys

from sanic import Sanic
from sanic.response import json as sanic_json, html
import json

from jinja2 import Environment, PackageLoader, select_autoescape

from recommendation import RecommendIndex
from util import FusionTableAgent

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

DEFAULT_STS = 10
DEFAULT_STT = 30
DEFAULT_N= 60
RESULT_SIZE = 10

@app.route("/")
async def root(request):
    return sanic_json({"bns root": "test"})


@app.route("/bns")
async def bns(request):

    # default
    data = {
        'query' : '',
        'result' : {},
        'weights': {'shop_to_shop': DEFAULT_STS, 'shop_to_topic': DEFAULT_STT, 'neighbors': DEFAULT_N}
    }

    width = 761
    height = 500

    # Get Values from request
    if request.raw_args:
        data['query'] = request.raw_args.get('query', '{}')
        shop_to_shop = int(request.raw_args.get('shop_to_shop', DEFAULT_STS))
        shop_to_topic = int(request.raw_args.get('shop_to_topic', DEFAULT_STT))
        neighbors = int(request.raw_args.get('neighbors', DEFAULT_N))

        data['query_json'] = json.loads(data['query'])
        data.update(json.loads(data['query']))
        data.update( {
            'weights': {'shop_to_shop': shop_to_shop, 'shop_to_topic': shop_to_topic, 'neighbors': neighbors}
        } )


    # get results from recommendation module
    data['result'] = ri.recommend_processor(data)
    data['result']['shop'] = data['result']['shop'][0:RESULT_SIZE]
    data['result']['topic'] = data['result']['topic'][0:RESULT_SIZE]

    # generate iframe html from google fusion table
    fta = FusionTableAgent()
    filter_key = [ x for x in data['query_json']['behaviors'].keys() ]
    filter_key.extend(data['query_json']['tendencies'])

    data['result']['network'] = fta.get_src(
        'integrated_network', width, height,
        filter_col='col0', filters=filter_key)

    data['result']['shop_location'] = fta.get_src('shop_location', width, height)

    # data reorganization
    #data['result']['shopname_list'] = [ shop_unit[0] for shop_unit in data['result']['shop'] ]
    data['result']['shopname_list'] = json.dumps([ shop_unit[0] for shop_unit in data['result']['shop'] ])
    data['result']['shopweight_list'] = [ shop_unit[1] for shop_unit in data['result']['shop'] ]

    data['result']['topic_list'] = json.dumps([ {'name':topic_unit[0], 'y':topic_unit[1]} for topic_unit in data['result']['topic'] ])

    #

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
