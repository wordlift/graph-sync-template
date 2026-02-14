from __future__ import annotations

import re
from html import unescape

from rdflib import Graph, Literal, URIRef, RDF
from rdflib.namespace import XSD
from lxml import html as lxml_html

from acme_kg.enrichment.youtube import YouTubeEnricher

SCHEMA = "http://schema.org/"


class YouTubePostprocessor:
    """Enrich schema:VideoObject nodes from YouTube Data API metadata."""

    def __init__(self, enricher: YouTubeEnricher | None = None) -> None:
        self._enricher = enricher or YouTubeEnricher()

    def process_graph(self, graph: Graph, context) -> Graph:
        self._materialize_video_nodes_from_html(graph, context)
        video_nodes = list(graph.subjects(RDF.type, URIRef(f"{SCHEMA}VideoObject")))

        for video_uri in video_nodes:
            embed_url = graph.value(video_uri, URIRef(f"{SCHEMA}embedUrl"))
            content_url = graph.value(video_uri, URIRef(f"{SCHEMA}contentUrl"))
            url = str(embed_url or content_url or "")
            video_id = self._extract_youtube_id(url)
            if not video_id:
                continue

            metadata = self._enricher.enrich_video(video_id)
            if not metadata:
                continue

            if metadata.get("title"):
                graph.set(
                    (video_uri, URIRef(f"{SCHEMA}name"), Literal(metadata["title"]))
                )
            if metadata.get("description"):
                graph.set(
                    (
                        video_uri,
                        URIRef(f"{SCHEMA}description"),
                        Literal(metadata["description"]),
                    )
                )
            if metadata.get("thumbnailUrl"):
                graph.set(
                    (
                        video_uri,
                        URIRef(f"{SCHEMA}thumbnailUrl"),
                        URIRef(metadata["thumbnailUrl"]),
                    )
                )
            if metadata.get("publishedAt"):
                graph.set(
                    (
                        video_uri,
                        URIRef(f"{SCHEMA}uploadDate"),
                        Literal(metadata["publishedAt"], datatype=XSD.dateTime),
                    )
                )

        return graph

    def _materialize_video_nodes_from_html(self, graph: Graph, context) -> None:
        response = getattr(context, "response", None)
        web_page = getattr(response, "web_page", None) if response else None
        raw_html = getattr(web_page, "html", None) if web_page else None
        if not isinstance(raw_html, str) or not raw_html.strip():
            return

        page_iri = self._find_page_iri(graph, getattr(context, "url", ""))
        if page_iri is None:
            return

        existing_video_ids: set[str] = set()
        for video_uri in graph.subjects(RDF.type, URIRef(f"{SCHEMA}VideoObject")):
            embed_url = graph.value(video_uri, URIRef(f"{SCHEMA}embedUrl"))
            content_url = graph.value(video_uri, URIRef(f"{SCHEMA}contentUrl"))
            existing_id = self._extract_youtube_id(str(embed_url or content_url or ""))
            if existing_id:
                existing_video_ids.add(existing_id)

        extracted_embed_urls = self._extract_embed_urls(raw_html)
        if not extracted_embed_urls:
            return

        next_index = len(list(graph.subjects(RDF.type, URIRef(f"{SCHEMA}VideoObject"))))
        for embed in extracted_embed_urls:
            video_id = self._extract_youtube_id(embed)
            if not video_id or video_id in existing_video_ids:
                continue
            existing_video_ids.add(video_id)

            next_index += 1
            ids = getattr(context, "ids", None)
            if ids is not None:
                video_iri = ids.new_child(
                    graph,
                    parent=page_iri,
                    type_name="VideoObject",
                    index=next_index,
                    force_index=True,
                    url_value=f"https://www.youtube.com/watch?v={video_id}",
                )
            else:
                video_iri = URIRef(
                    f"{page_iri}/video-objects/video-object-{next_index}"
                )
            graph.add((video_iri, RDF.type, URIRef(f"{SCHEMA}VideoObject")))
            graph.set((video_iri, URIRef(f"{SCHEMA}embedUrl"), URIRef(embed)))
            graph.set(
                (
                    video_iri,
                    URIRef(f"{SCHEMA}contentUrl"),
                    URIRef(f"https://www.youtube.com/watch?v={video_id}"),
                )
            )
            graph.set(
                (
                    video_iri,
                    URIRef(f"{SCHEMA}thumbnailUrl"),
                    URIRef(f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"),
                )
            )
            graph.set((video_iri, URIRef(f"{SCHEMA}mainEntityOfPage"), page_iri))
            graph.add((page_iri, URIRef(f"{SCHEMA}video"), video_iri))

    @staticmethod
    def _find_page_iri(graph: Graph, url: str) -> URIRef | None:
        page_type = URIRef(f"{SCHEMA}WebPage")
        candidates = list(graph.subjects(RDF.type, page_type))
        if len(candidates) == 1:
            return candidates[0]
        if candidates and url:
            for page in candidates:
                current_url = graph.value(page, URIRef(f"{SCHEMA}url"))
                if str(current_url or "") == url:
                    return page
            return candidates[0]

        if url:
            for page in graph.subjects(URIRef(f"{SCHEMA}url"), Literal(url)):
                return page
        return None

    @staticmethod
    def _extract_embed_urls(raw_html: str) -> list[str]:
        urls: list[str] = []
        seen: set[str] = set()

        try:
            root = lxml_html.fromstring(raw_html)
        except Exception:
            root = None

        if root is not None:
            iframe_urls = root.xpath(
                "//iframe[@src and (contains(@src,'youtube.com/embed') or contains(@src,'youtube-nocookie.com/embed'))]/@src"
            )
            for value in iframe_urls:
                normalized = YouTubePostprocessor._canonicalize_embed_url(
                    str(value).strip()
                )
                if normalized and normalized not in seen:
                    seen.add(normalized)
                    urls.append(normalized)

            data_options_values = root.xpath(
                "//*[@data-options and contains(@data-options,'youtube.com/embed')]/@data-options"
            )
            for value in data_options_values:
                for match in re.findall(
                    r"https?://(?:www\.)?youtube(?:-nocookie)?\.com/embed/[0-9A-Za-z_-]{11}(?:[^\s\"'\\]*)?",
                    unescape(str(value)),
                ):
                    normalized = YouTubePostprocessor._canonicalize_embed_url(
                        match.strip()
                    )
                    if normalized and normalized not in seen:
                        seen.add(normalized)
                        urls.append(normalized)

        return urls

    @staticmethod
    def _canonicalize_embed_url(url: str) -> str:
        return url.split("?", 1)[0].split("#", 1)[0].strip()

    @staticmethod
    def _extract_youtube_id(url: str) -> str | None:
        match = re.search(r"(?:v=|/)([0-9A-Za-z_-]{11})(?:[?&].*)?$", url)
        return match.group(1) if match else None
