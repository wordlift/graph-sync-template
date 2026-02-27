from __future__ import annotations

from dataclasses import dataclass
import io
import json
from pathlib import Path
import sys
from urllib.error import HTTPError

from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import XSD

sys.path.insert(0, str((Path.cwd() / "src").resolve()))

from acme_kg.enrichment.youtube import YouTubeEnricher
from acme_kg.postprocessors.youtube import SCHEMA, YouTubePostprocessor


@dataclass
class _WebPage:
    html: str | None


@dataclass
class _Response:
    web_page: _WebPage | None


@dataclass
class _Context:
    url: str = ""
    response: _Response | None = None
    ids: object | None = None


class _Ids:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def new_child(self, graph: Graph, **kwargs) -> URIRef:
        self.calls.append(kwargs)
        parent = kwargs["parent"]
        index = kwargs["index"]
        return URIRef(f"{parent}/video-objects/video-object-{index}")


class _StubEnricher:
    def __init__(self, values: dict[str, dict[str, str] | None]) -> None:
        self.values = values
        self.calls: list[str] = []

    def enrich_video(self, video_id: str):
        self.calls.append(video_id)
        return self.values.get(video_id)


class _FakeResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self._payload = payload

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_enricher_warns_and_skips_without_api_key(caplog) -> None:
    enricher = YouTubeEnricher(api_key=None)
    with caplog.at_level("WARNING"):
        assert enricher.enrich_video("abc123def45") is None
    assert "YOUTUBE_API_KEY is not configured" in caplog.text


def test_enricher_successful_response(monkeypatch) -> None:
    payload = {
        "items": [
            {
                "snippet": {
                    "title": "Video title",
                    "description": "Video description",
                    "publishedAt": "2026-01-01T00:00:00Z",
                    "thumbnails": {"high": {"url": "https://img.example/high.jpg"}},
                }
            }
        ]
    }
    monkeypatch.setattr(
        "acme_kg.enrichment.youtube.urllib.request.urlopen",
        lambda *args, **kwargs: _FakeResponse(payload),
    )

    enricher = YouTubeEnricher(api_key="key")
    result = enricher.enrich_video("abc123def45")
    assert result == {
        "title": "Video title",
        "description": "Video description",
        "thumbnailUrl": "https://img.example/high.jpg",
        "publishedAt": "2026-01-01T00:00:00Z",
    }


def test_enricher_no_items_warns(monkeypatch, caplog) -> None:
    monkeypatch.setattr(
        "acme_kg.enrichment.youtube.urllib.request.urlopen",
        lambda *args, **kwargs: _FakeResponse({"items": []}),
    )
    enricher = YouTubeEnricher(api_key="key")
    with caplog.at_level("WARNING"):
        assert enricher.enrich_video("abc123def45") is None
    assert "No YouTube data found" in caplog.text


def test_enricher_http_error(monkeypatch, caplog) -> None:
    def _raise_http_error(*args, **kwargs):
        raise HTTPError(
            url="https://www.googleapis.com/youtube/v3/videos",
            code=403,
            msg="Forbidden",
            hdrs=None,
            fp=io.BytesIO(b""),
        )

    monkeypatch.setattr(
        "acme_kg.enrichment.youtube.urllib.request.urlopen",
        _raise_http_error,
    )
    enricher = YouTubeEnricher(api_key="key")
    with caplog.at_level("ERROR"):
        assert enricher.enrich_video("abc123def45") is None
    assert "YouTube API HTTP error" in caplog.text


def test_enricher_generic_error(monkeypatch, caplog) -> None:
    monkeypatch.setattr(
        "acme_kg.enrichment.youtube.urllib.request.urlopen",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("boom")),
    )
    enricher = YouTubeEnricher(api_key="key")
    with caplog.at_level("ERROR"):
        assert enricher.enrich_video("abc123def45") is None
    assert "Error fetching YouTube metadata" in caplog.text


def test_extract_and_canonicalize_helpers() -> None:
    assert (
        YouTubePostprocessor._canonicalize_embed_url(" https://x/y?id=1#f ")
        == "https://x/y"
    )
    assert (
        YouTubePostprocessor._extract_youtube_id("https://www.youtube.com/watch?v=abc123def45")
        == "abc123def45"
    )
    assert (
        YouTubePostprocessor._extract_youtube_id("https://www.youtube.com/embed/abc123def45")
        == "abc123def45"
    )
    assert YouTubePostprocessor._extract_youtube_id("https://example.com/video") is None


def test_extract_embed_urls_from_html_and_data_options() -> None:
    html = """
    <html><body>
      <iframe src="https://www.youtube.com/embed/abc123def45?autoplay=1"></iframe>
      <iframe src="https://www.youtube-nocookie.com/embed/abc123def45#t=1"></iframe>
      <div data-options="video=https://www.youtube.com/embed/zzz999yyy88&amp;foo=bar"></div>
    </body></html>
    """
    urls = YouTubePostprocessor._extract_embed_urls(html)
    assert urls == [
        "https://www.youtube.com/embed/abc123def45",
        "https://www.youtube-nocookie.com/embed/abc123def45",
        "https://www.youtube.com/embed/zzz999yyy88&foo=bar",
    ]


def test_extract_embed_urls_handles_invalid_html() -> None:
    assert YouTubePostprocessor._extract_embed_urls("\x00\x00\x00") == []


def test_find_page_iri_variants() -> None:
    graph = Graph()
    page_type = URIRef(f"{SCHEMA}WebPage")
    p1 = URIRef("https://example.com/p1")
    p2 = URIRef("https://example.com/p2")
    graph.add((p1, RDF.type, page_type))
    graph.add((p2, RDF.type, page_type))
    graph.set((p2, URIRef(f"{SCHEMA}url"), Literal("https://example.com/page")))
    assert YouTubePostprocessor._find_page_iri(graph, "https://example.com/page") == p2
    assert YouTubePostprocessor._find_page_iri(graph, "https://missing.example/page") == p1

    graph2 = Graph()
    page3 = URIRef("https://example.com/page3")
    graph2.set((page3, URIRef(f"{SCHEMA}url"), Literal("https://literal.example/page")))
    assert YouTubePostprocessor._find_page_iri(graph2, "https://literal.example/page") == page3
    assert YouTubePostprocessor._find_page_iri(Graph(), "") is None


def test_materialize_video_nodes_with_ids_and_duplicate_filtering() -> None:
    graph = Graph()
    page = URIRef("https://example.com/page")
    graph.add((page, RDF.type, URIRef(f"{SCHEMA}WebPage")))
    graph.set((page, URIRef(f"{SCHEMA}url"), Literal("https://example.com/page")))

    existing_video = URIRef("https://example.com/page/video-objects/video-object-1")
    graph.add((existing_video, RDF.type, URIRef(f"{SCHEMA}VideoObject")))
    graph.set(
        (existing_video, URIRef(f"{SCHEMA}embedUrl"), URIRef("https://www.youtube.com/embed/abc123def45"))
    )

    ids = _Ids()
    context = _Context(
        url="https://example.com/page",
        response=_Response(
            _WebPage(
                '<iframe src="https://www.youtube.com/embed/abc123def45"></iframe>'
                '<iframe src="https://www.youtube.com/embed/zzz999yyy88"></iframe>'
            )
        ),
        ids=ids,
    )

    processor = YouTubePostprocessor(enricher=_StubEnricher({}))
    processor._materialize_video_nodes_from_html(graph, context)

    video_objects = list(graph.subjects(RDF.type, URIRef(f"{SCHEMA}VideoObject")))
    assert len(video_objects) == 2
    assert len(ids.calls) == 1
    assert ids.calls[0]["force_index"] is True
    assert ids.calls[0]["type_name"] == "VideoObject"


def test_materialize_video_nodes_without_ids_and_no_page_match() -> None:
    graph = Graph()
    page = URIRef("https://example.com/page")
    graph.add((page, RDF.type, URIRef(f"{SCHEMA}WebPage")))
    graph.set((page, URIRef(f"{SCHEMA}url"), Literal("https://example.com/page")))
    context = _Context(
        url="https://wrong.example/page",
        response=_Response(_WebPage('<iframe src="https://www.youtube.com/embed/abc123def45"></iframe>')),
        ids=None,
    )

    processor = YouTubePostprocessor(enricher=_StubEnricher({}))
    processor._materialize_video_nodes_from_html(graph, context)
    created = list(graph.subjects(RDF.type, URIRef(f"{SCHEMA}VideoObject")))
    assert len(created) == 1
    assert str(created[0]).endswith("/video-objects/video-object-1")

    graph2 = Graph()
    processor._materialize_video_nodes_from_html(
        graph2,
        _Context(
            url="https://example.com/page",
            response=_Response(_WebPage('<iframe src="https://www.youtube.com/embed/abc123def45"></iframe>')),
        ),
    )
    assert not list(graph2.subjects(RDF.type, URIRef(f"{SCHEMA}VideoObject")))

    graph3 = Graph()
    graph3.add((page, RDF.type, URIRef(f"{SCHEMA}WebPage")))
    processor._materialize_video_nodes_from_html(graph3, _Context(url="", response=_Response(_WebPage("   "))))
    assert not list(graph3.subjects(RDF.type, URIRef(f"{SCHEMA}VideoObject")))


def test_process_graph_enriches_video_nodes_and_skips_non_youtube_urls() -> None:
    graph = Graph()
    page = URIRef("https://example.com/page")
    graph.add((page, RDF.type, URIRef(f"{SCHEMA}WebPage")))
    graph.set((page, URIRef(f"{SCHEMA}url"), Literal("https://example.com/page")))

    video = URIRef("https://example.com/page/video-objects/video-object-1")
    graph.add((video, RDF.type, URIRef(f"{SCHEMA}VideoObject")))
    graph.set(
        (video, URIRef(f"{SCHEMA}embedUrl"), URIRef("https://www.youtube.com/embed/abc123def45"))
    )

    fallback_video = URIRef("https://example.com/page/video-objects/video-object-2")
    graph.add((fallback_video, RDF.type, URIRef(f"{SCHEMA}VideoObject")))
    graph.set(
        (fallback_video, URIRef(f"{SCHEMA}contentUrl"), URIRef("https://www.youtube.com/watch?v=zzz999yyy88"))
    )

    non_youtube = URIRef("https://example.com/page/video-objects/video-object-3")
    graph.add((non_youtube, RDF.type, URIRef(f"{SCHEMA}VideoObject")))
    graph.set((non_youtube, URIRef(f"{SCHEMA}embedUrl"), URIRef("https://example.com/embed/local")))

    stub = _StubEnricher(
        {
            "abc123def45": {
                "title": "Video title",
                "description": "Video description",
                "thumbnailUrl": "https://img.example/thumb.jpg",
                "publishedAt": "2026-01-01T00:00:00Z",
            },
            "zzz999yyy88": {"title": "Only title"},
        }
    )
    processor = YouTubePostprocessor(enricher=stub)
    result = processor.process_graph(graph, _Context(url="https://example.com/page", response=_Response(_WebPage(None))))
    assert result is graph

    assert stub.calls == ["abc123def45", "zzz999yyy88"]
    assert graph.value(video, URIRef(f"{SCHEMA}name")) == Literal("Video title")
    assert graph.value(video, URIRef(f"{SCHEMA}description")) == Literal("Video description")
    assert graph.value(video, URIRef(f"{SCHEMA}thumbnailUrl")) == URIRef("https://img.example/thumb.jpg")
    assert graph.value(video, URIRef(f"{SCHEMA}uploadDate")) == Literal(
        "2026-01-01T00:00:00Z", datatype=XSD.dateTime
    )
    assert graph.value(fallback_video, URIRef(f"{SCHEMA}name")) == Literal("Only title")
    assert graph.value(fallback_video, URIRef(f"{SCHEMA}description")) is None
