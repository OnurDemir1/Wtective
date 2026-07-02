import re
from urllib.parse import urlparse, urlunparse
from .static import StaticAnalyzer
from .network import NetworkAnalyzer
from .fingerprints.rules import RULES

DEFINITIVE_HEADERS = {
    'x-vercel-id', 'x-nf-request-id', 'x-amz-request-id',
    'x-azure-ref', 'x-ms-request-id', 'fly-request-id',
    'x-aspnet-version', 'x-aspnetmvc-version',
    'x-cloud-trace-context', 'cf-mitigated',
}

CDN_DOMAINS = {
    'fonts.googleapis.com': ('Font Service', 'Google Fonts'),
    'fonts.gstatic.com': ('Font Service', 'Google Fonts'),
    'use.typekit.net': ('Font Service', 'Adobe Fonts'),
    'cdnjs.cloudflare.com': ('CDN', 'cdnjs'),
    'unpkg.com': ('CDN', 'unpkg'),
    'cdn.jsdelivr.net': ('CDN', 'jsDelivr'),
    'ajax.googleapis.com': ('CDN', 'Google Hosted Libraries'),
}

CONFIDENCE_ORDER = {"Confirmed": 3, "Likely": 2, "Suspected": 1}

# JS identifiers that are far too common to trust as a technology signal when
# they only appear as a locally declared variable (var/const/let). They are
# only accepted when assigned as a real global (window./self.) or corroborated
# by another signal such as a script URL.
AMBIGUOUS_GLOBALS = {
    'analytics', 'heap', 'chart', 'marked', 'paper', 'ace', 'google',
    'drift', 'moment', 'tone', 'howl', 'konva', 'matter', 'fabric',
    'quill', 'sortable', 'masonry', 'isotope', 'pace', 'typed', 'velocity',
    'cropper', 'dropzone', 'io', 'ga', 'hj', 'ym', 'fs', 'fb', 'ze', 'ol',
    'dy', 'em', 'ky',
}


class Finding:
    __slots__ = ('category', 'name', 'confidence', 'evidences', 'version')

    def __init__(self, category, name, confidence, evidence, version=None):
        self.category = category
        self.name = name
        self.confidence = confidence
        self.evidences = [evidence]
        self.version = version

    def upgrade(self, new_confidence, evidence, version=None):
        if CONFIDENCE_ORDER.get(new_confidence, 0) > CONFIDENCE_ORDER.get(self.confidence, 0):
            self.confidence = new_confidence
        if evidence not in self.evidences:
            self.evidences.append(evidence)
        if version and not self.version:
            self.version = version


class Scanner:
    def __init__(self, target_url: str):
        self.target_url = self._normalize_url(target_url)
        self.findings = {}

    @staticmethod
    def _normalize_url(target_url: str) -> str:
        target_url = (target_url or '').strip()
        if not target_url:
            return target_url
        if '://' not in target_url:
            target_url = 'https://' + target_url
        parsed = urlparse(target_url)
        if not parsed.netloc and parsed.path:
            parsed = urlparse('https://' + parsed.path)
        path = parsed.path or '/'
        return urlunparse((parsed.scheme or 'https', parsed.netloc.lower(), path, '', parsed.query, ''))

    @staticmethod
    def _extract_js_globals(inline_scripts: list):
        """Return (window_globals, declared_names).

        window_globals are identifiers assigned onto the global object
        (window./self.) — a strong, trustworthy signal. declared_names are
        plain var/const/let locals, which are weak and only usable for
        distinctive names.
        """
        window_globals = set()
        declared = set()
        combined = '\n'.join(s for s in inline_scripts if s)
        if not combined:
            return window_globals, declared
        for m in re.finditer(r'(?:window|self)\.([A-Za-z_$][\w$]*)\s*[=\[]', combined):
            window_globals.add(m.group(1))
        for m in re.finditer(r'\b(?:var|const|let)\s+([A-Za-z_$][\w$]*)\s*=', combined):
            declared.add(m.group(1))
        return window_globals, declared

    @staticmethod
    def _is_ambiguous_global(name: str) -> bool:
        return len(name) <= 2 or name.lower() in AMBIGUOUS_GLOBALS

    def _add(self, category, name, confidence, evidence, version=None):
        key = f"{category}::{name}"
        if key in self.findings:
            self.findings[key].upgrade(confidence, evidence, version)
        else:
            self.findings[key] = Finding(category, name, confidence, evidence, version)

    def run(self, static=None, net=None):
        if static is None:
            static = StaticAnalyzer(self.target_url)
        if not static.fetch():
            static.close()
            return self._build_results()

        comments = static.get_comments()
        classes = static.get_all_classes()
        attrs = static.get_all_attrs()
        inline_scripts = static.get_inline_scripts()
        static.close()

        window_globals, declared_names = self._extract_js_globals(inline_scripts)
        js_all = window_globals | declared_names

        if net is None:
            net = NetworkAnalyzer(self.target_url)
        dns_records = net.check_dns()
        ssl_info = net.check_ssl()

        self._match_rules(static, window_globals, declared_names, comments, classes, attrs)
        self._infrastructure_checks(ssl_info, dns_records, static)
        self._heuristic_detection(static, js_all, inline_scripts)
        self._apply_versions(static)
        self._cross_validate()

        return self._build_results()

    def _match_rules(self, static, window_globals, declared_names, comments, classes, attrs):
        for category, techs in RULES.items():
            for tech, conds in techs.items():

                if 'headers' in conds:
                    for h_name, h_re in conds['headers'].items():
                        for k, v in static.response_headers.items():
                            if k.lower() == h_name.lower() and h_re.search(v):
                                conf = 'Confirmed' if k.lower() in DEFINITIVE_HEADERS else 'Likely'
                                self._add(category, tech, conf, f"Header {k}")

                if 'cookies' in conds:
                    for c_re in conds['cookies']:
                        for name in static.cookies.keys():
                            if c_re.search(name):
                                self._add(category, tech, 'Likely', f"Cookie {name}")

                if 'meta_generators' in conds:
                    for meta in static.meta_tags:
                        if meta.get('name', '').lower() == 'generator':
                            content = meta.get('content', '')
                            for g_re in conds['meta_generators']:
                                if g_re.search(content):
                                    self._add(category, tech, 'Confirmed', f"Meta Generator: {content}")

                if 'js_globals' in conds:
                    for g in conds['js_globals']:
                        key = g.replace('window.', '')
                        if key in window_globals:
                            self._add(category, tech, 'Confirmed', f"JS Global: {key}")
                        elif key in declared_names and not self._is_ambiguous_global(key):
                            self._add(category, tech, 'Likely', f"JS Global: {key}")

                if 'script_paths' in conds:
                    all_scripts = static.scripts + static.stylesheets
                    for p_re in conds['script_paths']:
                        for src in all_scripts:
                            if p_re.search(src):
                                self._add(category, tech, 'Likely', f"Script: {self._short(src)}")
                                break

                if 'url_paths' in conds:
                    target_domain = urlparse(self.target_url).netloc
                    candidate_urls = [self.target_url] + [
                        u for u in static.scripts + static.stylesheets
                        if target_domain in urlparse(u).netloc
                    ]
                    for p_re in conds['url_paths']:
                        for url in candidate_urls:
                            if p_re.search(url):
                                self._add(category, tech, 'Suspected', f"URL Path match")
                                break

                if 'html_attrs' in conds:
                    for a_re in conds['html_attrs']:
                        if a_re.search(static.html):
                            self._add(category, tech, 'Likely', f"HTML Attribute")
                            break

                if 'css_classes' in conds:
                    cls_str = ' '.join(classes)
                    for c_re in conds['css_classes']:
                        if c_re.search(cls_str):
                            self._add(category, tech, 'Suspected', f"CSS Class pattern")
                            break

                if 'html_comments' in conds:
                    for c_re in conds['html_comments']:
                        for comment in comments:
                            if c_re.search(comment):
                                self._add(category, tech, 'Suspected', f"HTML Comment")
                                break

    def _infrastructure_checks(self, ssl_info, dns_records, static):
        issuer = ssl_info.get('issuer', '')
        if 'Cloudflare' in issuer:
            self._add('CDN/WAF', 'Cloudflare', 'Confirmed', f"SSL Issuer: {issuer}")
        if "Let's Encrypt" in issuer:
            self._add('Certificate', "Let's Encrypt", 'Confirmed', f"SSL Issuer: {issuer}")
        if 'DigiCert' in issuer:
            self._add('Certificate', 'DigiCert', 'Confirmed', f"SSL Issuer: {issuer}")
        if 'Sectigo' in issuer or 'Comodo' in issuer:
            self._add('Certificate', 'Sectigo', 'Confirmed', f"SSL Issuer: {issuer}")

        for cname in dns_records.get('CNAME', []):
            cl = cname.lower()
            if 'vercel' in cl:
                self._add('PaaS/Hosting', 'Vercel', 'Confirmed', f"CNAME: {cname}")
            elif 'netlify' in cl:
                self._add('PaaS/Hosting', 'Netlify', 'Confirmed', f"CNAME: {cname}")
            elif 'herokuapp' in cl:
                self._add('PaaS/Hosting', 'Heroku', 'Confirmed', f"CNAME: {cname}")
            elif 'github.io' in cl:
                self._add('PaaS/Hosting', 'GitHub Pages', 'Confirmed', f"CNAME: {cname}")
            elif 'cloudfront' in cl:
                self._add('CDN', 'CloudFront', 'Confirmed', f"CNAME: {cname}")

        hl = {k.lower(): v for k, v in static.response_headers.items()}
        if 'cf-ray' in hl:
            self._add('CDN/WAF', 'Cloudflare', 'Confirmed', 'CF-RAY header')
        if 'cloudflare' in hl.get('server', '').lower():
            self._add('CDN/WAF', 'Cloudflare', 'Confirmed', 'Server: cloudflare')
        if 'content-security-policy' in hl:
            self._add('Security', 'CSP', 'Confirmed', 'Header present')
        if 'strict-transport-security' in hl:
            self._add('Security', 'HSTS', 'Confirmed', 'Header present')
        if 'x-frame-options' in hl:
            self._add('Security', 'X-Frame-Options', 'Likely', 'Header present')
        if 'x-content-type-options' in hl:
            self._add('Security', 'X-Content-Type-Options', 'Likely', 'Header present')
        if 'permissions-policy' in hl:
            self._add('Security', 'Permissions-Policy', 'Likely', 'Header present')

        if 'wp-admin' in static.robots_txt or 'wp-includes' in static.robots_txt:
            self._add('CMS', 'WordPress', 'Likely', 'robots.txt paths')

        if 'yoast' in static.sitemap_xml.lower():
            self._add('SEO Plugin', 'Yoast SEO', 'Confirmed', 'Sitemap generator')
            self._add('CMS', 'WordPress', 'Confirmed', 'Yoast implies WordPress')

        if static.has_wasm:
            self._add('Web Standard', 'WebAssembly', 'Confirmed', 'WASM reference detected')

        if static.has_source_maps:
            self._add('Security Risk', 'Exposed Source Maps', 'Confirmed', '.js.map accessible')

        if static.sw_content:
            self._add('Architecture', 'Service Worker', 'Confirmed', 'sw.js found')
            self._add('Miscellaneous', 'PWA', 'Likely', 'Service Worker present')
            if 'workbox' in static.sw_content.lower():
                self._add('JS Library', 'Workbox', 'Confirmed', 'Referenced in SW')

        for src in static.scripts + static.stylesheets:
            for domain, (cat, name) in CDN_DOMAINS.items():
                if domain in src:
                    self._add(cat, name, 'Confirmed', f"Loaded from {domain}")

    def _heuristic_detection(self, static, js_globals, inline_scripts):
        all_scripts_text = ' '.join(inline_scripts) if inline_scripts else ''
        html_lower = static.html.lower()
        robots_lower = static.robots_txt.lower()
        sitemap_lower = static.sitemap_xml.lower()

        if re.search(r'__NEXT_DATA__|/_next/static', static.html):
            self._add('Web Framework', 'Next.js', 'Confirmed', 'Page source pattern')
            self._add('Web Framework', 'React', 'Likely', 'Bundled with Next.js')

        if re.search(r'__NUXT__|/_nuxt/', static.html):
            self._add('Web Framework', 'Nuxt.js', 'Confirmed', 'Page source pattern')
            self._add('Web Framework', 'Vue.js', 'Likely', 'Bundled with Nuxt.js')
            self._add('Build Tool', 'Vite', 'Likely', 'Bundled with Nuxt.js')

        if re.search(r'/_astro/[^"\'>\s]+\.[A-Za-z0-9]{6,}\.(js|css)', static.html, re.I):
            self._add('Web Framework', 'Astro', 'Confirmed', 'Astro hashed asset pattern')

        if re.search(r'/_app/immutable/', static.html):
            self._add('Web Framework', 'SvelteKit', 'Confirmed', 'SvelteKit immutable assets')
            self._add('Web Framework', 'Svelte', 'Confirmed', 'Bundled with SvelteKit')
            self._add('Build Tool', 'Vite', 'Likely', 'Bundled with SvelteKit')

        if re.search(r'__remixContext|__remixManifest|/__remix-hmr', static.html):
            self._add('Web Framework', 'Remix', 'Confirmed', 'Remix source pattern')
            self._add('Web Framework', 'React', 'Likely', 'Bundled with Remix')

        if re.search(r'data-v-[a-f0-9]{6,}', static.html):
            self._add('Web Framework', 'Vue.js', 'Likely', 'Scoped style attributes')

        if re.search(r'_ngcontent-|_nghost-', static.html):
            self._add('Web Framework', 'Angular', 'Confirmed', 'Angular encapsulation attrs')

        if re.search(r'svelte-[a-z0-9]{5,}', static.html):
            self._add('Web Framework', 'Svelte', 'Likely', 'Svelte component classes')

        if re.search(r'wp-content/plugins/woocommerce|wc-cart-fragments|wc-ajax=', html_lower):
            self._add('E-commerce', 'WooCommerce', 'Confirmed', 'WooCommerce source pattern')
            self._add('CMS', 'WordPress', 'Confirmed', 'WooCommerce implies WordPress')

        if re.search(r'/skin/frontend/|/static/frontend/[A-Z]\w+/\w+/|mage/cookies|mage-cache|x-magento-|magento_version', html_lower):
            self._add('E-commerce', 'Magento', 'Confirmed', 'Magento source pattern')

        if re.search(r'cdn\.shopify\.com|shopify-section|shopify-features|window\.shopify|myshopify\.com', html_lower):
            self._add('E-commerce', 'Shopify', 'Confirmed', 'Shopify source pattern')

        if re.search(r'prestashop|/modules/(?:ps_|prestashop)', html_lower):
            self._add('E-commerce', 'PrestaShop', 'Confirmed', 'PrestaShop source pattern')

        if re.search(r'catalog/view/theme|index\.php\?route=product|route=checkout/cart', html_lower):
            self._add('E-commerce', 'OpenCart', 'Likely', 'OpenCart source pattern')

        if 'wp-content' in robots_lower or 'wp-json' in sitemap_lower:
            self._add('CMS', 'WordPress', 'Likely', 'WordPress robots/sitemap pattern')

        if re.search(r'core-js(?:@|/|-|\.)|/core-js/', html_lower):
            self._add('JS Library', 'core-js', 'Likely', 'core-js source pattern')

        db_patterns = {
            'MySQL': r'(sqlstate\[hy000\]|mysql server version for the right syntax|you have an error in your sql syntax|mysqli?_(?:query|connect|error)|mysql_fetch)',
            'MariaDB': r'(mariadb server version|mariadb\.org)',
            'PostgreSQL': r'(pg_query\(|pg_connect\(|psql:/|postgresql error|unterminated quoted string at or near)',
            'MongoDB': r'(mongooseerror|mongoerror|mongoclient)',
            'Redis': r'(redisexception|redis connection refused)',
            'SQLite': r'(sqlite3?\.(?:OperationalError|IntegrityError)|unable to open database file)',
        }
        error_text = (html_lower + ' ' + all_scripts_text.lower())[:200000]
        for db_name, pattern in db_patterns.items():
            if re.search(pattern, error_text):
                self._add('Database', db_name, 'Likely', 'Backend error/source signature')

        for script_src in static.scripts:
            src_lower = script_src.lower()
            if 'wp-content' in src_lower or 'wp-includes' in src_lower:
                self._add('CMS', 'WordPress', 'Confirmed', 'WP asset paths')
            if 'cdn.shopify.com' in src_lower:
                self._add('E-commerce', 'Shopify', 'Confirmed', 'Shopify CDN')
            if 'static.wixstatic.com' in src_lower or 'parastorage.com' in src_lower:
                self._add('CMS', 'Wix', 'Confirmed', 'Wix CDN')
            if 'squarespace.com' in src_lower:
                self._add('CMS', 'Squarespace', 'Confirmed', 'Squarespace CDN')
            if 'assets.website-files.com' in src_lower or '.webflow.com' in src_lower:
                self._add('CMS', 'Webflow', 'Confirmed', 'Webflow assets')
            if 'core-js' in src_lower:
                self._add('JS Library', 'core-js', 'Confirmed', 'core-js asset')
            if 'woocommerce' in src_lower or 'wc-cart-fragments' in src_lower:
                self._add('E-commerce', 'WooCommerce', 'Confirmed', 'WooCommerce asset')
                self._add('CMS', 'WordPress', 'Confirmed', 'WooCommerce asset')
            if 'prestashop' in src_lower:
                self._add('E-commerce', 'PrestaShop', 'Confirmed', 'PrestaShop asset')
            if 'opencart' in src_lower or 'catalog/view/theme' in src_lower:
                self._add('E-commerce', 'OpenCart', 'Likely', 'OpenCart asset')

        php_ext = re.findall(r'\.php[\?#]?', static.html)
        if len(php_ext) >= 2:
            self._add('Programming Language', 'PHP', 'Likely', 'Multiple .php references')

        aspx_ext = re.findall(r'\.aspx[\?#]?', static.html)
        if len(aspx_ext) >= 2:
            self._add('Programming Language', 'ASP.NET', 'Likely', 'Multiple .aspx references')

        if re.search(r'["\']\/graphql["\']|graphqlEndpoint|ApolloClient', all_scripts_text, re.I):
            self._add('API', 'GraphQL', 'Likely', 'Inline script pattern')
        elif re.search(r'["\']\/api\/v\d|["\']\/rest\/', all_scripts_text, re.I):
            self._add('API', 'REST API', 'Likely', 'Inline script pattern')

        if any(g.startswith('rspackChunk') or g == '__rspack_require__' for g in js_globals):
            self._add('Build Tool', 'Rspack', 'Confirmed', 'rspackChunk global')

        has_turbopack = 'TURBOPACK' in js_globals
        if any(g.startswith('webpackChunk') or g in ('webpackJsonp', '__webpack_require__') for g in js_globals):
            self._add('Build Tool', 'Webpack', 'Confirmed', 'webpack global')
        elif '__webpack_hash__' in js_globals and not has_turbopack:
            self._add('Build Tool', 'Webpack', 'Likely', '__webpack_hash__ global')

        has_modulepreload = 'modulepreload' in static.html
        has_vite_assets = bool(re.search(
            r'/assets/[a-zA-Z0-9._/-]+[.\-][A-Za-z0-9]{8}\.(js|css)',
            static.html
        ))
        if has_modulepreload and has_vite_assets and 'Web Framework::Next.js' not in self.findings:
            # Rollup and other bundlers emit the same modulepreload + hashed
            # asset shape, so on its own this is only a weak hint.
            self._add('Build Tool', 'Vite', 'Suspected', 'Vite modulepreload + hashed assets')

    def _apply_versions(self, static):
        for key, finding in self.findings.items():
            if finding.version:
                continue

            tech = finding.name

            for hdr_val in static.response_headers.values():
                m = re.search(r'(?<![A-Za-z0-9])' + re.escape(tech) + r'[/ ]v?([\d]+\.[\d]+(?:\.[\d]+)?)', hdr_val, re.I)
                if m:
                    finding.version = m.group(1)
                    break

            if finding.version:
                continue

            for meta in static.meta_tags:
                if meta.get('name', '').lower() == 'generator':
                    content = meta.get('content', '')
                    m = re.search(re.escape(tech) + r'[/ ]([\d]+\.[\d]+(?:\.[\d]+)?(?:[-.][a-zA-Z0-9]+)?)', content, re.I)
                    if m:
                        finding.version = m.group(1)
                        break

            if finding.version:
                continue

            all_src = static.scripts + static.stylesheets
            tech_escaped = re.escape(tech.lower().replace('.js', ''))
            for src in all_src:
                m = re.search(
                    r'(?:^|[/.@])' + tech_escaped + r'[/.@].*?[?&;]ver=(\d+\.\d+(?:\.\d+)?)',
                    src, re.I
                )
                if not m:
                    m = re.search(
                        r'(?:^|[/])' + tech_escaped + r'[@/]v?(\d+\.\d+(?:\.\d+)?)',
                        src, re.I
                    )
                if m and m.group(1) not in ('1.0.0', '0.0.0', '0.0.1'):
                    finding.version = m.group(1)
                    break

            if finding.version:
                continue

            if tech == 'Bootstrap':
                for src in all_src:
                    m = re.search(r'bootstrap(?:\.min)?\.(?:css|js)(?:\?v?=|\?ver=|[?&]ver=)(\d+\.\d+(?:\.\d+)?)', src, re.I)
                    if m:
                        finding.version = m.group(1)
                        break
                if finding.version:
                    continue
                for content in static.stylesheet_contents.values():
                    m = re.search(r'Bootstrap\s+v?(\d+\.\d+(?:\.\d+)?)', content[:5000], re.I)
                    if not m:
                        m = re.search(r'bootstrap(?:\.min)?\.css\s+v?(\d+\.\d+(?:\.\d+)?)', content[:5000], re.I)
                    if m:
                        finding.version = m.group(1)
                        break
                if finding.version:
                    continue
                for content in static.script_contents.values():
                    m = re.search(r'Bootstrap\s+v?(\d+\.\d+(?:\.\d+)?)', content[:5000], re.I)
                    if m:
                        finding.version = m.group(1)
                        break

    def _cross_validate(self):
        for key, f in self.findings.items():
            if f.confidence == 'Confirmed':
                continue
            unique = set()
            for e in f.evidences:
                tag = re.split(r'[:\s]', e.strip(), 1)[0]
                unique.add(tag)
            if len(unique) >= 2:
                if f.confidence == 'Suspected':
                    f.confidence = 'Likely'
                elif f.confidence == 'Likely':
                    f.confidence = 'Confirmed'

    def _short(self, url, maxlen=60):
        return url[:maxlen] + '...' if len(url) > maxlen else url

    def _build_results(self):
        grouped = {}
        for f in sorted(self.findings.values(), key=lambda x: -CONFIDENCE_ORDER.get(x.confidence, 0)):
            if f.category not in grouped:
                grouped[f.category] = []
            entry = {
                'name': f.name,
                'confidence': f.confidence,
                'evidence': ' | '.join(f.evidences[:3])
            }
            if f.version:
                entry['version'] = f.version
            grouped[f.category].append(entry)
        return grouped
