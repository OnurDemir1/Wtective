"""Misleading responses that must NOT trigger detections."""

from tests.util import scan


def test_common_local_vars_are_not_technologies():
    html = """
    <html><head><script>
      var io = 3;
      var ga = function(){};
      const analytics = {};
      let heap = [];
      var chart = null;
      const paper = document.body;
    </script></head><body>hello</body></html>
    """
    r = scan(html)
    for name in ('Socket.IO', 'Google Analytics', 'Segment', 'Heap',
                 'Chart.js', 'Paper.js'):
        assert not r.has(name), f"{name} should not be detected from a local var"


def test_ambiguous_long_word_var_skipped():
    r = scan("<script>var google = {}; var drift = 1; var moment = 2;</script>")
    assert not r.has('Google Maps')
    assert not r.has('Google Ads')
    assert not r.has('Drift')
    assert not r.has('Moment.js')


def test_technology_named_in_body_text_is_ignored():
    # The page merely talks about Apache and WordPress; no real signal.
    html = """
    <html><body>
      <p>Our servers proudly run Apache and WordPress.</p>
      <p>We also love jQuery and Bootstrap here.</p>
    </body></html>
    """
    r = scan(html, headers={'server': 'nginx'})
    assert r.has('Nginx')
    assert not r.has('Apache')
    assert not r.has('WordPress')
    assert not r.has('jQuery')


def test_two_headers_same_method_do_not_over_promote():
    # Fastly matches on two header rules; both are a single "Header" method,
    # so cross-validation must keep it at Likely, not upgrade to Confirmed.
    r = scan("<html></html>", headers={'via': 'Fastly', 'x-served-by': 'cache-abc'})
    assert r.has('Fastly')
    assert r.confidence('Fastly') == 'Likely'


def test_data_action_without_controller_is_not_stimulus():
    r = scan('<div data-action="click->x#y">nope</div>')
    assert not r.has('Stimulus')


def test_few_utility_classes_are_not_tailwind():
    r = scan('<div class="container btn header-main content">x</div>')
    assert not r.has('Tailwind CSS')


def test_fastly_via_header_is_not_reported_as_varnish():
    # Fastly fronts requests with `Via: 1.1 varnish`; that must not surface a
    # separate Varnish finding. Only the specific X-Varnish header counts.
    r = scan("<html></html>", headers={'via': '1.1 varnish', 'x-served-by': 'cache-fra-1'})
    assert not r.has('Varnish')
    assert r.has('Fastly')


def test_self_hosted_varnish_still_detected():
    r = scan("<html></html>", headers={'x-varnish': '12345 67890'})
    assert r.has('Varnish')


def test_vendor_bootstrap_loader_is_not_bootstrap_framework():
    # A file literally named "dotcom-bootstrap.js" is a vendor loader, not the
    # Bootstrap CSS framework.
    r = scan('<script src="https://cdn.example.com/web/dotcom-bootstrap.js"></script>')
    assert not r.has('Bootstrap')


def test_generic_hashed_assets_are_not_confidently_vite():
    # modulepreload + hashed /assets/ is shared by several bundlers, so a bare
    # match must stay Suspected, never Likely/Confirmed.
    html = """
    <link rel="modulepreload" href="/assets/index.a1b2c3d4.js">
    <script type="module" src="/assets/main.99887766.js"></script>
    """
    r = scan(html)
    if r.has('Vite'):
        assert r.confidence('Vite') == 'Suspected'


def test_short_server_token_does_not_leak_version_to_other_tech():
    # A "Django/2.1" server banner must not hand a version to an unrelated
    # finding via loose substring matching.
    html = "<meta name='generator' content='Django'>"
    r = scan(html, headers={'server': 'Django/2.1.7'})
    # Go should not exist at all here; assert nothing borrowed the version.
    assert not r.has('Go')
