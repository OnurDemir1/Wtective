import httpx

from wtective.core.scanner import Scanner
from wtective.core.static import StaticAnalyzer


class FakeNet:
    """Stand-in for NetworkAnalyzer so tests never touch DNS or TLS."""

    def __init__(self, dns=None, ssl=None):
        self._dns = dns or {}
        self._ssl = ssl or {}

    def check_dns(self):
        return self._dns

    def check_ssl(self):
        return self._ssl


class Result:
    """Flattened scan result with helpers for assertions."""

    def __init__(self, results):
        self.raw = results
        self.by_name = {}
        for techs in results.values():
            for t in techs:
                self.by_name.setdefault(t['name'], t)

    def has(self, name):
        return name in self.by_name

    def confidence(self, name):
        return self.by_name[name]['confidence']

    def version(self, name):
        return self.by_name.get(name, {}).get('version')

    def names(self):
        return set(self.by_name)


def _transport(pages):
    def handler(request):
        page = pages.get(request.url.path)
        if page is None:
            return httpx.Response(404, text='not found')
        if isinstance(page, str):
            page = {'body': page}
        return httpx.Response(
            page.get('status', 200),
            headers=dict(page.get('headers', {})),
            text=page.get('body', ''),
        )

    return httpx.MockTransport(handler)


def _failing_transport():
    def handler(request):
        raise httpx.ConnectError('unreachable', request=request)

    return httpx.MockTransport(handler)


def scan(html='', headers=None, pages=None, dns=None, ssl=None,
         url='https://example.com/', fail=False):
    if fail:
        transport = _failing_transport()
    else:
        merged = {'/': {
            'headers': {'content-type': 'text/html; charset=utf-8', **(headers or {})},
            'body': html,
        }}
        if pages:
            merged.update(pages)
        transport = _transport(merged)

    static = StaticAnalyzer(url, transport=transport)
    scanner = Scanner(url)
    return Result(scanner.run(static=static, net=FakeNet(dns=dns, ssl=ssl)))
