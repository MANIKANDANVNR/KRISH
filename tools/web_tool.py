from urllib.parse import urlparse
import ipaddress
import socket

import requests


class WebTool:

    name = "web"

    permission = "tool.web"

    risk = "medium"

    description = (
        "Retrieves public HTTP/HTTPS web pages."
    )

    def __init__(
        self,
        timeout=15,
    ):

        self.timeout = timeout

    def _validate_url(
        self,
        url,
    ):

        parsed = urlparse(url)

        if parsed.scheme not in {
            "http",
            "https",
        }:

            raise ValueError(
                "Only HTTP and HTTPS are allowed."
            )

        if not parsed.hostname:

            raise ValueError(
                "URL hostname is required."
            )

        hostname = parsed.hostname

        try:

            addresses = socket.getaddrinfo(
                hostname,
                None,
            )

        except socket.gaierror as error:

            raise ValueError(
                "Unable to resolve hostname."
            ) from error

        for address in addresses:

            ip_text = address[4][0]

            try:

                ip = ipaddress.ip_address(
                    ip_text
                )

            except ValueError:
                continue

            if (
                ip.is_private
                or ip.is_loopback
                or ip.is_link_local
                or ip.is_reserved
            ):

                raise PermissionError(
                    "Private/internal network "
                    "addresses are blocked."
                )

        return url

    def get(
        self,
        url,
    ):

        url = self._validate_url(
            url
        )

        response = requests.get(
            url,
            timeout=self.timeout,
            headers={
                "User-Agent": "KRISH/1.0"
            },
            allow_redirects=False,
            stream=True,
        )

        response.raise_for_status()

        content_length = response.headers.get(
            "Content-Length"
        )

        if (
            content_length
            and int(content_length)
            > 10_000_000
        ):

            raise ValueError(
                "Response exceeds 10 MB limit."
            )

        data = bytearray()

        for chunk in response.iter_content(
            chunk_size=65536
        ):

            data.extend(chunk)

            if len(data) > 10_000_000:

                raise ValueError(
                    "Response exceeds 10 MB limit."
                )

        return {
            "status": response.status_code,
            "url": response.url,
            "text": data.decode(
                response.encoding
                or "utf-8",
                errors="replace",
            ),
        }