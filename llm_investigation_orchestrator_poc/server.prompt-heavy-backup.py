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
TERMINAL_STATUSES = {"completed", "failed", "cancelled"}
EVENT_ID_PATTERN = re.compile(r"\b(?:PORT|CUST|FIN|TEL|MOVE|OBS|CAM|SIG|ACOU|BORD|DRONE|MAINT|SOC)-\d{4}\b")
ACTIVE_RUN_STARTED_AT = None
APP_BUILD = "perf-trace-1"


def elapsed_ms(started: float) -> float:
    return round((time.perf_counter() - started) * 1000, 3)


def parse_utc(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


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

        def arg_clue(tool, args):
            if tool in {"resolve_location", "resolve_event_reference", "resolve_entity"}:
                return f'"{args.get("query", "")}"'
            if tool == "trace_identifier":
                return f'המזהה "{args.get("identifier", "")}"'
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
            filters = {key: value for key, value in args.items() if value not in (None, "", [], False)}
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

            if tool == "resolve_location":
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
            if tool == "resolve_location":
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
                outcome = f'נמצאו {result.get("total", len(ids))} רשומות; הוחזרו {result.get("returned", len(ids))}; מזהים: {format_ids(ids)}.'
            elif tool == "get_events":
                requested = args.get("event_ids") or []
                found = [item.get("event_id") for item in result.get("events") or []]
                missing = result.get("missing_event_ids") or []
                action = f'שליפת הרשומות המלאות עבור {len(requested)} מזהים: {format_ids(requested)}.'
                outcome = f'הוחזרו {len(found)} רשומות: {format_ids(found)}; חסרים: {format_ids(missing)}.'
            elif tool == "aggregate_events":
                group_by = args.get("group_by")
                filters = {key: value for key, value in args.items() if key != "group_by" and value not in (None, "", [], False)}
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
            elif tool == "find_related_events":
                seeds = args.get("seed_event_ids") or []
                source_filter = args.get("source_types") or []
                source_text = f' וסוגי מקור {format_ids(source_filter)}' if source_filter else ""
                action = f'הרחבת ראיות העוגן {format_ids(seeds)} לפי {", ".join(args.get("dimensions") or ["entity", "identifier", "time", "location"])}{source_text}.'
                ids = result.get("event_ids") or []
                outcome = f'דורגו {result.get("total_candidates", len(ids))} מועמדים והוחזרו {len(ids)}: {format_ids(ids)}.'
            elif tool == "challenge_hypothesis":
                evidence = args.get("supporting_event_ids") or []
                action = f'בדיקת חלופות ופערים להשערה על בסיס {len(evidence)} אירועים: {format_ids(evidence)}.'
                alternatives = result.get("alternative_event_ids") or []
                gaps = result.get("gaps") or []
                outcome = f'נמצאו {len(alternatives)} אירועי חלופה ו-{len(gaps)} פערים; חלופות: {format_ids(alternatives)}.'
            else:
                action = f'קלט: {json.dumps(args, ensure_ascii=False)}.'
                outcome = f'פלט: {json.dumps(result, ensure_ascii=False)}.'
            steps.append({
                "tool": tool,
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
            "בתחילת כל שאלה, סווג את כוונת המשתמש לפני בחירת הכלים.\n"
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
            "לפני מסקנה משמעותית, השתמש ב-challenge_hypothesis כדי לחפש חלופות תמימות, סתירות ופערים."
            " הכלי אינו קובע אם ההשערה נכונה.\n"
            "אל תסתפק בתשובה מקומית אם השאלה מבקשת דפוס, קשר נסתר, מקור מוקדם או הסבר. חפש לאחור וקדימה סביב ראיות העוגן.\n"
            "כאשר המשתמש מבקש את תחילת התרחיש, הבחן בין האירוע המוקדם ביותר שכבר נמצא לבין המקור הסיבתי או התפעולי של הרצף."
            " אל תכריז על התחלה לפני שהרחבת לאחור מכל חוליית ביניים משמעותית שנמצאה, לרבות פעולות, קשרים, העברות, נקודות מעבר או שינויים במצב.\n"
            "כאשר המשתמש מבקש לזהות את האובייקט, הישות או הרכיב המרכזי בתרחיש, אל תבחר את המועמד המפורש הראשון בתוצאות."
            " דרוש חיבור רב-שלבי בינו לבין רצף הפעילות באמצעות מזהה, ישות, זמן, מקום או מעבר תפעולי; ציין אם החיבור ישיר או נסיבתי.\n"
            "כאשר רשומה מכילה תוכן סמנטי כגון חפץ, כינוי, מסלול, פעולה או תנאי תזמון,"
            " השתמש במונחים שבה כדי לחפש אחורה וקדימה ולעקוב אחר מזהים, ישויות או נקודות תפעוליות שנרמזו בה.\n"
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
            "לפני ניסוח התשובה הסופית, ערוך ביקורת שלמות קצרה: האם קיימת חוליית הכנה, חוליית קשר או העברה, חוליית תנועה או פעולה,"
            " ותוצאה; האם לכל חיבור יש גשר ראייתי; והאם חלופות נשמרו מחוץ לשרשרת אלא אם הוכח אחרת.\n"
            "כל טענה עובדתית מרכזית חייבת לכלול מזהי אירועים מדויקים בסוגריים, לדוגמה (BORD-0001).\n"
            "מבנה תשובת הצ'אט לאנליסט: אל תציג בה את שורות 'שלב חקירה'. הן מיועדות ליומן הפעילות בלבד."
            " התשובה הגלויה צריכה לסכם את תהליך החקירה בשפה טבעית: מאיזו נקודת עוגן התחלת, אילו כיווני בדיקה פתחת,"
            " איזה רמז העביר אותך לכיוון הבא, מה נמצא, ומה נשאר לא ודאי.\n"
            "פתח את התשובה בפסקה קצרה של 'מה עשיתי בחקירה' ולאחריה 'מה מצאתי'."
            " אחר כך הצג את השרשרת או הדפוס אם נמצא, עם סוגי הגשרים הראייתיים בין החוליות."
            " לאחר מכן הצג חלופות, פערים וחוסר ודאות. אל תכתוב רשימת כלים טכנית בגוף הצ'אט.\n"
            "אם השאלה היא שאלת המשך, התייחס בקצרה להקשר הקודם והסבר איך הצעד הנוכחי מצמצם, מרחיב או משנה את החקירה.\n"
            "לפני שורת 'מזהי ראיות', הוסף שורת ביקורת אחת עבור כל הפעלת כלי MCP שביצעת, לפי סדר הביצוע.\n"
            "כל שורת ביקורת חייבת להיות הסבר ציבורי ותפעולי בלבד, לא מחשבות פנימיות ולא שרשרת-מחשבה נסתרת.\n"
            "כל שורה חייבת להיות בפורמט המדויק: 'שלב חקירה: TOOL | OBSERVED_CLUE | DECISION | EXPECTED_VALUE | ACTION | RESULT'.\n"
            "TOOL הוא שם כלי ה-MCP ללא הקידומת mcp_intelligence_events_poc_.\n"
            "OBSERVED_CLUE הוא הרמז הגלוי מהשאלה או מפלט הכלים הקודמים שהוביל לצעד הזה; אם זה הצעד הראשון, כתוב את הביטוי או ההפניה מהשאלה.\n"
            "DECISION הוא הסבר קצר למה הפעולה הזו היא הצעד הבא, במונחי חקירה בלבד ובהסתמך רק על ראיות שכבר הוחזרו.\n"
            "EXPECTED_VALUE הוא מה הפעולה אמורה לאמת, לשלול או לצמצם.\n"
            "ACTION חייב לתאר במדויק את הקלט: הטקסט שפוענח, מזהי המיקום, חלון הזמן, הגורם, סוג המקור, מזהי האירועים או סדר המיון."
            " אין לכתוב ניסוח כללי כגון 'בוצע חיפוש'.\n"
            "RESULT חייב לתאר תוצאה בדיקה קונקרטית: מזהים שנפתרו, מספר רשומות, טווח זמנים, מזהי אירועים שנבחרו או העובדה שלא נמצאו התאמות."
            " אל תמציא פרמטרים או תוצאות שלא הופיעו בפלט הכלים.\n"
            "סיים בשורה קצרה שמתחילה 'מזהי ראיות:' ובה רשימת כל מזהי האירועים שעליהם הסתמכת.\n"
            "לאחר שורת הראיות, הוסף שורה אחרונה בפורמט המדויק 'תצוגה מומלצת: VIEW | REASON'.\n"
            "VIEW חייב להיות אחד בלבד: map כאשר הממצא הגאוגרפי או מסלול התנועה הוא העיקר;"
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
                return {
                    "run_id": run_id,
                    "answer": clean_output,
                    "event_ids": sorted(set(EVENT_ID_PATTERN.findall(clean_output))),
                    "recommended_view": recommended_view,
                    "view_reason": view_reason,
                    "investigation_steps": exact_steps or investigation_steps,
                    "events": events,
                    "usage": status.get("usage", {}),
                    "performance": performance,
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
        if urlparse(self.path).path != "/api/investigate":
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
