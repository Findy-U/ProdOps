from payload_example.issue_example import issue
from webhook.parse_issue import parse_issue
import datetime


def test_parse_issue_returns_dict() -> None:
    parsed_issue = parse_issue(issue)
    assert type(parsed_issue) is dict


def test_parse_issue_returns_expected_dict() -> None:
    expected_return = {'project_card_id': '1793822382',
                       'assignee': {'login': 'Demian143', 'id': 81446007,
                                    'node_id': 'MDQ6VXNlcjgxNDQ2MDA3', 'avatar_url': 'https://avatars.githubusercontent.com/u/81446007?v=4', 'gravatar_id': '', 'url': 'https://api.github.com/users/Demian143', 'html_url': 'https://github.com/Demian143', 'followers_url': 'https://api.github.com/users/Demian143/followers', 'following_url': 'https://api.github.com/users/Demian143/following{/other_user}', 'gists_url': 'https://api.github.com/users/Demian143/gists{/gist_id}', 'starred_url': 'https://api.github.com/users/Demian143/starred{/owner}{/repo}',
                                    'subscriptions_url': 'https://api.github.com/users/Demian143/subscriptions', 'organizations_url': 'https://api.github.com/users/Demian143/orgs', 'repos_url': 'https://api.github.com/users/Demian143/repos', 'events_url': 'https://api.github.com/users/Demian143/events{/privacy}', 'received_events_url': 'https://api.github.com/users/Demian143/received_events', 'type': 'User', 'site_admin': False},
                       'assignee_login': None,
                       'created_at': datetime.datetime(2023, 7, 7, 16, 24, 5, tzinfo=datetime.timezone.utc),
                       'closed_at': None}

    assert parse_issue(issue) == expected_return
