from jinja2 import nodes, TemplateRuntimeError
from jinja2.ext import Extension

from edri.api.handlers import HTTPHandler
from edri.utility.function import format_url


class URLExtension(Extension):
    tags = {'url'}

    def parse(self, parser):
        # Parse the token and create a call to the _render_url method
        lineno = next(parser.stream).lineno

        # Parse the first argument, which is the endpoint name
        endpoint = parser.parse_expression()

        # Parse the optional keyword arguments
        args = [endpoint]
        kwargs = []
        while parser.stream.current.type != 'block_end':
            token = parser.stream.current
            if token.type == 'name' and parser.stream.look().type == 'assign':
                key = parser.stream.current.value
                parser.stream.skip()  # Skip over the key
                parser.stream.skip()  # Skip over the '='
                value = parser.parse_expression()
                kwargs.append(nodes.Keyword(key, value))
            else:
                args.append(parser.parse_expression())

        return nodes.Output([self.call_method('_render_url', args, kwargs)], lineno=lineno)

    @staticmethod
    def _render_url(endpoint, **kwargs):
        event_type = HTTPHandler.event_type_names().get(endpoint)
        try:
            extensions = HTTPHandler.event_type_extensions()[event_type]
        except KeyError:
            raise TemplateRuntimeError("Event %s was not found" % endpoint)
        if "url_original" in extensions:
            try:
                formated_url = format_url(extensions["url_original"], **kwargs)
            except KeyError as e:
                raise TemplateRuntimeError(str(e))
            return formated_url
        else:
            try:
                return extensions["url"]
            except KeyError:
                raise TemplateRuntimeError("Event %s was not found" % endpoint)
