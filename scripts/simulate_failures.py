import argparse
import os
import sys
import time

import requests


BASE_URL = os.environ.get("SIMULATE_BASE_URL", "http://localhost:5001")


def run_request(path: str, expected: int | None = None, pause: float = 0.5) -> None:
    url = f"{BASE_URL}{path}"
    try:
        response = requests.get(url, timeout=5)
        print(f"{response.request.method} {url} -> {response.status_code}")
        if expected is not None and response.status_code != expected:
            print(
                f"Ожидался статус {expected}, но получен {response.status_code}",
                file=sys.stderr,
            )
    except requests.RequestException as exc:
        print(f"Ошибка запроса к {url}: {exc}", file=sys.stderr)
    time.sleep(pause)


def scenario_normal() -> None:
    print("Сценарий normal: успешные запросы")
    for path in ["/", "/materials", "/suppliers", "/workers"]:
        run_request(path, expected=200)


def scenario_auth() -> None:
    print("Сценарий auth: ошибки авторизации")
    for _ in range(3):
        run_request("/demo/auth-failure", expected=401)


def scenario_bad_request() -> None:
    print("Сценарий bad-request: ошибки 400")
    for _ in range(2):
        run_request("/demo/bad-request", expected=400)


def scenario_forbidden() -> None:
    print("Сценарий forbidden: ошибки 403")
    for _ in range(2):
        run_request("/demo/forbidden", expected=403)


def scenario_invalid() -> None:
    print("Сценарий invalid: несуществующие ресурсы")
    for path in ["/missing-resource", "/api/unknown", "/does-not-exist"]:
        run_request(path, expected=404)


def scenario_unprocessable() -> None:
    print("Сценарий unprocessable: ошибки 422")
    for _ in range(2):
        run_request("/demo/unprocessable", expected=422)


def scenario_rate_limit() -> None:
    print("Сценарий rate-limit: ошибки 429")
    for _ in range(2):
        run_request("/demo/rate-limit", expected=429)


def scenario_failure() -> None:
    print("Сценарий failure: 500 ошибки сервера")
    for _ in range(3):
        run_request("/demo/failure", expected=500)


def scenario_unavailable() -> None:
    print("Сценарий unavailable: ошибки 503")
    for _ in range(2):
        run_request("/demo/unavailable", expected=503)


def scenario_client_errors() -> None:
    print("Сценарий client-errors: набор клиентских ошибок")
    scenario_bad_request()
    scenario_auth()
    scenario_forbidden()
    scenario_invalid()
    scenario_unprocessable()
    scenario_rate_limit()


def scenario_server_errors() -> None:
    print("Сценарий server-errors: набор серверных ошибок")
    scenario_failure()
    scenario_unavailable()


def main() -> None:
    parser = argparse.ArgumentParser(description="Имитация отказов для ПР4")
    parser.add_argument(
        "--scenario",
        choices=[
            "normal",
            "auth",
            "bad-request",
            "forbidden",
            "invalid",
            "unprocessable",
            "rate-limit",
            "failure",
            "unavailable",
            "client-errors",
            "server-errors",
            "all",
        ],
        default="all",
        help="Сценарий генерации логов",
    )
    args = parser.parse_args()

    if args.scenario in ("normal", "all"):
        scenario_normal()
    if args.scenario in ("bad-request",):
        scenario_bad_request()
    if args.scenario in ("auth",):
        scenario_auth()
    if args.scenario in ("forbidden",):
        scenario_forbidden()
    if args.scenario in ("invalid",):
        scenario_invalid()
    if args.scenario in ("unprocessable",):
        scenario_unprocessable()
    if args.scenario in ("rate-limit",):
        scenario_rate_limit()
    if args.scenario in ("failure",):
        scenario_failure()
    if args.scenario in ("unavailable",):
        scenario_unavailable()
    if args.scenario in ("client-errors",):
        scenario_client_errors()
    if args.scenario in ("server-errors",):
        scenario_server_errors()
    if args.scenario == "all":
        scenario_client_errors()
        scenario_server_errors()


if __name__ == "__main__":
    main()
