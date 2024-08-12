from fastapi import Request, Response
from fastapi.responses import JSONResponse
from accept_types import get_best_match
from fastapi.templating import Jinja2Templates
import jinja2
from pydantic import BaseModel
from typing import Mapping


class HTMXResponse(Response):
    def __init__(
        self,
        request: Request,
        directory: str,
        template: str,
        content: BaseModel | dict | None = None,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
    ) -> None:
        self.directory = directory
        self.template = template
        self.content = content
        self.request = request
        super().__init__(content, status_code, headers, media_type, None)

    def render(self, _) -> bytes:
        accept = self.request.headers.get('accept')
        return_type = get_best_match(
            accept, ['text/html', 'application/json']
        )

        if return_type == 'text/html':
            self.media_type = 'text/html'
            if 'template_dirs' in self.request.state.context:
                self.request.state.context['template_dirs'].append(self.directory)
                template_dirs = self.request.state.context['template_dirs']
            else:
                template_dirs = [self.directory]
            env = jinja2.Environment(
                loader=jinja2.ChoiceLoader([jinja2.FileSystemLoader(dir) for dir in template_dirs])
            )
            templates = Jinja2Templates(env=env)
            #templates = Jinja2Templates(directory=self.directory)

            # NOTE: you can add extra parameters to the request.state
            # to be rendered in your jinja template
            context = {'request': self.request}
            
            if getattr(self.request.state, "context"):
                context = {**context, **self.request.state.context}
            context['model'] = self.content

            if isinstance(self.request.state.template_filters, dict):
                for key, value in self.request.state.template_filters.items():
                    templates.env.filters[key] = value
            return templates.TemplateResponse(
                self.template,
                context,
                status_code=self.status_code
            ).body
        elif return_type == 'application/json':
            self.media_type = 'application/json'
            if isinstance(self.content, BaseModel):
                data = self.content.model_dump(mode='json')
            elif self.content is None:
                data = {}
            else:
                data = self.content

            return JSONResponse(data).body