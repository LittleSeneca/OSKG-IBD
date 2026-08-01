#!/usr/bin/env python3
"""
Phase 4: Structural Analysis for OSKG-IBD
Five analyses: hinge inventory, cascade trees, convergence points,
contradiction clusters, structural gaps.

Inputs:
  - notes/claims/*.md (claim metadata: frontmatter + edges section)
  - scripts/manifests/phase3_edges/combined.json (canonical edge set)

Outputs:
  - scripts/phase4_analysis_output.txt (human-readable report)
  - scripts/phase4_analysis.json (machine-readable summary)

Pure stdlib -- no NetworkX.
"""

import json
import os
import re
from collections import defaultdict, deque
from pathlib import Path

import yaml

# ── Paths ──────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLAIMS_DIR = PROJECT_ROOT / "notes" / "claims"
EDGE_FILE = PROJECT_ROOT / "scripts" / "manifests" / "phase3_edges" / "combined.json"
OUTPUT_JSON = PROJECT_ROOT / "scripts" / "phase4_analysis.json"
OUTPUT_TXT = PROJECT_ROOT / "scripts" / "phase4_analysis_output.txt"

# ── Helpers ────────────────────────────────────────────────────────────

def parse_frontmatter(text):
    """Parse YAML frontmatter from a markdown file. Returns dict or None."""
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1))
    except Exception:
        return None

def parse_edges_from_claim(text, slug):
    """Parse the ## Edges section of a claim file for wikilinks.
    Returns dict: {edge_type: [(target_slug, rationale), ...]}"""
    edges_section = re.search(r'## Edges\s*\n(.*?)(?:\n## |\n---|\Z)', text, re.DOTALL)
    if not edges_section:
        return {}
    body = edges_section.group(1)
    # Edge types we track
    edge_map = {}
    current_type = None
    for line in body.split('\n'):
        # Detect edge type headers
        m_type = re.match(r'\*\*(Depends on|Supports|Extends|Operationalizes|Challenged by|Contradicts):?\*\*', line)
        if m_type:
            raw = m_type.group(1).strip(':')
            # Normalize to snake_case
            current_type = raw.lower().replace(' ', '_')
            edge_map[current_type] = []
            continue
        # Detect wikilinks
        m_link = re.findall(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', line)
        if m_link and current_type:
            for target, rationale in m_link:
                edge_map.setdefault(current_type, []).append((target.strip(), rationale.strip() if rationale else ''))
    # Normalize edge type names from claim files to canonical
    canonical = {}
    for etype, links in edge_map.items():
        if etype in ('supports', 'extends', 'depends_on', 'operationalizes', 'challenged_by', 'contradicts'):
            canonical[etype] = links
        elif etype == 'challenged_by':
            canonical['challenged_by'] = links
    return canonical

def load_claim_metadata():
    """Load all claim files, extract metadata and edges. Returns dict slug->data."""
    claims = {}
    for fpath in sorted(CLAIMS_DIR.glob("claim-*.md")):
        slug = fpath.stem  # filename without .md
        text = fpath.read_text(encoding='utf-8')
        fm = parse_frontmatter(text)
        if not fm:
            continue
        # Validate: must have type/claim tag and non-empty claim_id
        tags = fm.get('tags', [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(',')]
        if 'type/claim' not in tags:
            continue
        claim_id = fm.get('claim_id', '')
        if not claim_id:
            continue
        status = fm.get('status', 'active')
        if status != 'active':
            continue

        statement = fm.get('statement', '')
        # Truncate long statements
        if len(statement) > 200:
            statement = statement[:197] + '...'

        claims[slug] = {
            'slug': slug,
            'claim_id': claim_id,
            'statement': statement,
            'confidence': fm.get('confidence', 'unknown'),
            'source_note': fm.get('source_note', ''),
            'claim_type': fm.get('claim_type', ''),
            'tags': tags,
            'edges_from_file': parse_edges_from_claim(text, slug),
        }
    return claims

def load_canonical_edges():
    """Load canonical edge set from Phase 3 combined.json."""
    if not EDGE_FILE.exists():
        print(f"WARNING: Edge file not found at {EDGE_FILE}")
        return []
    with open(EDGE_FILE, 'r', encoding='utf-8') as f:
        raw = json.load(f)
    edges = []
    for e in raw:
        edges.append({
            'claim_a': e['claim_a'],
            'claim_b': e['claim_b'],
            'edge_type': e['edge_type'],
            'rationale': e.get('rationale', ''),
        })
    return edges

def build_graph(claims, canonical_edges):
    """Build adjacency graph from canonical edges + claim metadata.
    Returns dict: graph[slug] = {
        'meta': {...},
        'out_edges': {target_slug: set(edge_types)},
        'in_edges': {source_slug: set(edge_types)},
    }
    """
    graph = {}
    for slug, meta in claims.items():
        graph[slug] = {
            'meta': meta,
            'out_edges': defaultdict(set),
            'in_edges': defaultdict(set),
        }

    for e in canonical_edges:
        a, b, etype = e['claim_a'], e['claim_b'], e['edge_type']
        # Only add if both claims exist
        if a not in graph or b not in graph:
            continue
        graph[a]['out_edges'][b].add(etype)
        graph[b]['in_edges'][a].add(etype)

    return graph

# ── Analysis 1: Hinge Inventory ────────────────────────────────────────

def _brandes_betweenness(graph, undirected=True):
    """Brandes' algorithm for betweenness centrality on undirected projection.
    Returns dict slug->betweenness_score."""
    nodes = list(graph.keys())
    n = len(nodes)
    node_idx = {node: i for i, node in enumerate(nodes)}

    # Build adjacency list (undirected)
    adj = [[] for _ in range(n)]
    for slug, data in graph.items():
        u = node_idx[slug]
        for target in data['out_edges']:
            v = node_idx.get(target)
            if v is not None:
                adj[u].append(v)
                adj[v].append(u)  # undirected
        for source in data['in_edges']:
            v = node_idx.get(source)
            if v is not None:
                adj[u].append(v)
                adj[v].append(u)

    betweenness = {slug: 0.0 for slug in nodes}

    for s in range(n):
        # Single-source shortest paths
        S = []
        P = [[] for _ in range(n)]
        sigma = [0] * n
        sigma[s] = 1
        d = [-1] * n
        d[s] = 0
        Q = deque([s])

        while Q:
            v = Q.popleft()
            S.append(v)
            for w in adj[v]:
                if d[w] < 0:
                    Q.append(w)
                    d[w] = d[v] + 1
                if d[w] == d[v] + 1:
                    sigma[w] += sigma[v]
                    P[w].append(v)

        # Back-propagation
        delta = [0.0] * n
        while S:
            w = S.pop()
            for v in P[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
            if w != s:
                betweenness[nodes[w]] += delta[w]

    # Brandes returns twice the undirected betweenness for directed graphs
    # Normalize for undirected
    norm = 1.0 / ((n - 1) * (n - 2)) if n > 2 else 1.0
    for slug in betweenness:
        betweenness[slug] *= norm

    return betweenness

def hinge_inventory(graph):
    """Top 15 claims by edge_count * betweenness_centrality."""
    betweenness = _brandes_betweenness(graph, undirected=True)

    scored = []
    for slug, data in graph.items():
        out_deg = len(data['out_edges'])
        in_deg = len(data['in_edges'])
        total_deg = out_deg + in_deg
        bc = betweenness.get(slug, 0.0)
        score = total_deg * bc

        # Count direct dependents (reachable via supports/extends/depends_on outbound)
        dependents = set()
        for target, etypes in data['out_edges'].items():
            if etypes & {'supports', 'extends', 'depends_on'}:
                dependents.add(target)

        meta = data['meta']
        scored.append({
            'slug': slug,
            'claim_id': meta['claim_id'],
            'statement': meta['statement'][:150] if len(meta['statement']) > 150 else meta['statement'],
            'score': round(score, 4),
            'degree': total_deg,
            'betweenness': round(bc, 6),
            'confidence': meta['confidence'],
            'source_note': meta['source_note'],
            'topics': [t for t in meta.get('tags', []) if t.startswith('topic/')],
            'direct_dependents': len(dependents),
        })

    scored.sort(key=lambda x: x['score'], reverse=True)
    return scored[:15]

# ── Analysis 2: Cascade Trees ──────────────────────────────────────────

def cascade_trees(graph, hinges, depth=3, top_n=6):
    """Build downstream cascade trees for top N hinges."""
    trees = []
    for h in hinges[:top_n]:
        slug = h['slug']
        meta = graph[slug]['meta']
        tree_lines = []
        tree_lines.append(f"## Cascade: {meta['claim_id']} ({slug})")
        statement = meta['statement']
        if len(statement) > 120:
            statement = statement[:117] + '...'
        tree_lines.append(f"**{statement}**")
        tree_lines.append(f"Confidence: {meta['confidence']} | Source: {meta['source_note']}")
        tree_lines.append('')

        # BFS following outgoing supports, extends, depends_on
        seen = {slug}
        queue = deque()
        for target, etypes in graph[slug]['out_edges'].items():
            active = [et for et in etypes if et in ('supports', 'extends', 'depends_on')]
            if active:
                queue.append((target, 1, active))
                seen.add(target)

        children_map = {slug: []}
        tree_nodes = []

        while queue:
            current, d, etypes = queue.popleft()
            if d > depth:
                continue
            edge_abbrev = '/'.join(sorted({'sup': 'supports', 'ext': 'extends', 'dep': 'depends_on'}.get(et[:3], et[:3]) for et in etypes))
            cm = graph.get(current, {})
            cm_meta = cm.get('meta', {})
            stmt = cm_meta.get('statement', '')
            if len(stmt) > 100:
                stmt = stmt[:97] + '...'
            tree_nodes.append({
                'slug': current,
                'depth': d,
                'edge_abbrev': edge_abbrev,
                'statement': stmt,
            })

            if current in graph:
                for target, ets in graph[current]['out_edges'].items():
                    if target not in seen:
                        active = [et for et in ets if et in ('supports', 'extends', 'depends_on')]
                        if active:
                            seen.add(target)
                            queue.append((target, d + 1, active))

        # Render tree structure
        def render_tree(nodes):
            """Render tree nodes into Unicode tree lines."""
            lines = []
            # Group nodes by depth
            prev_depth = 0
            stack = []  # stack of (prefix, is_last) for each depth level
            for i, node in enumerate(nodes):
                d = node['depth']
                # Determine if this is the last sibling at this depth
                # Look ahead: find next node at same depth
                is_last = True
                for j in range(i + 1, len(nodes)):
                    if nodes[j]['depth'] <= d:
                        if nodes[j]['depth'] < d:
                            is_last = True
                        else:
                            is_last = False
                        break
                # Build prefix
                prefix_parts = []
                for sd, slast in stack:
                    prefix_parts.append('   ' if slast else '│  ')
                connector = '└── ' if is_last else '├── '
                # Update stack
                while stack and stack[-1][0] >= d:
                    stack.pop()
                stack.append((d, is_last))

                prefix = ''.join(prefix_parts)
                lines.append(f"{prefix}{connector}({node['edge_abbrev']}) {node['statement']}")
            return lines

        tree_lines.extend(render_tree(tree_nodes))
        tree_lines.append('')
        trees.append('\n'.join(tree_lines))

    return '\n'.join(trees)

# ── Analysis 3: Convergence Points ─────────────────────────────────────

def convergence_points(graph):
    """Claims where 5+ unique source_notes independently support the claim."""
    results = []
    for slug, data in graph.items():
        supporters = defaultdict(set)  # source_note -> set of supporter slugs
        contradictions = []
        for source_slug, etypes in data['in_edges'].items():
            if etypes & {'supports', 'extends'}:
                src_meta = graph.get(source_slug, {}).get('meta', {})
                src_note = src_meta.get('source_note', '').replace('[[', '').replace(']]', '')
                if src_note:
                    supporters[src_note].add(source_slug)
            if 'contradicts' in etypes:
                contradictions.append(source_slug)

        unique_sources = len(supporters)
        if unique_sources >= 3:  # Lower threshold for IBD domain (less consensus)
            total = sum(len(v) for v in supporters.values())
            meta = data['meta']
            results.append({
                'slug': slug,
                'claim_id': meta['claim_id'],
                'statement': meta['statement'][:150] if len(meta['statement']) > 150 else meta['statement'],
                'confidence': meta['confidence'],
                'unique_sources': unique_sources,
                'total_supporters': total,
                'contradiction_count': len(contradictions),
                'source_list': sorted(list(supporters.keys())),
            })

    results.sort(key=lambda x: (-x['unique_sources'], -x['total_supporters']))
    return results

# ── Analysis 4: Contradiction Clusters ─────────────────────────────────

def contradiction_clusters(graph):
    """For contradiction pairs, build camps around each side."""
    # Find all contradiction edges
    contradictions = []
    for slug, data in graph.items():
        for target, etypes in data['out_edges'].items():
            if 'contradicts' in etypes:
                contradictions.append((slug, target))

    clusters = []
    for claim_a, claim_b in contradictions:
        def gather_camp(slug, depth=2):
            camp = set()
            queue = deque([(slug, 0)])
            seen = {slug}
            while queue:
                current, d = queue.popleft()
                if d >= depth:
                    continue
                g = graph.get(current)
                if not g:
                    continue
                # Incoming: who supports this position
                for source, etypes in g['in_edges'].items():
                    if source not in seen and etypes & {'supports', 'extends', 'depends_on'}:
                        camp.add(source)
                        seen.add(source)
                        queue.append((source, d + 1))
                # Outgoing: what this position supports
                for target, etypes in g['out_edges'].items():
                    if target not in seen and etypes & {'supports', 'extends', 'depends_on'}:
                        camp.add(target)
                        seen.add(target)
                        queue.append((target, d + 1))
            return camp

        camp_a = gather_camp(claim_a)
        camp_b = gather_camp(claim_b)
        shared = camp_a & camp_b

        # Source notes in each camp
        def camp_sources(camp):
            sources = set()
            for s in camp:
                m = graph.get(s, {}).get('meta', {})
                sn = m.get('source_note', '').replace('[[', '').replace(']]', '')
                if sn:
                    sources.add(sn)
            return sources

        src_a = camp_sources(camp_a)
        src_b = camp_sources(camp_b)

        # Assessment
        if len(camp_a) >= 3 and len(camp_b) >= 3:
            if shared:
                tension = "genuine domain tension with shared sources -- same evidence, different readings"
            else:
                tension = "genuine domain tension -- separate camps"
        elif len(camp_a) <= 1 and len(camp_b) <= 1:
            tension = "structurally isolated -- likely an edge-case disagreement"
        elif len(camp_a) >= 3 * max(1, len(camp_b)) or len(camp_b) >= 3 * max(1, len(camp_a)):
            tension = "asymmetric -- one position is the outlier"
        else:
            tension = "moderate tension"

        meta_a = graph.get(claim_a, {}).get('meta', {})
        meta_b = graph.get(claim_b, {}).get('meta', {})

        clusters.append({
            'claim_a': claim_a,
            'claim_b': claim_b,
            'statement_a': (meta_a.get('statement', '')[:120] + '...') if len(meta_a.get('statement', '')) > 120 else meta_a.get('statement', ''),
            'statement_b': (meta_b.get('statement', '')[:120] + '...') if len(meta_b.get('statement', '')) > 120 else meta_b.get('statement', ''),
            'camp_a_size': len(camp_a),
            'camp_b_size': len(camp_b),
            'shared_sources': len(shared),
            'shared_names': sorted(shared),
            'sources_a': sorted(src_a),
            'sources_b': sorted(src_b),
            'assessment': tension,
        })

    return clusters

# ── Analysis 5: Structural Gaps ────────────────────────────────────────

def structural_gaps(graph):
    """Orphans, articulation points, connected components, topic sparsity."""

    # 5a: Orphans -- claims with zero edges
    orphans = []
    for slug, data in graph.items():
        if len(data['out_edges']) == 0 and len(data['in_edges']) == 0:
            meta = data['meta']
            orphans.append({
                'slug': slug,
                'claim_id': meta['claim_id'],
                'statement': meta['statement'][:120] if len(meta['statement']) > 120 else meta['statement'],
                'source_note': meta['source_note'],
                'topics': [t for t in meta.get('tags', []) if t.startswith('topic/')],
            })

    # 5b: Connected components (undirected)
    visited = set()
    components = []
    node_list = list(graph.keys())

    # Build undirected adjacency set
    undirected = {slug: set() for slug in graph}
    for slug, data in graph.items():
        for t in data['out_edges']:
            undirected[slug].add(t)
            if t in undirected:
                undirected[t].add(slug)
        for s in data['in_edges']:
            undirected[slug].add(s)
            if s in undirected:
                undirected[s].add(slug)

    for node in node_list:
        if node in visited:
            continue
        # BFS
        comp = []
        queue = deque([node])
        visited.add(node)
        while queue:
            cur = queue.popleft()
            comp.append(cur)
            for nb in undirected.get(cur, set()):
                if nb not in visited:
                    visited.add(nb)
                    queue.append(nb)
        components.append(comp)

    # Flag small isolated clusters (2-5 claims) and the giant component
    small_clusters = []
    giant = []
    for comp in components:
        if 2 <= len(comp) <= 5:
            small_clusters.append(comp)
        elif len(comp) > 100:
            giant = comp

    # 5c: Articulation points (bridges)
    # Use DFS-based articulation point detection on undirected projection
    def find_articulation_points(nodes, adj):
        """Tarjan's algorithm for articulation points."""
        n = len(nodes)
        idx = {node: i for i, node in enumerate(nodes)}
        visited = [False] * n
        disc = [0] * n
        low = [0] * n
        parent = [-1] * n
        ap = [False] * n
        time = 0

        def dfs(u):
            nonlocal time
            children = 0
            visited[u] = True
            disc[u] = low[u] = time
            time += 1

            for v_node in adj.get(nodes[u], set()):
                v = idx.get(v_node)
                if v is None:
                    continue
                if not visited[v]:
                    children += 1
                    parent[v] = u
                    dfs(v)
                    low[u] = min(low[u], low[v])
                    if parent[u] == -1 and children > 1:
                        ap[u] = True
                    if parent[u] != -1 and low[v] >= disc[u]:
                        ap[u] = True
                elif v != parent[u]:
                    low[u] = min(low[u], disc[v])

        for i in range(n):
            if not visited[i]:
                dfs(i)
        return [nodes[i] for i in range(n) if ap[i]]

    # Run articulation point detection on the largest component
    articulation_points = []
    if giant:
        articulation_points = find_articulation_points(giant, undirected)

    # Score articulation points by degree
    ap_scored = []
    for ap in articulation_points:
        deg = len(undirected.get(ap, set()))
        meta = graph.get(ap, {}).get('meta', {})
        ap_scored.append({
            'slug': ap,
            'claim_id': meta.get('claim_id', ''),
            'statement': (meta.get('statement', '')[:100] + '...') if len(meta.get('statement', '')) > 100 else meta.get('statement', ''),
            'degree': deg,
        })
    ap_scored.sort(key=lambda x: x['degree'], reverse=True)

    # 5d: Topic sparsity
    topic_claims = defaultdict(list)
    for slug, data in graph.items():
        for tag in data['meta'].get('tags', []):
            if tag.startswith('topic/'):
                topic_claims[tag].append(slug)

    topic_sparsity = []
    for topic, slugs in topic_claims.items():
        if len(slugs) < 3:
            continue
        total_edges = sum(
            len(graph.get(s, {}).get('out_edges', {})) + len(graph.get(s, {}).get('in_edges', {}))
            for s in slugs
        )
        avg = total_edges / len(slugs)
        if avg < 2.0:
            topic_sparsity.append({
                'topic': topic,
                'claims': len(slugs),
                'avg_edges': round(avg, 2),
            })

    topic_sparsity.sort(key=lambda x: x['avg_edges'])

    return {
        'orphans': orphans,
        'orphan_count': len(orphans),
        'components': {
            'total': len(components),
            'giant_size': len(giant) if giant else 0,
            'small_clusters': [{'size': len(c), 'members': c} for c in small_clusters],
        },
        'articulation_points': ap_scored[:10],
        'topic_sparsity': topic_sparsity[:15],
    }

# ── Main ───────────────────────────────────────────────────────────────

def main():
    print("Loading claims...")
    claims = load_claim_metadata()
    print(f"  Loaded {len(claims)} active claims")

    print("Loading canonical edges...")
    edges = load_canonical_edges()
    print(f"  Loaded {len(edges)} edges")

    print("Building graph...")
    graph = build_graph(claims, edges)

    claimed_edges = sum(1 for s in graph if graph[s]['out_edges'] or graph[s]['in_edges'])
    print(f"  {claimed_edges} claims with edges, {len(graph) - claimed_edges} orphans")

    # ── Run analyses ──
    print("\n=== Analysis 1: Hinge Inventory ===")
    hinges = hinge_inventory(graph)
    for i, h in enumerate(hinges[:10], 1):
        print(f"  {i:2}. {h['claim_id']} (score={h['score']:.4f}, deg={h['degree']}, bc={h['betweenness']:.6f})")

    print("\n=== Analysis 2: Cascade Trees ===")
    cascades = cascade_trees(graph, hinges, depth=3, top_n=15)

    print("\n=== Analysis 3: Convergence Points ===")
    conv = convergence_points(graph)
    print(f"  Found {len(conv)} convergence points (3+ unique sources)")
    for c in conv[:10]:
        print(f"  {c['claim_id']}: {c['unique_sources']} sources, {c['total_supporters']} supporters")

    print("\n=== Analysis 4: Contradiction Clusters ===")
    contras = contradiction_clusters(graph)
    print(f"  Found {len(contras)} contradiction clusters")

    print("\n=== Analysis 5: Structural Gaps ===")
    gaps = structural_gaps(graph)
    print(f"  Orphans: {gaps['orphan_count']}")
    print(f"  Components: {gaps['components']['total']} (giant: {gaps['components']['giant_size']})")
    print(f"  Small clusters: {len(gaps['components']['small_clusters'])}")
    print(f"  Articulation points: {len(gaps['articulation_points'])}")
    print(f"  Sparse topics: {len(gaps['topic_sparsity'])}")

    # ── Build output ──
    results = {
        'project': 'OSKG-IBD',
        'phase': 4,
        'summary': {
            'total_claims': len(claims),
            'total_edges': len(edges),
            'claims_with_edges': claimed_edges,
            'orphans': gaps['orphan_count'],
            'components': gaps['components']['total'],
            'giant_component_size': gaps['components']['giant_size'],
        },
        'hinges': hinges,
        'convergence_points': conv,
        'contradiction_clusters': contras,
        'structural_gaps': gaps,
    }

    # Write JSON
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nWrote {OUTPUT_JSON}")

    # Write text report
    lines = []
    lines.append("=" * 72)
    lines.append("  OSKG-IBD Phase 4: Structural Analysis Report")
    lines.append("=" * 72)
    lines.append(f"  Claims: {len(claims)} | Edges: {len(edges)} | Connected: {claimed_edges} | Orphans: {gaps['orphan_count']}")
    lines.append("=" * 72 + "\n")

    # 1. Hinges
    lines.append("─" * 72)
    lines.append("1. HINGE INVENTORY (Top 15)")
    lines.append("─" * 72)
    for i, h in enumerate(hinges, 1):
        lines.append(f"\n{i:2}. [{h['claim_id']}]  score={h['score']:.4f}  deg={h['degree']}  bc={h['betweenness']:.6f}")
        lines.append(f"    {h['statement']}")
        lines.append(f"    Confidence: {h['confidence']} | Source: {h['source_note']}")
        lines.append(f"    Topics: {', '.join(h['topics'][:5])} | Dependents: {h['direct_dependents']}")

    # 2. Cascade Trees
    lines.append("\n\n" + "─" * 72)
    lines.append("2. CASCADE TREES (Top 15 Hinges)")
    lines.append("─" * 72)
    lines.append(cascades)

    # 3. Convergence Points
    lines.append("\n" + "─" * 72)
    lines.append("3. CONVERGENCE POINTS (3+ unique source notes)")
    lines.append("─" * 72)
    if conv:
        for i, c in enumerate(conv[:20], 1):
            lines.append(f"\n{i:2}. [{c['claim_id']}]")
            lines.append(f"    {c['statement']}")
            lines.append(f"    Unique sources: {c['unique_sources']} | Total supporters: {c['total_supporters']} | Contradictions: {c['contradiction_count']}")
            lines.append(f"    Sources: {', '.join(c['source_list'][:10])}")
    else:
        lines.append("\n  No convergence points found (threshold: 3+ unique sources).")

    # 4. Contradiction Clusters
    lines.append("\n\n" + "─" * 72)
    lines.append("4. CONTRADICTION CLUSTERS")
    lines.append("─" * 72)
    if contras:
        for i, cc in enumerate(contras, 1):
            lines.append(f"\n{i}. {cc['claim_a']} vs {cc['claim_b']}")
            lines.append(f"   A: {cc['statement_a']}")
            lines.append(f"   B: {cc['statement_b']}")
            lines.append(f"   Camp A: {cc['camp_a_size']} claims | Camp B: {cc['camp_b_size']} claims | Shared: {cc['shared_sources']}")
            lines.append(f"   Sources A: {', '.join(cc['sources_a'][:5])}")
            lines.append(f"   Sources B: {', '.join(cc['sources_b'][:5])}")
            lines.append(f"   Assessment: {cc['assessment']}")
    else:
        lines.append("\n  No contradiction edges found.")

    # 5. Structural Gaps
    lines.append("\n\n" + "─" * 72)
    lines.append("5. STRUCTURAL GAPS")
    lines.append("─" * 72)

    lines.append(f"\n5a. ORPHANS: {gaps['orphan_count']} claims with zero edges")
    for i, o in enumerate(gaps['orphans'][:30], 1):
        lines.append(f"  {i:2}. [{o['claim_id']}] {o['statement'][:80]}")
        lines.append(f"      Source: {o['source_note']} | Topics: {', '.join(o['topics'][:3])}")

    lines.append(f"\n5b. CONNECTED COMPONENTS: {gaps['components']['total']} total")
    lines.append(f"    Giant component: {gaps['components']['giant_size']} claims")
    lines.append(f"    Small isolated clusters (2-5 claims): {len(gaps['components']['small_clusters'])}")
    for sc in gaps['components']['small_clusters']:
        lines.append(f"      Size {sc['size']}: {', '.join(sc['members'][:5])}")

    lines.append(f"\n5c. ARTICULATION POINTS: {len(gaps['articulation_points'])} bridges in giant component")
    for ap in gaps['articulation_points']:
        lines.append(f"    [{ap['claim_id']}] deg={ap['degree']}: {ap['statement']}")

    lines.append(f"\n5d. TOPIC SPARSITY: {len(gaps['topic_sparsity'])} under-connected topics")
    for ts in gaps['topic_sparsity']:
        lines.append(f"    {ts['topic']}: {ts['claims']} claims, avg {ts['avg_edges']} edges/claim")

    report = '\n'.join(lines)
    with open(OUTPUT_TXT, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Wrote {OUTPUT_TXT}")

if __name__ == '__main__':
    main()
