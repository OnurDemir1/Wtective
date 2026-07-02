"""Genuine signals that must be detected, at the right confidence."""

from tests.util import scan


def test_real_window_globals_are_confirmed():
    html = """
    <script>
      window.Shopify = window.Shopify || {};
      window.dataLayer = window.dataLayer || [];
    </script>
    """
    r = scan(html)
    assert r.confidence('Shopify') == 'Confirmed'
    assert r.confidence('Google Tag Manager') == 'Confirmed'


def test_distinctive_local_var_is_likely():
    r = scan("<script>var mixpanel = init();</script>")
    assert r.has('Mixpanel')
    assert r.confidence('Mixpanel') == 'Likely'


def test_nginx_server_header_with_version():
    r = scan("<html></html>", headers={'server': 'nginx/1.25.3'})
    assert r.has('Nginx')
    assert r.version('Nginx') == '1.25.3'


def test_php_powered_by_header_version():
    r = scan("<html></html>", headers={'x-powered-by': 'PHP/8.2.11'})
    assert r.has('PHP')
    assert r.version('PHP') == '8.2.11'


def test_meta_generator_wordpress_with_version():
    r = scan('<meta name="generator" content="WordPress 6.5.2">')
    assert r.confidence('WordPress') == 'Confirmed'
    assert r.version('WordPress') == '6.5.2'


def test_next_js_implies_react():
    html = """
    <div id="__next"></div>
    <script id="__NEXT_DATA__" type="application/json">{}</script>
    <script src="/_next/static/chunks/main.js"></script>
    """
    r = scan(html)
    assert r.confidence('Next.js') == 'Confirmed'
    assert r.has('React')


def test_cloudflare_via_cf_ray_header():
    r = scan("<html></html>", headers={'cf-ray': 'abc123-AMS'})
    assert r.confidence('Cloudflare') == 'Confirmed'


def test_cloudflare_via_server_header():
    r = scan("<html></html>", headers={'server': 'cloudflare'})
    assert r.confidence('Cloudflare') == 'Confirmed'


def test_wordpress_cross_validates_across_two_methods():
    # A Link header (Likely) plus a wp- cookie (Likely) are two independent
    # methods, so cross-validation should promote WordPress to Confirmed.
    r = scan(
        "<html></html>",
        headers={
            'link': '<https://example.com/wp-json/>; rel="https://api.w.org/"',
            'set-cookie': 'wp-settings-time-1=1699; path=/',
        },
    )
    assert r.confidence('WordPress') == 'Confirmed'


def test_wordpress_asset_path_confirms():
    html = '<script src="/wp-content/themes/twenty/app.js"></script>'
    r = scan(html)
    assert r.confidence('WordPress') == 'Confirmed'


def test_stimulus_controller_attribute_detected():
    r = scan('<div data-controller="hello" data-action="click->hello#greet"></div>')
    assert r.has('Stimulus')


def test_tailwind_from_responsive_prefixes():
    html = '<div class="sm:hidden md:flex lg:block hover:bg-blue-500">x</div>'
    r = scan(html)
    assert r.has('Tailwind CSS')


def test_exposed_source_map_detected():
    html = '<script src="/app.js"></script>'
    pages = {'/app.js.map': {'body': '{"version":3,"sources":["a.js"],"names":[]}'}}
    r = scan(html, pages=pages)
    assert r.confidence('Exposed Source Maps') == 'Confirmed'


def test_security_headers_detected():
    r = scan(
        "<html></html>",
        headers={
            'strict-transport-security': 'max-age=63072000',
            'content-security-policy': "default-src 'self'",
        },
    )
    assert r.has('HSTS')
    assert r.has('CSP')


def test_modern_ember_via_view_ids_and_classes():
    # Modern Ember apps do not expose window.Ember; they auto-assign
    # id="ember123" and ember-view classes instead.
    html = """
    <div id="ember0" class="ember-view">
      <div id="ember42" class="ember-view app-shell ember-application">content</div>
    </div>
    """
    r = scan(html)
    assert r.has('Ember.js')


def test_unreachable_target_returns_empty():
    r = scan(fail=True)
    assert r.names() == set()
