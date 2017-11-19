import sys

from sanic import Sanic
from sanic.response import json, html

from jinja2 import Environment, PackageLoader, select_autoescape

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


@app.route("/")
async def root(request):
    return json({"bns root": "test"})


@app.route("/bns")
async def bns(request):

    # default
    data = {
        'query' : '',
        'range1' : 50,
        'range2' : 50,
        'range3' : 50
    }

    # Get Values from request
    if request.raw_args:
        data['query'] = request.raw_args['query']
        data['range1'] = int(request.raw_args['relation'])
        data['range2'] = int(request.raw_args['attribute'])
        data['range3'] = int(request.raw_args['following'])


    # get results from recommendation module

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
