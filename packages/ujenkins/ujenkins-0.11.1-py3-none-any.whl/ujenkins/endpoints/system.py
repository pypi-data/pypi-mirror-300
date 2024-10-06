import json

from typing import NamedTuple, Tuple

from ujenkins.exceptions import JenkinsError


class JenkinsVersion(NamedTuple):
    major: int
    minor: int
    patch: int = 0
    build: int = 0


class System:

    def __init__(self, jenkins) -> None:
        self.jenkins = jenkins

    def get_status(self) -> dict:
        """
        Get server status.

        Returns:
            dict: jenkins server details.
        """
        return self.jenkins._request('GET', '/api/json')

    def get_version(self) -> JenkinsVersion:
        """
        Get server version.

        Returns:
            JenkinsVersion: named tuple with minor, major, patch version.
        """
        def callback(response):
            header = response.headers.get('X-Jenkins')
            if not header:
                raise JenkinsError('Header `X-Jenkins` isn`t found in response')

            versions = header.split('.')

            return JenkinsVersion(*map(int, versions))

        return self.jenkins._request('GET', '/', _callback=callback)

    def is_ready(self) -> bool:
        """
        Determines is server loaded and ready for work.

        Returns:
            bool: ready state.
        """
        def callback(response):
            try:
                status = response.text
                return 'mode' in status
            except JenkinsError:
                return False

        return self.jenkins._request('GET', '/api/json', _callback=callback)

    def quiet_down(self) -> None:
        """
        Start server quiet down period, new builds will not be started.

        Returns:
            None
        """
        return self.jenkins._request('POST', '/quietDown')

    def cancel_quiet_down(self) -> None:
        """
        Cancel server quiet down period.

        Returns:
            None
        """
        return self.jenkins._request('POST', '/cancelQuietDown')

    def restart(self) -> None:
        """
        Restart server immediately.

        Returns:
            None
        """
        return self.jenkins._request('POST', '/restart')

    def safe_restart(self) -> None:
        """
        Restart server when installation is complete and no jobs are running.

        Returns:
            None
        """
        return self.jenkins._request('POST', '/safeRestart')

    @staticmethod
    def _build_token_url(suffix: str) -> str:
        return '/me/descriptorByName/jenkins.security.ApiTokenProperty/' + suffix

    def generate_token(self, name: str) -> Tuple[str, str]:
        """
        Generate new API token.

        Args:
            name (str):
                Name of token.

        Returns:
            Tuple[str, str]: tokenValue - uses for authorization,
                             tokenUuid - uses for revoke
        """
        def callback(response):
            content = json.loads(response.text)

            if content['status'] != 'ok':
                raise JenkinsError('Non OK status returned: ' + str(content))

            return content['data']['tokenValue'], content['data']['tokenUuid']

        params = {'newTokenName': name}

        return self.jenkins._request(
            'POST',
            self._build_token_url('generateNewToken'),
            params=params,
            _callback=callback,
        )

    def revoke_token(self, token_uuid: str) -> None:
        """
        Revoke API token, please note that uuid is used, not value.

        Args:
            token_uuid (str):
                UUID of token to be revoked.

        Returns:
            None
        """
        params = {'tokenUuid': token_uuid}

        return self.jenkins._request(
            'POST',
            self._build_token_url('revoke'),
            params=params
        )

    def run_groovy_script(self, script: str) -> str:
        """
        Execute Groovy script on the server.

        Args:
            script (str):
                Script content.

        Returns:
            str: output of script.
        """
        return self.jenkins._request(
            'POST',
            '/scriptText',
            data={'script': script},
            _callback=self.jenkins._return_text,
        )
