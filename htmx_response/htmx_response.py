from fastapi import Request, Response
from fastapi.routing import APIRoute
from typing import Callable
from accept_types import get_best_match
from fastapi.templating import Jinja2Templates

import jinja2
import json

def get_htmx_route(
        base_dir: str,
        base_template: str,
):
    class HTMXRoute(APIRoute):
        def get_route_handler(self) -> Callable:
            original_route_handler = super().get_route_handler()

            async def custom_route_handler(request: Request) -> Response:
                return_type = get_best_match(
                    request.headers.get('accept', 'text/html'), ['text/html', 'application/json']
                )

                response: Response = await original_route_handler(request)
                if return_type == 'text/html' and 'htmx-template' in response.headers:
                    env = jinja2.Environment(
                        loader=jinja2.ChoiceLoader([jinja2.FileSystemLoader(base_dir)])
                    )
                    templates = Jinja2Templates(env=env)
                    #templates = Jinja2Templates(directory=template_dirs)
                    layout = templates.env.get_template(base_template)
                    context = json.loads(response.body.decode('utf-8'))
                    context['request'] = request
                    context['layout'] = layout
                    return templates.TemplateResponse(
                        response.headers.get('htmx-template'),
                        context=context
                    )
                return response

            return custom_route_handler
    return HTMXRoute