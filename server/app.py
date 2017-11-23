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

DEFAULT_STS = 100
DEFAULT_STT = 0
DEFAULT_N= 0

RESULT_SIZE = 5

@app.route("/")
async def root(request):
    return sanic_json({"bns root": "test"})


@app.route("/bns")
async def bns(request):

    # default
    data = {
        'behaviors' : {},
        'tendencies' : [],
        'neighbors' : {},
        'result' : {},
        'weights': {'shop_to_shop': DEFAULT_STS, 'shop_to_topic': DEFAULT_STT, 'neighbors': DEFAULT_N}
    }

    width = 761
    height = 500

    # Get Values from request
    if request.raw_args:
        """
        sample json
        {
            'behaviors': {'커피빈강남대로점': 10, '빈로이': 20},
            'tendencies': ['커피', '점심', '직장인', '저가'],
            'neighbors': {'커피빈강남대로점': ['봉피양', '빈로이', 'CJ올리브네트웍스역삼점']},
            'weights': {'shop_to_shop': 0.1, 'shop_to_topic': 0.3, 'neighbors': 0.6}
        }
        """
        data['behaviors'] = json.loads(request.raw_args.get('behaviors', '{}'))
        data['behaviors_json'] = json.dumps(data['behaviors'], ensure_ascii=False)
        data['tendencies'] = json.loads(request.raw_args.get('tendencies', '[]'))
        data['tendencies_json'] = json.dumps(data['tendencies'], ensure_ascii=False)
        data['neighbors'] = json.loads(request.raw_args.get('neighbors', '{}'))
        data['neighbors_json'] = json.dumps(data['neighbors'], ensure_ascii=False)

        shop_to_shop = int(request.raw_args.get('shop_to_shop', DEFAULT_STS))
        shop_to_topic = int(request.raw_args.get('shop_to_topic', DEFAULT_STT))
        neighbor_weight = int(request.raw_args.get('neighbor_weight', DEFAULT_N))

        if not data['behaviors'] and not data['tendencies'] and not data['neighbors']:
            shop_to_shop = 100
            shop_to_topic = 0
            neighbor_weight = 0
        else:
            shop_to_shop = 10
            shop_to_topic = 30
            neighbor_weight = 60


        data.update( {
            'weights': {'shop_to_shop': shop_to_shop, 'shop_to_topic': shop_to_topic, 'neighbors': neighbor_weight}
        } )


    # get results from recommendation module
    data['result'] = ri.recommend_processor(data)
    data['result']['shop'] = data['result']['shop'][0:RESULT_SIZE]
    data['result']['topic'] = data['result']['topic'][0:RESULT_SIZE]

    # generate iframe html from google fusion table
    fta = FusionTableAgent()
    behavior_key = [ behavior for behavior in data['behaviors'].keys() ]
    filter_key = behavior_key + data['tendencies']

    if not filter_key:
        filter_key=None

    if not behavior_key:
        behavior_key=None

    data['result']['integrated_network'] = fta.get_src(
        'integrated_network', width, height,
        filter_col='col0', filters=filter_key)

    data['result']['shop_to_shop_network'] = fta.get_src(
        'shop_to_shop', width, height,
        filter_col='col1', filters=behavior_key)

    data['result']['shop_to_topic_network'] = fta.get_src(
        'shop_to_topic', width, height,
        filter_col='col0', filters=behavior_key)

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
