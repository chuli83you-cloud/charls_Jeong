#!/usr/bin/env python3
import html
import re
from collections import Counter
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

STOPWORDS = {
    "그리고", "하지만", "그러나", "또한", "정말", "아주", "너무", "같은", "대한", "에서", "으로", "에게",
    "있는", "하는", "했다", "합니다", "이다", "입니다", "그", "이", "저", "것", "수", "등",
    "the", "and", "for", "with", "that", "this", "are", "was", "were", "from", "have", "has", "had",
}


def split_sentences(text: str):
    raw = re.split(r"(?<=[.!?。！？\n])\s+", text.strip())
    return [s.strip() for s in raw if s.strip()]


def tokenize(text: str):
    tokens = re.findall(r"[가-힣A-Za-z]{2,}", text.lower())
    return [t for t in tokens if t not in STOPWORDS]


def extract_topics(text: str, n_topics: int = 5):
    freq = Counter(tokenize(text))
    topics = [w for w, _ in freq.most_common(n_topics)]
    while len(topics) < n_topics:
        topics.append(f"핵심 인사이트 {len(topics) + 1}")
    return topics


def pick_support_sentences(sentences, topic: str, k: int = 3):
    scored = []
    for s in sentences:
        score = s.lower().count(topic.lower())
        if score:
            scored.append((score, s))
    scored.sort(key=lambda x: x[0], reverse=True)
    selected = [s for _, s in scored[:k]]
    if len(selected) < k:
        for s in sentences:
            if s not in selected:
                selected.append(s)
            if len(selected) == k:
                break
    return selected


def shorten(text: str, limit: int = 180):
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def generate_thread(topic: str, support):
    return [
        f"[주제: {topic}] 블로그 글에서 뽑은 핵심을 스레드로 정리합니다.",
        f"1) 왜 중요한가? {shorten(support[0], 160)}",
        f"2) 핵심 포인트 {shorten(support[1], 160)}",
        f"3) 바로 적용하기 {shorten(support[2], 160)}",
        "4) 체크리스트: 오늘 행동 1가지 정하기 → 기록하기 → 1주 뒤 개선하기",
        f"5) 한 줄 결론: '{topic}'는 실행의 기준입니다.",
    ]


def render_page(blog_text="", result_html=""):
    escaped_text = html.escape(blog_text)
    return f"""<!doctype html>
<html lang='ko'>
<head>
  <meta charset='utf-8'/>
  <meta name='viewport' content='width=device-width, initial-scale=1'/>
  <title>블로그→스레드 5개 생성기</title>
  <style>
    body {{ font-family: sans-serif; max-width: 960px; margin: 2rem auto; padding: 0 1rem; }}
    textarea {{ width: 100%; min-height: 260px; }}
    button {{ margin-top: 1rem; padding: .6rem 1rem; }}
    .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 1rem; margin-top: 1rem; }}
    pre {{ background:#f6f8fa; padding:.8rem; border-radius:6px; white-space:pre-wrap; }}
  </style>
</head>
<body>
  <h1>🧵 블로그 글 → 주제별 스레드 5개 생성기</h1>
  <p>블로그 원문을 붙여 넣으면 서로 다른 주제로 스레드 5개를 생성합니다.</p>
  <form method='post'>
    <textarea name='blog_text' placeholder='여기에 블로그 글 전체를 입력하세요...'>{escaped_text}</textarea><br/>
    <button type='submit'>스레드 만들기</button>
  </form>
  {result_html}
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, body: str):
        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self._send(render_page())

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        payload = self.rfile.read(content_length).decode("utf-8")
        blog_text = parse_qs(payload).get("blog_text", [""])[0]

        if len(blog_text.strip()) < 100:
            result = "<div class='card'><strong>100자 이상 입력해 주세요.</strong></div>"
            self._send(render_page(blog_text, result))
            return

        sentences = split_sentences(blog_text)
        topics = extract_topics(blog_text, 5)

        blocks = ["<h2>생성 결과</h2>"]
        for i, topic in enumerate(topics, 1):
            support = pick_support_sentences(sentences, topic, 3)
            thread = generate_thread(topic, support)
            posts = "\n\n".join(f"[{idx}] {html.escape(t)}" for idx, t in enumerate(thread, 1))
            blocks.append(f"<div class='card'><h3>스레드 {i}: {html.escape(topic)}</h3><pre>{posts}</pre></div>")

        self._send(render_page(blog_text, "".join(blocks)))


def run():
    server = HTTPServer(("0.0.0.0", 8000), Handler)
    print("Server running on http://0.0.0.0:8000")
    server.serve_forever()


if __name__ == "__main__":
    run()
