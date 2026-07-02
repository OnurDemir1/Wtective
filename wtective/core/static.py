import httpx
from bs4 import BeautifulSoup, Comment
from urllib.parse import urljoin
from typing import List, Optional


class StaticAnalyzer:
    def __init__(self, target_url: str, transport=None):
        self.target_url = target_url
        self.ua = (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/125.0.0.0 Safari/537.36'
        )
        self.client = httpx.Client(
            verify=False, timeout=20.0,
            headers={'User-Agent': self.ua},
            follow_redirects=True,
            transport=transport,
        )

        self.html = ""
        self.soup = None
        self.response_headers = {}
        self.cookies = {}
        self.scripts = []
        self.script_contents = {}
        self.stylesheets = []
        self.stylesheet_contents = {}
        self.meta_tags = []
        self.robots_txt = ""
        self.sitemap_xml = ""
        self.has_wasm = False
        self.has_source_maps = False
        self.sw_content = ""

    def fetch(self) -> bool:
        try:
            resp = self.client.get(self.target_url)
            self.html = resp.text
            self.response_headers = resp.headers
            self.cookies = resp.cookies
            self.soup = BeautifulSoup(self.html, 'html.parser')

            self.scripts = [urljoin(self.target_url, s.get('src')) for s in self.soup.find_all('script') if s.get('src')]
            self.stylesheets = [urljoin(self.target_url, l.get('href')) for l in self.soup.find_all('link', rel='stylesheet') if l.get('href')]
            self.meta_tags = self.soup.find_all('meta')

            self._fetch_robots()
            self._fetch_sitemap()
            self._fetch_script_contents()
            self._fetch_stylesheet_contents()
            self._check_wasm()
            self._check_source_maps()
            self._fetch_service_worker()
            return True
        except Exception:
            return False

    def _fetch_robots(self):
        try:
            r = self.client.get(urljoin(self.target_url, '/robots.txt'))
            if r.status_code == 200 and 'text' in r.headers.get('content-type', ''):
                self.robots_txt = r.text
        except Exception:
            pass

    def _fetch_sitemap(self):
        try:
            r = self.client.get(urljoin(self.target_url, '/sitemap.xml'))
            if r.status_code == 200:
                self.sitemap_xml = r.text[:50000]
        except Exception:
            pass

    def _fetch_stylesheet_contents(self):
        for href in self.stylesheets[:12]:
            try:
                r = self.client.get(href)
                if r.status_code == 200:
                    self.stylesheet_contents[href] = r.text[:120000]
            except Exception:
                pass

    def _fetch_script_contents(self):
        for src in self.scripts[:20]:
            if not any(name in src.lower() for name in ('bootstrap', 'jquery', 'react', 'vue', 'angular')):
                continue
            try:
                r = self.client.get(src)
                if r.status_code == 200:
                    self.script_contents[src] = r.text[:80000]
            except Exception:
                pass

    def _check_wasm(self):
        self.has_wasm = '.wasm' in self.html or 'application/wasm' in self.html

    def _check_source_maps(self):
        for script in self.scripts[:5]:
            try:
                r = self.client.get(script + '.map')
                if r.status_code == 200 and '"sources"' in r.text[:200]:
                    self.has_source_maps = True
                    return
            except Exception:
                pass

    def _fetch_service_worker(self):
        for path in ['/sw.js', '/service-worker.js']:
            try:
                r = self.client.get(urljoin(self.target_url, path))
                if r.status_code == 200 and ('self.addEventListener' in r.text or 'serviceWorker' in r.text):
                    self.sw_content = r.text
                    return
            except Exception:
                pass

    def get_favicon_hash(self) -> Optional[int]:
        from ..utils.hashing import get_favicon_hash
        favicon_url = None
        if self.soup:
            icon = self.soup.find('link', rel=lambda x: x and 'icon' in str(x).lower())
            if icon and icon.get('href'):
                favicon_url = icon['href']
        if not favicon_url:
            favicon_url = '/favicon.ico'
        if not favicon_url.startswith('http'):
            favicon_url = urljoin(self.target_url, favicon_url)
        try:
            r = self.client.get(favicon_url)
            if r.status_code == 200:
                return get_favicon_hash(r.content)
        except Exception:
            pass
        return None

    def get_comments(self) -> List[str]:
        if not self.soup:
            return []
        return [str(c) for c in self.soup.find_all(string=lambda t: isinstance(t, Comment))]

    def get_all_classes(self) -> List[str]:
        classes = set()
        if self.soup:
            for tag in self.soup.find_all(True):
                cls = tag.get('class')
                if cls:
                    classes.update(cls)
        return list(classes)

    def get_all_attrs(self) -> List[str]:
        attrs = set()
        if self.soup:
            for tag in self.soup.find_all(True):
                attrs.update(tag.attrs.keys())
        return list(attrs)

    def get_inline_scripts(self) -> List[str]:
        if not self.soup:
            return []
        return [s.string for s in self.soup.find_all('script') if s.string and len(s.string) > 10]

    def close(self):
        self.client.close()

