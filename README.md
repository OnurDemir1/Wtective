# Wtective

A fast, accurate CLI that detects the web technologies behind any site — frameworks, CMSes, e-commerce platforms, CDNs, analytics, servers, and security headers — from a single URL.

Wtective is built to be **conservative**: it favours real signals (headers, cookies, meta generators, genuine JS globals, asset paths) over loose guesses, so results stay trustworthy instead of noisy.

## Install

```bash
git clone https://github.com/OnurDemir1/Wtective.git
cd Wtective
```

**Recommended — [pipx](https://pipx.pypa.io/)** (installs the `wtect` command globally in its own isolated environment):

```bash
pipx install .
```

On Debian/Kali/Ubuntu, install pipx first if you don't have it:

```bash
sudo apt install -y pipx
pipx ensurepath   # then restart your shell
```

**Alternative — virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install .
```

> Running a bare `pip install .` on Debian/Kali/Ubuntu fails with
> `error: externally-managed-environment` (PEP 668). Use pipx or a venv as
> shown above rather than `--break-system-packages`.

## Usage

```bash
wtect -u example.com
wtect -u https://www.example.com/
```

Aliases `wtective` and `wt` work the same way.

## Confidence levels

Every result is tagged so you know how much to trust it:

- `+` **Confirmed** — a definitive signal (response header, meta generator, real global, or known asset path).
- `~` **Likely** — a strong but indirect signal.
- `?` **Suspected** — a weak signal that needs corroboration.

Independent signals reinforce each other: two different kinds of evidence for the same technology raise its confidence automatically.

## What it detects

| Category | Examples |
|---|---|
| Framework | Next.js, Nuxt, SvelteKit, Astro, Remix, Angular, Vue, React |
| CMS | WordPress, Webflow, Wix, Ghost, Drupal, Framer |
| E-commerce | Shopify, WooCommerce, Magento, PrestaShop |
| UI / CSS | Tailwind, Bootstrap, Material UI, Ant Design |
| Build tool | Webpack, Vite, Turbopack, Rspack |
| Analytics | Google Analytics, GTM, Mixpanel, Plausible, Hotjar |
| CDN / WAF | Cloudflare, Fastly, Akamai, CloudFront |
| Hosting | Vercel, Netlify, AWS, Azure, Fly.io |
| Server | Nginx, Apache, Caddy, LiteSpeed |
| Security | HSTS, CSP, WAF detection, exposed source maps |

...and hundreds more across payments, chat, auth, monitoring, and fonts.

## Example

```
wtective v1.0  Web Technology Detector
--------------------------------------------------
Target: https://woocommerce.com/

20 technologies detected across 12 categories

Scan Results
├── CMS (1)
│   └── +  WordPress 7.0  Confirmed
├── E-commerce (1)
│   └── +  WooCommerce  Confirmed
├── Analytics (1)
│   └── +  Google Tag Manager  Confirmed
└── ...

+ Confirmed (12)  ~ Likely (8)  ? Suspected (0)
Completed in 5.9s
```

## Development

Run the test suite against the built-in mocked responses:

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
