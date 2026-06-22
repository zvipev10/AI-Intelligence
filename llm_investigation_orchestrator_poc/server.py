#!/usr/bin/env python3
from __future__ import annotations

import http.client
import json
import mimetypes
import re
import sys
import time
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import paramiko


ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / ".hermes-api.json"
PERFORMANCE_DIR = ROOT / "performance_logs"
TERMINAL_STATUSES = {"completed", "failed", "cancelled"}
EVENT_ID_PATTERN = re.compile(r"\b(?:PORT|CUST|FIN|TEL|MOVE|OBS|CAM|SIG|ACOU|BORD|DRONE|MAINT|SOC)-\d{4}\b")
ACTIVE_RUN_STARTED_AT = None
APP_BUILD = "planner-1"


def elapsed_ms(started: float) -> float:
    return round((time.perf_counter() - started) * 1000, 3)


def parse_utc(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def safe_filename(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.:-]+", "-", str(value or "")).strip("-")
    return cleaned[:120] or "run"


def write_performance_log(run_id: str, performance: dict, prompt: str | None = None) -> Path:
    PERFORMANCE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = PERFORMANCE_DIR / f"{timestamp}-{safe_filename(run_id)}.json"
    payload = {
        "run_id": run_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "prompt": prompt,
        "performance": performance,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def update_performance_client(run_id: str, client_performance: dict) -> Path | None:
    if not run_id:
        return None
    files = sorted(PERFORMANCE_DIR.glob(f"*-{safe_filename(run_id)}.json"))
    if not files:
        return None
    path = files[-1]
    payload = json.loads(path.read_text(encoding="utf-8"))
    performance = payload.setdefault("performance", {})
    performance["client"] = client_performance
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


class SSHHTTPConnection(http.client.HTTPConnection):
    def __init__(self, ssh_client, remote_host, remote_port, timeout=30):
        super().__init__(remote_host, remote_port, timeout=timeout)
        self.ssh_client = ssh_client

    def connect(self):
        transport = self.ssh_client.get_transport()
        if transport is None:
            raise ConnectionError("SSH transport is unavailable")
        self.sock = transport.open_channel(
            "direct-tcpip",
            (self.host, self.port),
            ("127.0.0.1", 0),
            timeout=self.timeout,
        )


class HermesSession:
    def __init__(self, config):
        self.config = config
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def __enter__(self):
        self.ssh.connect(
            self.config["host"],
            username=self.config["user"],
            key_filename=self.config["key_path"],
            look_for_keys=False,
            allow_agent=False,
            timeout=15,
        )
        return self

    def __exit__(self, exc_type, exc, tb):
        self.ssh.close()

    def request(self, method, path, body=None, timeout=60, parse_json=True):
        connection = SSHHTTPConnection(
            self.ssh,
            self.config["remote_host"],
            int(self.config["remote_port"]),
            timeout=timeout,
        )
        encoded = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Accept": "application/json" if parse_json else "text/event-stream",
        }
        if encoded is not None:
            headers["Content-Type"] = "application/json; charset=utf-8"
        try:
            connection.request(method, path, body=encoded, headers=headers)
            response = connection.getresponse()
            raw = response.read().decode("utf-8", errors="replace")
            if response.status >= 400:
                raise RuntimeError(f"Hermes API {response.status}: {raw}")
            return (json.loads(raw) if raw else {}) if parse_json else raw
        finally:
            connection.close()

    def ssh_command(self, command, timeout=30):
        _, stdout, stderr = self.ssh.exec_command(command, timeout=timeout)
        code = stdout.channel.recv_exit_status()
        output = stdout.read().decode("utf-8", errors="replace")
        error = stderr.read().decode("utf-8", errors="replace")
        if code:
            raise RuntimeError(error or output or f"SSH command failed: {code}")
        return output


class HermesClient:
    def __init__(self, config):
        self.config = config

    def request(self, method, path, body=None, timeout=60, parse_json=True):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            self.config["host"],
            username=self.config["user"],
            key_filename=self.config["key_path"],
            look_for_keys=False,
            allow_agent=False,
            timeout=15,
        )
        try:
            connection = SSHHTTPConnection(
                ssh,
                self.config["remote_host"],
                int(self.config["remote_port"]),
                timeout=timeout,
            )
            encoded = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
            headers = {
                "Authorization": f"Bearer {self.config['api_key']}",
                "Accept": "application/json" if parse_json else "text/event-stream",
            }
            if encoded is not None:
                headers["Content-Type"] = "application/json; charset=utf-8"
            connection.request(method, path, body=encoded, headers=headers)
            response = connection.getresponse()
            raw = response.read().decode("utf-8", errors="replace")
            if response.status >= 400:
                raise RuntimeError(f"Hermes API {response.status}: {raw}")
            return (json.loads(raw) if raw else {}) if parse_json else raw
        finally:
            ssh.close()

    def ssh_command(self, command, timeout=30):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            self.config["host"], username=self.config["user"],
            key_filename=self.config["key_path"], look_for_keys=False,
            allow_agent=False, timeout=15,
        )
        try:
            _, stdout, stderr = ssh.exec_command(command, timeout=timeout)
            code = stdout.channel.recv_exit_status()
            output = stdout.read().decode("utf-8", errors="replace")
            error = stderr.read().decode("utf-8", errors="replace")
            if code:
                raise RuntimeError(error or output or f"SSH command failed: {code}")
            return output
        finally:
            ssh.close()

    @staticmethod
    def summarize_audit(records):
        def format_ids(ids, limit=14):
            values = [str(value) for value in ids if value]
            if len(values) <= limit:
                return ", ".join(values) if values else "אין"
            return f'{", ".join(values[:limit])}, ועוד {len(values) - limit} מזהים'

        def compact_json(value):
            return json.dumps(value, ensure_ascii=False, separators=(",", ":"))

        def public_args(args):
            return {key: value for key, value in args.items() if key != "step_bridge"}

        def arg_clue(tool, args):
            if tool == "classify_question_intent":
                return f'השאלה "{args.get("question", "")}"'
            if tool in {"resolve_location", "resolve_event_reference", "resolve_entity"}:
                return f'"{args.get("query", "")}"'
            if tool == "trace_identifier":
                return f'המזהה "{args.get("identifier", "")}"'
            if tool == "trace_semantic_clues":
                clues = args.get("clues") or []
                seeds = args.get("seed_event_ids") or []
                if clues:
                    return f'הרמזים {format_ids(clues)}'
                return f'רמזים מתוך אירועי העוגן {format_ids(seeds)}'
            if tool == "plan_next_investigation_step":
                return f'מצב החקירה: {args.get("objective") or "יעד לא צוין"}'
            if tool == "get_events":
                return f'מזהי האירועים {format_ids(args.get("event_ids") or [])}'
            if tool == "find_related_events":
                return f'אירועי העוגן {format_ids(args.get("seed_event_ids") or [])}'
            if tool == "explain_linkage":
                return f'המעבר בין {args.get("first_event_id") or "אירוע ראשון"} לבין {args.get("second_event_id") or "אירוע שני"}'
            if tool == "build_event_sequence":
                return f'קבוצת האירועים {format_ids(args.get("event_ids") or [])}'
            if tool == "challenge_hypothesis":
                return f'ההשערה על בסיס {format_ids(args.get("supporting_event_ids") or [])}'
            if tool == "find_actor_history":
                actors = args.get("actors") or []
                return f'הגורם "{actors[0]}"' if len(actors) == 1 else f'הגורמים {format_ids(actors)}'
            if tool == "aggregate_events":
                return f'ממד הקיבוץ {args.get("group_by") or "לא צוין"}'
            filters = {key: value for key, value in public_args(args).items() if value not in (None, "", [], False)}
            return f'מסנני החיפוש {compact_json(filters)}' if filters else "חיפוש פתוח ללא מסננים"

        def result_clue(result):
            ids = result.get("event_ids") or [item.get("event_id") for item in result.get("events") or []]
            ids = [item for item in ids if item]
            if ids:
                return f'מזהים שעלו: {format_ids(ids)}'
            matches = result.get("matches") or []
            if matches:
                labels = [item.get("canonical_name") or item.get("entity_id") for item in matches]
                return f'ישויות שעלו: {format_ids(labels)}'
            locations = result.get("locations") or []
            if locations:
                labels = [item.get("name") or item.get("location_id") for item in locations]
                return f'מיקומים שעלו: {format_ids(labels)}'
            alternatives = result.get("alternative_event_ids") or []
            if alternatives:
                return f'חלופות שעלו: {format_ids(alternatives)}'
            return "השלב הקודם צמצם את מרחב החיפוש"

        def derived_bridge(tool, args, index, previous_result):
            clue = arg_clue(tool, args)
            if index == 0:
                observed = f'נקודת הפתיחה של החקירה היא {clue}.'
            else:
                observed = f'{result_clue(previous_result or {})}; מזה הסוכן עבר לבדוק את {clue}.'

            if tool == "classify_question_intent":
                decision = "לפני בחירת כלי נתונים, הסוכן מסווג את סוג הבקשה כדי לבחור מסלול עבודה ותקציב מתאים."
                expected = "לקבל מצב עבודה, תקציב כלים, משפחות כלים מותרות וחסומות, ורמז לתצוגה."
            elif tool == "resolve_location":
                decision = f'צריך להפוך את הביטוי {clue} למיקום מוכר כדי שכל חיפוש המשך יהיה ממוקד.'
                expected = "לקבל מזהי מיקום קנוניים או להבין שאין התאמה גאוגרפית ברורה."
            elif tool == "resolve_event_reference":
                decision = f'צריך להפוך את ההפניה {clue} לאירוע עוגן מדויק לפני הרחבת החקירה.'
                expected = "לקבל מזהה אירוע, זמן ומיקום שישמשו בסיס לצעדים הבאים."
            elif tool == "search_events":
                decision = f'הסוכן משתמש ב-{clue} כדי למצוא רשומות שעומדות בתנאי החיפוש ולאסוף מועמדים ראשונים.'
                expected = "לקבל רשימת אירועים מצומצמת שאפשר לאמת או להרחיב ממנה."
            elif tool == "get_events":
                decision = f'הסוכן קורא את הרשומות המלאות של {clue} כדי לא להסתמך רק על מזהים או תקצירים.'
                expected = "לאמת את תוכן האירועים, הזמנים, הגורמים והמיקומים לפני הסקת קשר."
            elif tool == "find_actor_history":
                decision = f'{clue} עשוי לקשור בין אירועים, לכן הסוכן בודק היסטוריה וכינויים.'
                expected = "למצוא הופעות נוספות של אותו גורם או להבין שהוא אינו יוצר רצף."
            elif tool == "aggregate_events":
                decision = f'הסוכן מקבץ לפי {clue} כדי לזהות ריכוזים או חריגות שלא בולטים באירוע יחיד.'
                expected = "לקבל תמונת התפלגות שתכוון לחיפוש ממוקד יותר."
            elif tool == "explain_linkage":
                decision = f'לפני הצגת מעבר בשרשרת, הסוכן בודק אם {clue} נתמך בגשר ראייתי ולא רק בסיפור רציף.'
                expected = "לקבל את סוג הגשר, חוזקו, או אזהרה שהמעבר הוא פער."
            elif tool == "build_event_sequence":
                decision = f'לאחר שנאספו כמה אירועים, הסוכן מסדר את {clue} כדי לבדוק אם יש רצף ולא רק סמיכות.'
                expected = "לראות סדר זמנים ומסלול, ולזהות קפיצות או חוליות חסרות."
            elif tool == "resolve_entity":
                decision = f'השם {clue} עלול להיות כינוי או שם חלקי, לכן הסוכן בודק אם הוא שייך לישות מוכרת.'
                expected = "לקבל שם קנוני וכינויים שישמשו לחיפושים הבאים."
            elif tool == "trace_identifier":
                negated = " כולל אזכורים שוללים" if args.get("include_negated") else ""
                decision = f'הערך {clue} נראה כמו מזהה חוזר, ולכן הסוכן עוקב אחר הופעותיו במקורות נוספים{negated}.'
                expected = "למצוא אירועים שמחוברים באותו מזהה, או לשלול שהמזהה חוזר בשרשרת."
            elif tool == "trace_semantic_clues":
                negated = " כולל אזכורים שוללים" if args.get("include_negated") else ""
                decision = f'הערך {clue} הוא רמז תפעולי ולא מזהה פורמלי, לכן הסוכן מחפש הופעות סמנטיות שלו במקורות נוספים{negated}.'
                expected = "למצוא חוליות שבהן אותו חפץ, מסלול, מחסן, כלי רכב או ניסוח תפעולי מחבר בין אירועים."
            elif tool == "plan_next_investigation_step":
                decision = "הסוכן עוצר לבקרת תהליך כדי לוודא שלא נשארו seeds מומלצים, רמזים סמנטיים או גשרים סמוכים שלא נבדקו לפני סיכום."
                expected = "לקבל אילוץ לצעד הבא, מזהים או רמזים שחובה לטפל בהם, וכלים שחסומים עד להשלמת הבדיקה."
            elif tool == "find_related_events":
                decision = f'במקום להישאר סביב אירוע יחיד, הסוכן מרחיב מ-{clue} לפי קשרי זמן, מקום, ישות ומזהים.'
                expected = "לאתר חוליות סמוכות או מוקדמות שמקבלות ניקוד קשר גבוה."
            elif tool == "challenge_hypothesis":
                decision = f'לפני חיזוק ההשערה, הסוכן בודק את {clue} מול חלופות ופערים.'
                expected = "לגלות הסברים תמימים, סתירות או חסרים שמחלישים את הרצף."
            else:
                decision = f'הסוכן משתמש ב-{clue} כדי לצמצם אי-ודאות ולהחליט על המשך החקירה.'
                expected = "לקבל פלט שיאשר, ישלול או ימקד את כיוון החקירה."
            return observed, decision, expected

        steps = []
        previous_result = None
        for index, record in enumerate(records):
            tool = record.get("tool", "MCP")
            args = record.get("arguments") or {}
            result = record.get("result") or {}
            observed_clue, decision, expected_value = derived_bridge(tool, args, index, previous_result)
            model_bridge = str(args.get("step_bridge") or "").strip()
            bridge_summary = model_bridge or decision
            if tool == "classify_question_intent":
                action = f'סיווג כוונת השאלה "{args.get("question", "")}".'
                outcome = (
                    f'הכוונה סווגה כ-{result.get("intent")}; מצב עבודה {result.get("recommended_mode")}; '
                    f'תקציב כלים {result.get("tool_budget")}; תצוגה מומלצת {result.get("recommended_view_hint")}; '
                    f'סיבה: {result.get("reason")}.'
                )
            elif tool == "resolve_location":
                action = f'פתרון הביטוי הגאוגרפי "{args.get("query", "")}" למזהי מיקום.'
                locations = result.get("locations") or []
                labels = [f'{item.get("location_id")} ({item.get("name")})' for item in locations]
                outcome = f'נמצאו {len(labels)} מיקומים: {", ".join(labels) if labels else "אין התאמות"}.'
            elif tool == "resolve_event_reference":
                action = f'פתרון ההפניה "{args.get("query", "")}" לאירוע עוגן.'
                ids = result.get("event_ids") or []
                times = [item.get("timestamp_utc") for item in result.get("events") or [] if item.get("timestamp_utc")]
                outcome = f'נמצאו {len(ids)} אירועים: {format_ids(ids)}' + (f'; זמנים: {", ".join(times)}.' if times else ".")
            elif tool in {"search_events", "find_actor_history"}:
                filters = []
                for key in ["start_time", "end_time", "location_ids", "actors", "source_types", "keywords", "night_only", "limit"]:
                    value = args.get(key)
                    if value not in (None, "", [], False):
                        filters.append(f"{key}={json.dumps(value, ensure_ascii=False)}")
                action = f'חיפוש במאגר עם המסננים: {"; ".join(filters) if filters else "ללא מסננים"}.'
                ids = result.get("event_ids") or []
                total = result.get("total", len(ids))
                returned = result.get("returned", len(ids))
                truncated = bool(result.get("truncated") or (isinstance(total, int) and isinstance(returned, int) and total > returned))
                warning = " זוהי תוצאה מקוצצת; אין לבחור ממנה עוגן חקירתי בלי צמצום נוסף או הגדלת limit." if truncated else ""
                outcome = f'נמצאו {total} רשומות; הוחזרו {returned}; מזהים: {format_ids(ids)}.{warning}'
            elif tool == "get_events":
                requested = args.get("event_ids") or []
                found = [item.get("event_id") for item in result.get("events") or []]
                missing = result.get("missing_event_ids") or []
                action = f'שליפת הרשומות המלאות עבור {len(requested)} מזהים: {format_ids(requested)}.'
                outcome = f'הוחזרו {len(found)} רשומות: {format_ids(found)}; חסרים: {format_ids(missing)}.'
            elif tool == "aggregate_events":
                group_by = args.get("group_by")
                filters = {key: value for key, value in public_args(args).items() if key != "group_by" and value not in (None, "", [], False)}
                action = f'קיבוץ אירועים לפי {group_by} עם מסננים {json.dumps(filters, ensure_ascii=False)}.'
                groups = result.get("groups") or []
                group_text = ", ".join(f'{item.get("label")}={item.get("count")}' for item in groups[:12])
                outcome = f'נכללו {result.get("total_events", 0)} אירועים; קבוצות: {group_text if group_text else "אין"}.'
            elif tool == "explain_linkage":
                action = f'בדיקת גשר ראייתי בין {args.get("first_event_id")} לבין {args.get("second_event_id")}.'
                bridges = result.get("bridges") or []
                bridge_text = ", ".join(f'{item.get("bridge_type")} ({item.get("detail")})' for item in bridges[:4])
                outcome = f'נמצאו {result.get("bridge_count", 0)} גשרים; {bridge_text if bridge_text else "לא נמצא גשר"}; הערכה: {result.get("assessment") or "אין"}.'
            elif tool == "build_event_sequence":
                requested = args.get("event_ids") or []
                route = result.get("route") or []
                route_text = " -> ".join(f'{item.get("location_name")} [{", ".join(item.get("event_ids") or [])}]' for item in route)
                action = f'מיון כרונולוגי של {len(requested)} אירועים: {format_ids(requested)}.'
                outcome = f'נבנה רצף של {result.get("event_count", 0)} אירועים בין {result.get("start_time")} ל-{result.get("end_time")}; מסלול: {route_text or "לא נבנה"}.'
            elif tool == "resolve_entity":
                action = f'פתרון שם הגורם "{args.get("query", "")}" לישות קנונית ולכינויים.'
                matches = result.get("matches") or []
                labels = [f'{item.get("entity_id")} ({item.get("canonical_name")})' for item in matches]
                outcome = f'נמצאו {len(matches)} התאמות: {", ".join(labels) if labels else "אין"}.'
            elif tool == "trace_identifier":
                action = f'מעקב אחר המזהה "{args.get("identifier", "")}" מסוג {args.get("identifier_type") or "אוטומטי"}.'
                ids = result.get("event_ids") or []
                excluded = result.get("excluded_negated_mentions", 0)
                outcome = f'נמצאו {result.get("total_mentions", len(ids))} אזכורים והוחזרו {len(ids)} אירועים: {format_ids(ids)}; הושמטו {excluded} אזכורים שוללים.'
            elif tool == "trace_semantic_clues":
                clues = args.get("clues") or result.get("clues") or []
                seeds = args.get("seed_event_ids") or []
                action = f'מעקב אחר רמזים סמנטיים {format_ids(clues)} מתוך עוגנים {format_ids(seeds)}.'
                ids = result.get("event_ids") or []
                total = result.get("total_matches", len(ids))
                returned = result.get("returned", len(ids))
                truncated = bool(result.get("truncated") or (isinstance(total, int) and isinstance(returned, int) and total > returned))
                warning = " זוהי תוצאה מקוצצת; יש לצמצם או להמשיך הרחבה לפני שלילת קשר." if truncated else ""
                recommended = [item.get("event_id") for item in result.get("recommended_next_seeds") or [] if item.get("event_id")]
                new_clues = result.get("new_clues_to_trace") or []
                recommendation = ""
                if recommended:
                    recommendation = f' seeds מומלצים להמשך: {format_ids(recommended)}.'
                if new_clues:
                    recommendation += f' רמזים חדשים: {format_ids(new_clues)}.'
                outcome = f'נמצאו {total} התאמות סמנטיות והוחזרו {returned}: {format_ids(ids)}.{recommendation}{warning}'
            elif tool == "plan_next_investigation_step":
                action = "בדיקת בקרה תהליכית למצב החקירה לפני בחירת הצעד הבא."
                required_ids = result.get("required_event_ids") or []
                required_clues = result.get("required_clues") or []
                blocked = result.get("blocked_tool_families") or []
                allowed = result.get("allowed_tool_families") or []
                state_summary = result.get("state_summary") or {}
                parts = [
                    f'אילוץ הצעד הבא: {result.get("next_step_constraint") or "לא צוין"}',
                    f'החלטה: {result.get("decision") or "לא צוין"}',
                    f'סיבה: {result.get("reason") or "לא צוינה"}',
                ]
                if required_ids:
                    parts.append(f'מזהים שחובה לטפל בהם: {format_ids(required_ids)}')
                if required_clues:
                    parts.append(f'רמזים שחובה לבדוק: {format_ids(required_clues)}')
                if allowed:
                    parts.append(f'כלים מותרים: {format_ids(allowed)}')
                if blocked:
                    parts.append(f'כלים חסומים זמנית: {format_ids(blocked)}')
                if state_summary:
                    parts.append(
                        "מצב קצר: "
                        f'שרשרת={state_summary.get("candidate_chain_length", 0)}, '
                        f'seeds פתוחים={state_summary.get("unexpanded_recommended_seed_count", 0)}, '
                        f'רמזים חדשים={state_summary.get("new_clue_count", 0)}, '
                        f'תקציב נותר={state_summary.get("tool_budget_remaining", 0)}'
                    )
                outcome = "; ".join(parts) + "."
            elif tool == "find_related_events":
                seeds = args.get("seed_event_ids") or []
                source_filter = args.get("source_types") or []
                source_text = f' וסוגי מקור {format_ids(source_filter)}' if source_filter else ""
                action = f'הרחבת ראיות העוגן {format_ids(seeds)} לפי {", ".join(args.get("dimensions") or ["entity", "identifier", "semantic", "time", "location"])}{source_text}.'
                ids = result.get("event_ids") or []
                total = result.get("total_candidates", len(ids))
                returned = result.get("returned", len(ids))
                truncated = bool(result.get("truncated") or (isinstance(total, int) and isinstance(returned, int) and total > returned))
                warning = " זוהי הרחבה מקוצצת; אין להסיק שאין המשך שרשרת בלי הגדלת limit, צמצום ממוקד או הרחבה נוספת." if truncated else ""
                recommended = [item.get("event_id") for item in result.get("recommended_next_seeds") or [] if item.get("event_id")]
                new_clues = result.get("new_clues_to_trace") or []
                recommendation = ""
                if recommended:
                    recommendation = f' seeds מומלצים להמשך: {format_ids(recommended)}.'
                if new_clues:
                    recommendation += f' רמזים חדשים: {format_ids(new_clues)}.'
                outcome = f'דורגו {total} מועמדים והוחזרו {returned}: {format_ids(ids)}.{recommendation}{warning}'
            elif tool == "challenge_hypothesis":
                evidence = args.get("supporting_event_ids") or []
                action = f'בדיקת חלופות ופערים להשערה על בסיס {len(evidence)} אירועים: {format_ids(evidence)}.'
                alternatives = result.get("alternative_event_ids") or []
                gaps = result.get("gaps") or []
                outcome = f'נמצאו {len(alternatives)} אירועי חלופה ו-{len(gaps)} פערים; חלופות: {format_ids(alternatives)}.'
            else:
                action = f'קלט: {json.dumps(public_args(args), ensure_ascii=False)}.'
                outcome = f'פלט: {json.dumps(result, ensure_ascii=False)}.'
            steps.append({
                "tool": tool,
                "bridge_summary": bridge_summary,
                "observed_clue": observed_clue,
                "decision": decision,
                "expected_value": expected_value,
                "rationale": decision,
                "action": action,
                "result": outcome,
                "technical": {
                    "tool": tool,
                    "arguments": args,
                    "is_error": bool(record.get("is_error")),
                    "timestamp_utc": record.get("timestamp_utc"),
                },
            })
            if tool == "aggregate_events" and result.get("group_by") == "location":
                steps[-1]["map_locations"] = [
                    {
                        "location_id": item.get("key"),
                        "location_name": item.get("label"),
                        "count": item.get("count", 0),
                    }
                    for item in (result.get("groups") or [])
                    if item.get("key")
                ]
            previous_result = result
        return steps

    @staticmethod
    def render_investigation_state(inv_state):
        """Render the structured investigation state as a Hebrew instruction block."""
        if not inv_state:
            return ""
        lines = ["--- מצב חקירה נוכחי (אל תחזור על עבודה שכבר בוצעה) ---"]
        turn = inv_state.get("turn", 0)
        lines.append(f"תור מספר: {turn}")

        confirmed = inv_state.get("confirmed_event_ids") or []
        if confirmed:
            ids_str = ", ".join(confirmed[:40])
            suffix = f" ועוד {len(confirmed) - 40}" if len(confirmed) > 40 else ""
            lines.append(f"אירועים שאושרו עד כה ({len(confirmed)}): {ids_str}{suffix}")

        actors = inv_state.get("confirmed_actors") or []
        if actors:
            lines.append(f"גורמים שזוהו: {', '.join(actors)}")

        entities = inv_state.get("entities_resolved") or {}
        if entities:
            entity_strs = [f"{eid}: {', '.join(aliases)}" for eid, aliases in entities.items()]
            lines.append(f"ישויות שפוענחו: {'; '.join(entity_strs)}")

        hypothesis = inv_state.get("current_hypothesis")
        if hypothesis:
            confidence = inv_state.get("confidence") or "לא הוגדרה"
            lines.append(f"השערה פעילה: {hypothesis}")
            lines.append(f"רמת ביטחון נוכחית: {confidence}")

        gaps = inv_state.get("gaps") or []
        if gaps:
            lines.append(f"פערים ידועים: {'; '.join(gaps)}")

        leads = inv_state.get("open_leads") or []
        if leads:
            lines.append(f"כיווני המשך פתוחים: {'; '.join(leads)}")

        lines.append("--- המשך החקירה משאלת האנליסט הנוכחית ---")
        return "\n".join(lines)

    def read_live_steps(self):
        if ACTIVE_RUN_STARTED_AT is None:
            return []
        audit_path = "/opt/intelligence-poc/mcp_audit.jsonl"
        audit_text = self.ssh_command(f"cat {audit_path} 2>/dev/null || true", timeout=20)
        audit_records = []
        for line in audit_text.splitlines():
            try:
                record = json.loads(line)
                timestamp = record.get("timestamp_utc")
                if timestamp:
                    parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                    if parsed < ACTIVE_RUN_STARTED_AT:
                        continue
                audit_records.append(record)
            except json.JSONDecodeError:
                continue
        return self.summarize_audit(audit_records)

    def investigate(self, prompt, history, investigation_state=None, investigation_id=None):
        global ACTIVE_RUN_STARTED_AT
        overall_started = time.perf_counter()
        performance = {
            "gateway": {},
            "hermes": {"poll_count": 0, "status_request_total_ms": 0},
            "tools": {},
        }
        audit_path = "/opt/intelligence-poc/mcp_audit.jsonl"
        instructions = (
            "אתה סוכן חקירה למערכת מודיעינית ניסיונית. השב בעברית בלבד.\n"
            "השתמש אך ורק בכלי MCP ששמם מתחיל ב-mcp_intelligence_events_poc_ ובנתונים שהם מחזירים.\n"
            "בכל שאלה חדשה, הפעל תחילה את הכלי classify_question_intent עם נוסח שאלת האנליסט והקשר קצר אם דרוש."
            " התייחס לפלט הכלי כמסגרת העבודה: recommended_mode, tool_budget, allowed_tool_families, blocked_tool_families ו-recommended_view_hint.\n"
            "בכל קריאת כלי, כולל classify_question_intent, כלול בפרמטרים step_bridge."
            " step_bridge חייב להיות משפט אחד או שניים בעברית שמסבירים את עבודת הסוכן בין תוצאת הכלי הקודם לבין בחירת הצעד הנוכחי:"
            " מה זוהה או הובן מהמידע שחזר, איזה פרט בתוצאה גרם לזיהוי הזה, מה הצעד הבא שנבחר, ומדוע הצעד הזה מתאים."
            " בצעד הראשון, כאשר אין עדיין תוצאת כלי קודמת, כתוב שזה צעד פתיחה לסיווג שאלת האנליסט ובחירת מסלול עבודה."
            " אל תחשוף מחשבות פנימיות או chain-of-thought; כתוב רציונל אנליטי קצר שניתן להציג לאנליסט.\n"
            "אם recommended_mode הוא retrieval: הישאר בתוך tool_budget ככל האפשר, השתמש רק במשפחות הכלים המותרות,"
            " ואל תפעיל challenge_hypothesis, find_related_events או explain_linkage אלא אם המשתמש ביקש במפורש קשר נסתר, דפוס, חשד, הסבר או חלופות.\n"
            "אם recommended_mode הוא investigation: בצע חקירה, אך נסה להישאר בתוך tool_budget. עבור חקירות שרשרת, מזהה ספציפי, גבול או רכיב מרכזי, tool_budget עשוי להיות 30 והוא נועד לאפשר השלמת בדיקה אמיתית."
            " אל תעצור אחרי מציאת שתי רשומות ישירות בלבד; המשך להרחבה, צמצום, בדיקת גשרים, ובניית רצף עד שיש בסיס למסקנה או עד שמוצגים פערים מפורשים.\n"
            "בחקירה על מזהה ספציפי לכיוון יעד, למשל מזהה מטען לכיוון גבול, בצע סדר עבודה מחייב:"
            " 1) trace_identifier למזהה עצמו;"
            " 2) אם נמצאו רשומות ישירות, find_related_events מהן עם limit=500 לפני כל challenge_hypothesis;"
            " 3) אחרי כלי שמחזיר recommended_next_seeds או new_clues_to_trace, הפעל plan_next_investigation_step לפני בחירת צעד אחר;"
            " 4) אם המזהה הישיר מפסיק להופיע, הפעל trace_semantic_clues על מונחי חפץ, תיאור מטען, מחסן, מסלול, כלי רכב או ניסוח תקשורתי שעלו ברשומות;"
            " 5) אם יש הרבה מועמדים, צמצם לפי source_types, זמן, מיקום או ממד קשר והרחב שוב;"
            " 6) בדוק גשרים עם explain_linkage בין מועמדי שרשרת מרכזיים;"
            " 7) בנה רצף עם build_event_sequence;"
            " 8) רק לאחר מכן בדוק חלופות עם challenge_hypothesis."
            " אם המזהה לא מופיע ישירות ביעד, זה פער ולא סיום חקירה; המשך לבדוק המשך תפעולי דרך ישות, מחסן, תנועה, תצפית, תקשורת או מיקום.\n"
            "פרוטוקול הרחבת שרשרת מוגבל: בחקירת שרשרת, אל תבדוק קשר ישיר בין העוגן הראשוני לעוגן הסופי כמבחן מסכם לפני שבנית חוליות ביניים."
            " נהל רשימת frontier של אירועים מבטיחים: לאחר trace_identifier, trace_semantic_clues, search_events או find_related_events,"
            " בחר לכל היותר 3 אירועים חדשים בעלי ערך חקירתי גבוה שאינם כבר בשרשרת, והפוך אותם ל-seeds להרחבה נוספת."
            " ערך חקירתי גבוה כולל: מזהה פורמלי, רמז סמנטי תפעולי, תקשורת, סיגינט, תשלום, מחסן, תנועה, מטען מכוסה, תצפית, או קרבה ברורה לעוגן היעד."
            " הרחב עד עומק 3 לכל היותר מהעוגן המקורי, ועד 9 seeds חדשים לכל היותר בכל החקירה."
            " אל תבצע יותר מ-2 קריאות trace_semantic_clues, יותר מ-4 קריאות find_related_events, או יותר מ-6 בדיקות explain_linkage באותה חקירה, אלא אם המשתמש ביקש במפורש להמשיך."
            " בכל סבב הרחבה, העדף הרחבה ממועמד שנמצא כבר כגשר ביניים ולא מחיפוש רחב מקוצץ."
            " אם trace_semantic_clues מחזיר אירועים כמו תשלום, תקשורת, מחסן, תנועה, מטען מכוסה, סיגינט או תצפית,"
            " חובה לבצע לפחות סבב הרחבה אחד מאחד מהם לפני בדיקת challenge_hypothesis או לפני מסקנה שהקשר חלש."
            " אם trace_semantic_clues מחזיר recommended_next_seeds, השתמש בהם כ-frontier המחייב הבא: הרחב עד 3 seeds בלבד, לפי הסדר שהכלי החזיר."
            " אם הוא מחזיר new_clues_to_trace, השתמש בהם בקריאת trace_semantic_clues הבאה, אלא אם כבר הגעת למגבלת 2 קריאות סמנטיות."
            " אל תבחר seeds אחרים מתוך תוצאה רחבה לפני שניסית את recommended_next_seeds או הסברת מדוע הם לא רלוונטיים."
            " אותו כלל חל גם על find_related_events: אם הוא מחזיר recommended_next_seeds, השתמש בהם כ-frontier המחייב הבא לפני מעבר ל-challenge_hypothesis או לסיכום."
            " אל תבנה רצף סופי רק מהעוגנים המקוריים אם find_related_events החזיר seeds מומלצים מסוג תקשורת, תנועה, מחסן, תצפית, סיגינט או מטען מכוסה שלא הורחבו."
            " כלל מחייב: כאשר כלי מחזיר recommended_next_seeds, הקריאה הבאה שאינה explain_linkage חייבת להיות get_events או find_related_events על אותם event_id בדיוק, עד 3 seeds, לפי הסדר שהוחזר."
            " אל תחליף אותם בזרעים אחרים מתוך הרשימה הרחבה, אל תבחר חלופות, ואל תפעיל challenge_hypothesis לפני שבוצעה לפחות קריאת הרחבה אחת על seed מומלץ אחד או יותר."
            " אם seed מומלץ נראה לא רלוונטי, חובה לציין זאת ב-step_bridge ולשלוף אותו עם get_events לפני דחייה."
            " כאשר seeds מומלצים כוללים חוליית ביניים כמו מחסן, תנועה, מטען מכוסה, מצלמה, תצפית או סיגינט, כלול אותם ברצף המועמד עד שבדיקת explain_linkage מראה שאין גשר מספיק."
            " השתמש ב-plan_next_investigation_step כנקודת ביקורת תהליכית: שלח לו objective, candidate_chain_event_ids, pending_recommended_seeds, expanded_seed_event_ids, new_clues_to_trace, linkage_checks_done, semantic_calls_used, related_calls_used ו-tool_budget_remaining."
            " אם הוא מחזיר blocked_tool_families הכוללים challenge_hypothesis או final_summary, אסור להפעיל אותם עד שבוצעה הפעולה שהוא דרש."
            " אם הוא מחזיר required_event_ids, הצעד הבא חייב להשתמש במזהים האלה בדיוק, אלא אם step_bridge מסביר מדוע הם נדחו לאחר get_events."
            " בדוק גשרים עם explain_linkage בין חוליות סמוכות בשרשרת המועמדת, לא רק בין התחלה לסוף."
            " הפעל challenge_hypothesis רק לאחר שנמצא רצף מועמד של לפחות 5 אירועים, או לאחר שני סבבי הרחבה שלא מצאו שום חוליה חדשה."
            " אם הגעת למגבלות העומק או הקריאות, עצור והצג אילו חוליות נמצאו ואילו seeds לא הורחבו.\n"
            "בחקירה עמוקה, אל תשתמש ב-limit קטן כמו 20 לחיפוש רחב לפי מיקום בלבד או לפי אזור כללי."
            " אם החיפוש נועד לבחור עוגני שרשרת מתוך מרחב גדול, השתמש קודם ב-aggregate_events או במסננים מצמצמים כגון זמן, סוג מקור, מילות מפתח, ישות או מזהה."
            " אם בכל זאת נדרש חיפוש רחב, השתמש ב-limit גבוה, עד 500, והבהר ב-step_bridge שזה עדיין מדגם אם התוצאה מקוצצת."
            " כאשר כלי מחזיר truncated=true או total גדול מ-returned, אל תבחר עוגן חקירתי כאילו נבדקו כל הרשומות; בצע צמצום נוסף, אגרגציה, או חיפוש ממוקד לפני בחירת seeds."
            " אל תציג שרשרת כמבוססת אם העוגנים נבחרו רק מתוך תוצאה מקוצצת ללא הצדקה.\n"
            "ב-find_related_events בחקירה עמוקה, אל תשתמש ב-limit=20 או limit=150 להרחבה רחבה. השתמש בדרך כלל ב-limit=500, או צמצם מראש לפי source_types, חלון זמן, מיקום או ממדי קשר."
            " אם total_candidates גדול בהרבה מ-returned, התייחס לתוצאה כמדגם מדורג ולא כבדיקה מלאה; המשך בסינון או בהרחבה נוספת.\n"
            "אם המשתמש מבקש להציג, לשלוף, לסנן, לצמצם, למנות או להראות אירועים/רשומות/תוצאות,"
            " התייחס לכך כבקשת שליפה וסינון. במצב זה החזר את התוצאות הרלוונטיות וסיכום קצר של דרך הסינון,"
            " בלי לבנות תרחיש, בלי לחפש קשרים נסתרים, בלי להציג שרשרת או דפוס, ובלי להפעיל challenge_hypothesis,"
            " אלא אם המשתמש ביקש במפורש דפוס, קשרים, הסבר, חשד, חלופות, מקור התרחיש או רכיב מרכזי.\n"
            "בבקשת שליפה וסינון, השתמש בכלים הדרושים לזיהוי מיקום, חיפוש ושליפת רשומות בלבד,"
            " והעדף תצוגת evidence כאשר מטרת המשתמש היא לראות את האירועים עצמם.\n"
            "כאשר השאלה גאוגרפית או מבקשת מקבצים, ריכוזים, TOP מיקומים, אזורים, מוקדים או 'איפה',"
            " התייחס לכך כתוצאה מרחבית. השתמש ב-aggregate_events עם group_by=location כאשר מתאים,"
            " והחזר לכל מיקום את location_id, שם המיקום ומספר האירועים."
            " בחר תצוגה מומלצת map גם אם אין מזהי אירועים בודדים, והסבר שזו תוצאה אגרגטיבית לפי מיקום."
            " אל תציג היעדר מזהי אירועים ככשל כאשר המשתמש ביקש ריכוזים או מיקומים.\n"
            "אם המשתמש מבקש לחקור דפוס, קשר נסתר, גורמים משותפים, אירועים מקדימים, הסברים חלופיים,"
            " תחילת תרחיש או רכיב מרכזי, התייחס לכך כבקשת חקירה והפעל את תהליך ההרחבה, ההצלבה והביקורת המלא.\n"
            "אל תניח שמזהה מקום או תיאור יחסי ברורים: פתור קודם מיקומים והפניות לאירועים בעזרת הכלים המתאימים.\n"
            "בצע הצלבה בין זמן, מקום, גורם וסוג מקור. הפרד בין עובדות, הסקה וחוסר ודאות.\n"
            "כאשר שם גורם עשוי להיות כינוי או שם מקוצר, השתמש ב-resolve_entity לפני חיפוש היסטוריה."
            " find_actor_history מרחיב אוטומטית את כל הכינויים של ישות מוכרת; בדוק בפלט אילו שמות הורחבו.\n"
            "כאשר מופיע ערך מובחן שעשוי לשמש מזהה חוזר, השתמש ב-trace_identifier כדי לבדוק אם הוא מופיע במקורות נוספים."
            " אל תניח מראש את סוג המזהה או את משמעותו.\n"
            "כאשר trace_identifier משמש לבדיקת אזור, חלון זמן או משפחת מקורות מסוימת, השתמש במסנני start_time, end_time, location_ids ו-source_types"
            " כדי למנוע ערבוב אזכורים רחוקים או לא רלוונטיים.\n"
            "ב-trace_identifier, השאר include_negated=false בכל מעקב רגיל אחר מזהה ובכל ניסיון לבנות את השרשרת הראשית."
            " השתמש ב-include_negated=true רק בבדיקת סתירות, שלילות או חלופות, ורק כאשר אתה מציין שזו מטרת הבדיקה."
            " אל תערבב תוצאות שוללות עם ראיות השרשרת המרכזית.\n"
            "כאשר נמצאה ראיית עוגן משמעותית, השתמש ב-find_related_events להרחבה איטרטיבית."
            " העדף מועמדים עם כמה ממדי קשר והמשך להרחיב מהם עד שהקשרים נחלשים או שאין תוספת מהותית.\n"
            "כאשר אתה בודק משפחת ראיות מסוימת סביב עוגנים שכבר נמצאו, השתמש ב-source_types של find_related_events"
            " כדי לצמצם את ההרחבה לסוגי מקור רלוונטיים, למשל תקשורת, סיגינט, פיננסים, תנועה, תצפית, נמל או מכס."
            " אל תשתמש במסנן זה אם מטרת הצעד היא גילוי רחב; השתמש בו כאשר השאלה או פערי השלמות מצביעים על מקור ראייתי חסר.\n"
            "אל תפעיל challenge_hypothesis מוקדם מדי. בחקירת שרשרת או מזהה, אל תפעיל אותו לפני שבוצע find_related_events אחד לפחות על רשומות העוגן ונבדק לפחות גשר אחד עם explain_linkage, אלא אם היו לפחות שני חיפושים ממוקדים שנכשלו."
            " השתמש בו רק אחרי שנבנתה שרשרת מועמדת עם לפחות 3 עד 5 אירועים תומכים, או אחרי חיפוש מפורש שנכשל ומטרתו לבדוק חלופות."
            " אל תאתגר השערה על בסיס אירוע אחד או שתי רשומות נמל/מכס בלבד אם עדיין לא נבדק המשך תפעולי. הכלי אינו קובע אם ההשערה נכונה.\n"
            "אל תסתפק בתשובה מקומית אם השאלה מבקשת דפוס, קשר נסתר, מקור מוקדם או הסבר. חפש לאחור וקדימה סביב ראיות העוגן.\n"
            "כאשר המשתמש מבקש את תחילת התרחיש, הבחן בין האירוע המוקדם ביותר שכבר נמצא לבין המקור הסיבתי או התפעולי של הרצף."
            " אל תכריז על התחלה לפני שהרחבת לאחור מכל חוליית ביניים משמעותית שנמצאה, לרבות פעולות, קשרים, העברות, נקודות מעבר או שינויים במצב.\n"
            "כאשר המשתמש מבקש לזהות את האובייקט, הישות או הרכיב המרכזי בתרחיש, אל תבחר את המועמד המפורש הראשון בתוצאות."
            " דרוש חיבור רב-שלבי בינו לבין רצף הפעילות באמצעות מזהה, ישות, זמן, מקום או מעבר תפעולי; ציין אם החיבור ישיר או נסיבתי.\n"
            "כאשר רשומה מכילה תוכן סמנטי כגון חפץ, כינוי, מסלול, פעולה או תנאי תזמון,"
            " השתמש ב-trace_semantic_clues עם המונחים שבה כדי לחפש אחורה וקדימה ולעקוב אחר מזהים, ישויות או נקודות תפעוליות שנרמזו בה."
            " השתמש בכלי הזה במיוחד כאשר המעבר בשרשרת אינו מבוסס על מזהה פורמלי אלא על שפה תפעולית כמו חפץ, מטען, מחסן, דרך צדדית, כלי רכב, תזמון או כינוי.\n"
            "אם קיימת תנועה חוקית או שגרתית באותו חלון זמן, אל תניח שהיא התרחיש המרכזי."
            " בדוק האם היא מחוברת לשרשרת או משמשת חלופה, רקע, הסחה או נקודת תזמון שהפעילות האחרת מתרחשת לפניה או אחריה.\n"
            "לפני תשובה על מקור התרחיש או הרכיב המרכזי בו, נסה לבנות שרשרת סיבתית ותפעולית מלאה ככל האפשר:"
            " תנאי מקדים, הכנה, קשר או העברה, שינוי מצב, תנועה או פעולה, ותוצאה."
            " אם חסרה חוליה, הצג אותה כפער והמשך לחפש במקום להשלים אותה בהשערה.\n"
            "לפני הצגת תרחיש רב-מקורי, בצע בדיקת שלמות של סוגי הראיות שעשויים להיות רלוונטיים לשאלה:"
            " תנועה ותצפית, תקשורת ותוכן סמנטי, קשרי ישויות וכינויים, העברות או פעולות מנהליות, ומזהים חוזרים."
            " אין חובה למצוא ראיה מכל סוג, אך חובה לבדוק סוגים סבירים ולציין במפורש אילו נבדקו, אילו נמצאו ואילו חסרים.\n"
            "אל תסתפק בקרבת זמן ומקום כאשר קיימת רשומה בעלת תוכן סמנטי שעשוי להסביר את הרצף."
            " חלץ ממנה מונחים, פעולות, מסלולים ותנאי תזמון, חפש אותם במקורות נוספים, והרחב גם מהאירוע הסמנטי עצמו.\n"
            "לכל מעבר בין שני שלבים בשרשרת, קבע את סוג הגשר הראייתי: מזהה משותף, ישות או כינוי, תוכן סמנטי,"
            " רציפות זמן-מקום, או קשר תפעולי מפורש. אם אין גשר כזה, אל תציג את המעבר כעובדה; סמן אותו כהשערה או כפער.\n"
            "כאשר אתה עומד להציג מעבר חשוב בין שני אירועים בשרשרת, השתמש ב-explain_linkage כדי לבדוק את הגשר הראייתי."
            " אם הכלי מחזיר שאין גשר מספיק, אל תציג את המעבר כעובדה גם אם הוא נראה סביר כרונולוגית.\n"
            "הפרד בין חברי השרשרת לבין אירועי חלופה, רקע או תזמון. אירוע חוקי, שגרתי או מאומת אינו הופך לחלק מהשרשרת"
            " רק משום שהוא סמוך בזמן או במקום; בדוק אם הוא מחובר בגשר ראייתי או דווקא מסביר, סותר או מתזמן את הפעילות האחרת.\n"
            "לאחר זיהוי מועמד לרכיב מרכזי, אל תעצור מיד. בצע סבב הרחבה נוסף משני צדי המועמד ומנקודות המעבר הסמוכות לו,"
            " ובדוק אם קיימות ראיות תקשורתיות, קשרי גורמים, פעולות קודמות או תצפיות מאוחרות שמחזקות או מחלישות את הזיהוי.\n"
            "כל טענה עובדתית מרכזית חייבת לכלול מזהי אירועים מדויקים בסוגריים, לדוגמה (BORD-0001).\n"
            "מבנה תשובת הצ'אט לאנליסט תלוי בפלט classify_question_intent.\n"
            "אם recommended_mode הוא retrieval: כתוב תשובת תוצאה קצרה מאוד, 1 עד 3 משפטים בלבד."
            " ענה ישירות על מה שהתבקש, ציין ספירות, מיקומים או סינון שבוצע, ואל תוסיף ניתוח חקירתי, השערות, חלופות, גשר ראייתי או דפוס נסתר."
            " אם מדובר באגרגציה לפי מיקום, ציין location_id, שם מיקום וספירה. אם מדובר ברשומות, ציין עד 10 מזהי אירועים מרכזיים."
            " אל תכתוב מהלך חקירה, אל תפרט כלים ופרמטרים, ואל תשתמש במבנה עובדה/הסקה/חוסר ודאות.\n"
            "אם recommended_mode הוא investigation: כתוב תשובה קצרה אך חקירתית, 3 עד 6 משפטים."
            " סכם מה נבדק, מה נמצא, מהו הגשר הראייתי או הפער המרכזי, ומה נשאר לא ודאי."
            " אם יש רצף או דפוס, תאר אותו במשפט אחד או שניים בלבד."
            " אל תפרט את כל הצעדים הטכניים, הכלים והפרמטרים; יומן הפעילות בממשק מציג אותם בנפרד.\n"
            "בכל מצב, סיים בשורה קצרה שמתחילה 'מזהי ראיות:' ובה רק מזהי האירועים המרכזיים שעליהם הסתמכת, עד 20 מזהים."
            " אם זו תוצאה אגרגטיבית ללא מזהי אירועים, כתוב 'מזהי ראיות: תוצאה אגרגטיבית ללא מזהי אירועים'.\n"
            "אם באחד מצעדי החקירה התקבלה תוצאה מקוצצת או מדגם מדורג, אל תנסח היעדר ראיה כמסקנה מוחלטת."
            " כתוב במפורש שהבדיקה אינה ממצה ושנדרש צמצום נוסף או הרחבת limit כדי לשלול המשך שרשרת בביטחון גבוה.\n"
            "לאחר שורת הראיות, הוסף שורה אחרונה בפורמט המדויק 'תצוגה מומלצת: VIEW | REASON'.\n"
            "VIEW חייב להתבסס קודם על recommended_view_hint מ-classify_question_intent, אלא אם תוצאות הכלים מצדיקות שינוי ברור."
            " הערכים האפשריים: map כאשר הממצא הגאוגרפי או מסלול התנועה הוא העיקר;"
            " timeline כאשר סדר האירועים והעיתוי הם העיקר; evidence כאשר בדיקת המקורות והרשומות הגולמיות היא העיקר.\n"
            "REASON הוא הסבר קצר בעברית, עד שמונה מילים, לבחירת התצוגה.\n"
            "אין להשתמש בכלי מערכת, קבצים, רשת או shell, ואין לבקש אישור לכלים."
        )
        state_block = self.render_investigation_state(investigation_state)
        full_instructions = f"{instructions}\n\n{state_block}" if state_block else instructions
        safe_investigation_id = re.sub(r"[^A-Za-z0-9_.:-]+", "-", str(investigation_id or "")).strip("-")
        session_id = safe_investigation_id or f"intelligence-orchestrator-{int(time.time() * 1000)}"
        session_started = time.perf_counter()
        with HermesSession(self.config) as session:
            performance["gateway"]["ssh_session_open_ms"] = elapsed_ms(session_started)
            stage_started = time.perf_counter()
            session.ssh_command(f"truncate -s 0 {audit_path}")
            performance["gateway"]["audit_truncate_ms"] = elapsed_ms(stage_started)
            ACTIVE_RUN_STARTED_AT = datetime.now(timezone.utc)
            create_started = time.perf_counter()
            created = session.request("POST", "/v1/runs", {
                "input": prompt,
                "instructions": full_instructions,
                "conversation_history": history[-10:],
                "session_id": session_id,
            })
            created_at = datetime.now(timezone.utc)
            performance["hermes"]["run_create_ms"] = elapsed_ms(create_started)
            run_id = created["run_id"]
            run_wait_started = time.perf_counter()
            deadline = time.time() + 240
            while time.time() < deadline:
                poll_started = time.perf_counter()
                status = session.request("GET", f"/v1/runs/{run_id}")
                performance["hermes"]["poll_count"] += 1
                performance["hermes"]["status_request_total_ms"] += elapsed_ms(poll_started)
                if status.get("status") in TERMINAL_STATUSES:
                    terminal_at = datetime.now(timezone.utc)
                    performance["hermes"]["run_wait_ms"] = elapsed_ms(run_wait_started)
                    if status.get("status") != "completed":
                        raise RuntimeError(status.get("error") or f"Hermes run {status.get('status')}")
                    postprocess_started = time.perf_counter()
                    output = status.get("output", "")
                else:
                    time.sleep(1)
                    continue
                step_pattern = re.compile(
                    r"(?im)^\s*שלב חקירה\s*:\s*([^|\r\n]+?)\s*\|\s*([^|\r\n]+?)\s*\|\s*([^|\r\n]+?)\s*\|\s*([^|\r\n]+?)\s*\|\s*([^|\r\n]+?)\s*\|\s*(.+?)\s*$"
                )
                any_step_line_pattern = re.compile(r"(?im)^\s*שלב חקירה\s*:.*(?:\r?\n|$)")
                investigation_steps = [
                    {
                        "tool": match.group(1).strip(),
                        "observed_clue": match.group(2).strip(),
                        "decision": match.group(3).strip(),
                        "expected_value": match.group(4).strip(),
                        "action": match.group(5).strip(),
                        "result": match.group(6).strip(),
                    }
                    for match in step_pattern.finditer(output)
                ]
                output_without_steps = any_step_line_pattern.sub("", output)
                view_match = re.search(
                    r"(?im)^\s*תצוגה מומלצת\s*:\s*(map|timeline|evidence)(?:\s*\|\s*(.+?))?\s*$",
                    output_without_steps,
                )
                recommended_view = view_match.group(1).lower() if view_match else None
                view_reason = view_match.group(2).strip() if view_match and view_match.group(2) else ""
                clean_output = (
                    (output_without_steps[:view_match.start()] + output_without_steps[view_match.end():]).strip()
                    if view_match else output_without_steps.strip()
                )
                if recommended_view is None:
                    combined = f"{prompt}\n{clean_output}"
                    if re.search(r"רשומ|מקור|ראי|אימות|בדוק|ציטוט", combined):
                        recommended_view, view_reason = "evidence", "בדיקה ישירה של הרשומות המצוטטות"
                    elif re.search(r"רצף|סדר|ציר זמן|לפני|אחרי|עיתוי|שעה", combined):
                        recommended_view, view_reason = "timeline", "העיתוי ורצף האירועים הם העיקר"
                    else:
                        recommended_view, view_reason = "map", "המיקומות והתנועה הם מוקד הממצא"
                event_fetch_started = time.perf_counter()
                event_stream = session.request(
                    "GET",
                    f"/v1/runs/{run_id}/events",
                    timeout=30,
                    parse_json=False,
                )
                performance["gateway"]["event_fetch_ms"] = elapsed_ms(event_fetch_started)
                events = []
                for line in event_stream.splitlines():
                    if not line.startswith("data:"):
                        continue
                    try:
                        event = json.loads(line[5:].strip())
                    except json.JSONDecodeError:
                        continue
                    if event.get("event") in {"tool.started", "tool.completed"}:
                        events.append(event)
                audit_fetch_started = time.perf_counter()
                audit_text = session.ssh_command(f"cat {audit_path} 2>/dev/null || true")
                performance["gateway"]["audit_fetch_ms"] = elapsed_ms(audit_fetch_started)
                audit_records = []
                for line in audit_text.splitlines():
                    try:
                        audit_records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
                exact_steps = self.summarize_audit(audit_records)
                tool_durations = [
                    float(record.get("duration_ms"))
                    for record in audit_records
                    if isinstance(record.get("duration_ms"), (int, float))
                ]
                slowest_record = max(
                    (record for record in audit_records if isinstance(record.get("duration_ms"), (int, float))),
                    key=lambda record: float(record.get("duration_ms")),
                    default=None,
                )
                first_tool_time = min(
                    (parsed for parsed in (parse_utc(record.get("timestamp_utc")) for record in audit_records) if parsed),
                    default=None,
                )
                tool_total_ms = round(sum(tool_durations), 3)
                performance["tools"] = {
                    "tool_call_count": len(audit_records),
                    "tool_execution_total_ms": tool_total_ms,
                    "tool_execution_max_ms": round(max(tool_durations), 3) if tool_durations else 0,
                    "slowest_tool": (
                        {
                            "name": slowest_record.get("tool"),
                            "duration_ms": round(float(slowest_record.get("duration_ms")), 3),
                        }
                        if slowest_record else None
                    ),
                }
                if first_tool_time:
                    performance["hermes"]["time_to_first_tool_ms"] = round((first_tool_time - created_at).total_seconds() * 1000, 3)
                hermes_run_ms = round((terminal_at - created_at).total_seconds() * 1000, 3)
                performance["hermes"]["run_total_ms"] = hermes_run_ms
                performance["hermes"]["model_orchestration_gap_ms"] = round(max(0, hermes_run_ms - tool_total_ms), 3)
                if exact_steps and investigation_steps:
                    for index, step in enumerate(exact_steps):
                        if index >= len(investigation_steps):
                            continue
                        model_step = investigation_steps[index]
                        if model_step.get("tool") != step.get("tool"):
                            continue
                        step["model_explanation"] = {
                            "observed_clue": model_step.get("observed_clue"),
                            "decision": model_step.get("decision"),
                            "expected_value": model_step.get("expected_value"),
                            "action": model_step.get("action"),
                            "result": model_step.get("result"),
                        }
                performance["gateway"]["postprocess_ms"] = elapsed_ms(postprocess_started)
                performance["gateway"]["total_ms"] = elapsed_ms(overall_started)
                performance["summary"] = {
                    "total_user_wait_server_ms": performance["gateway"]["total_ms"],
                    "hermes_run_total_ms": performance["hermes"].get("run_total_ms"),
                    "time_to_first_tool_ms": performance["hermes"].get("time_to_first_tool_ms"),
                    "tool_execution_total_ms": performance["tools"].get("tool_execution_total_ms"),
                    "model_orchestration_gap_ms": performance["hermes"].get("model_orchestration_gap_ms"),
                    "tool_call_count": performance["tools"].get("tool_call_count"),
                    "slowest_tool": performance["tools"].get("slowest_tool"),
                }
                performance_log_path = write_performance_log(run_id, performance, prompt)
                return {
                    "run_id": run_id,
                    "answer": clean_output,
                    "event_ids": sorted(set(EVENT_ID_PATTERN.findall(clean_output))),
                    "recommended_view": recommended_view,
                    "view_reason": view_reason,
                    "investigation_steps": exact_steps or investigation_steps,
                    "events": events,
                    "usage": status.get("usage", {}),
                    "performance_log": performance_log_path.name,
                }
            time.sleep(1)
        raise TimeoutError("Hermes investigation exceeded 240 seconds")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):
        sys.stdout.write("%s - %s\n" % (self.log_date_time_string(), fmt % args))

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()

    def send_json(self, status, value):
        payload = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path == "/api/status":
            self.send_json(200, {"mode": "hermes", "configured": CONFIG_PATH.exists(), "build": APP_BUILD})
            return
        if self.path == "/api/live-steps":
            try:
                config = json.loads(CONFIG_PATH.read_text())
                steps = HermesClient(config).read_live_steps()
                self.send_json(200, {"investigation_steps": steps})
            except Exception as exc:
                self.send_json(502, {"error": str(exc)})
            return
        super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/performance-client":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                request = json.loads(self.rfile.read(length).decode("utf-8"))
                run_id = str(request.get("run_id") or "")
                client_performance = request.get("client") or {}
                updated = update_performance_client(run_id, client_performance)
                self.send_json(200, {"stored": bool(updated), "file": updated.name if updated else None})
            except Exception as exc:
                self.send_json(502, {"error": str(exc)})
            return
        if path != "/api/investigate":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            request = json.loads(self.rfile.read(length).decode("utf-8"))
            prompt = str(request.get("prompt", "")).strip()
            if not prompt:
                self.send_json(400, {"error": "Missing prompt"})
                return
            config = json.loads(CONFIG_PATH.read_text())
            result = HermesClient(config).investigate(
                prompt,
                request.get("history") or [],
                investigation_state=request.get("investigation_state"),
                investigation_id=request.get("investigation_id"),
            )
            self.send_json(200, result)
        except Exception as exc:
            self.send_json(502, {"error": str(exc)})


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8767
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"POC server listening on http://127.0.0.1:{port}/", flush=True)
    server.serve_forever()
