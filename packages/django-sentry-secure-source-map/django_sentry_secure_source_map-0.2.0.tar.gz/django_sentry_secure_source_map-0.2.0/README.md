# django-sentry-secure-source-map


![CI](https://github.com/torchbox/django-sentry-secure-source-map/workflows/CI/badge.svg)
![PyPI](https://img.shields.io/pypi/v/django-sentry-secure-source-map.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-sentry-secure-source-map.svg)


A middleware to ensure only Sentry can access source maps.

When enabled, only requests from Sentry will be able to access source maps (any URL starting with `STATIC_URL` and ending `.map`).

For more information, see [Secure Access to Source Maps](https://docs.sentry.io/platforms/javascript/sourcemaps/uploading/hosting-publicly/#secure-access-to-source-maps)

## Installation

```
pip install django-sentry-secure-source-map
```

Then add `sentry_secure_source_map.SentrySecureSourceMapMiddleware` to your `MIDDLEWARE` in `settings.py`. Ideally, it should be placed as high as possible, before tools like [`whitenoise`](https://pypi.org/project/whitenoise/).

Next, you need to configure the token. Retrieve your project's "Security Token" from the settings page, and set it as `SENTRY_SECURITY_TOKEN`.

```python
SENTRY_SECURITY_TOKEN = "abcde12345"
```

If the token isn't set, the middleware does nothing.

"Enable JavaScript source fetching" **must** be enabled in Sentry.
