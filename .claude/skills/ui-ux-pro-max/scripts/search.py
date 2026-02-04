#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI/UX Pro Max Search - BM25 search engine for UI/UX style guides
Usage: python search.py "<query>" [--domain <domain>] [--stack <stack>] [--max-results 3]
       python search.py "<query>" --design-system [-p "Project Name"]
       python search.py "<query>" --design-system --persist [-p "Project Name"] [--page "dashboard"]
       python search.py "<query>" --presentation --title "Title" [--type business] [--audience executives] [--output out.html] [--format reveal_js]

Domains: style, prompt, color, chart, landing, product, ux, typography, slide_layout, animation, presentation_pattern, ...
Stacks: html-tailwind, react, nextjs

Persistence (Master + Overrides pattern):
  --persist    Save design system to design-system/MASTER.md
  --page       Also create a page-specific override file in design-system/pages/
"""

import argparse
import json
import sys
from pathlib import Path

from core import CSV_CONFIG, AVAILABLE_STACKS, MAX_RESULTS, search, search_stack
from design_system import generate_design_system, persist_design_system


def format_output(result):
    """Format results for Claude consumption (token-optimized)"""
    if "error" in result:
        return f"Error: {result['error']}"

    output = []
    if result.get("stack"):
        output.append(f"## UI Pro Max Stack Guidelines")
        output.append(f"**Stack:** {result['stack']} | **Query:** {result['query']}")
    else:
        output.append(f"## UI Pro Max Search Results")
        output.append(f"**Domain:** {result['domain']} | **Query:** {result['query']}")
    output.append(f"**Source:** {result['file']} | **Found:** {result['count']} results\n")

    for i, row in enumerate(result['results'], 1):
        output.append(f"### Result {i}")
        for key, value in row.items():
            value_str = str(value)
            if len(value_str) > 300:
                value_str = value_str[:300] + "..."
            output.append(f"- **{key}:** {value_str}")
        output.append("")

    return "\n".join(output)


def run_presentation(args):
    """运行演示文稿生成并可选导出到文件"""
    script_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(script_dir))

    from presentation_generator import PresentationGenerator
    from presentation_reasoning import PresentationType, AudienceType, Tone

    try:
        out_fmt = getattr(args, "presentation_format", "json")
    except AttributeError:
        out_fmt = "json"

    gen = PresentationGenerator(data_dir=script_dir.parent / "data")

    from presentation_generator import OutputFormat
    # 导出 reveal_js/pptx 时先生成标准 JSON 结构，再由导出器写文件
    if out_fmt in ("reveal_js", "pptx"):
        of = OutputFormat.JSON
    else:
        of = getattr(OutputFormat, out_fmt.upper(), OutputFormat.JSON)

    result = gen.generate(
        title=args.presentation_title or args.query,
        presentation_type=getattr(args, "presentation_type", "business_presentation") or "business_presentation",
        audience=getattr(args, "presentation_audience", "general_employees") or "general_employees",
        duration_minutes=int(getattr(args, "presentation_duration", 15) or 15),
        tone=getattr(args, "presentation_tone", "professional") or "professional",
        industry=getattr(args, "presentation_industry", "") or "",
        key_points=[],
        objectives=[],
        output_format=of,
        options={
            "include_animations": getattr(args, "with_animations", True),
            "author": getattr(args, "author", None),
            "company": getattr(args, "company", None),
        },
    )

    if getattr(args, "output", None):
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if out_fmt == "reveal_js":
            from revealjs_exporter import RevealJSExporter
            exporter = RevealJSExporter(theme=getattr(args, "reveal_theme", "black"))
            exporter.save(result["slides"], result["metadata"], out_path)
            print(f"Reveal.js 已保存: {out_path}")
        elif out_fmt == "pptx":
            from pptx_exporter import PPTXExporter
            exporter = PPTXExporter()
            exporter.save(result["slides"], result["metadata"], out_path)
            print(f"PPTX 已保存: {out_path}")
        elif out_fmt in ("json", "dict"):
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"JSON 已保存: {out_path}")
        elif out_fmt == "markdown":
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(result if isinstance(result, str) else result.get("markdown", str(result)))
            print(f"Markdown 已保存: {out_path}")
    else:
        if out_fmt == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UI Pro Max Search")
    parser.add_argument("query", nargs="?", default="", help="Search query or presentation topic")
    parser.add_argument("--domain", "-d", choices=list(CSV_CONFIG.keys()), help="Search domain")
    parser.add_argument("--stack", "-s", choices=AVAILABLE_STACKS, help="Stack-specific search (html-tailwind, react, nextjs)")
    parser.add_argument("--max-results", "-n", type=int, default=MAX_RESULTS, help="Max results (default: 3)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    # Design system generation
    parser.add_argument("--design-system", "-ds", action="store_true", help="Generate complete design system recommendation")
    parser.add_argument("--project-name", "-p", type=str, default=None, help="Project name for design system output")
    parser.add_argument("--format", "-f", choices=["ascii", "markdown"], default="ascii", help="Output format for design system")
    # Persistence (Master + Overrides pattern)
    parser.add_argument("--persist", action="store_true", help="Save design system to design-system/MASTER.md (creates hierarchical structure)")
    parser.add_argument("--page", type=str, default=None, help="Create page-specific override file in design-system/pages/")
    parser.add_argument("--output-dir", "-o", type=str, default=None, help="Output directory for persisted files (default: current directory)")

    # 演示文稿生成
    parser.add_argument("--presentation", action="store_true", help="Generate presentation from query/title")
    parser.add_argument("--title", type=str, default=None, dest="presentation_title", help="Presentation title (default: query)")
    parser.add_argument("--type", type=str, default="business_presentation", dest="presentation_type",
                        choices=["business_presentation", "investor_pitch", "product_launch", "training_workshop", "webinar", "keynote", "sales_pitch"],
                        help="Presentation type")
    parser.add_argument("--audience", type=str, default="general_employees", dest="presentation_audience",
                        choices=["general_employees", "senior_executives", "investors", "clients", "technical_team", "students"],
                        help="Target audience")
    parser.add_argument("--duration", type=int, default=15, dest="presentation_duration", help="Duration in minutes")
    parser.add_argument("--tone", type=str, default="professional", dest="presentation_tone",
                        choices=["professional", "casual", "persuasive", "inspirational", "educational"],
                        help="Tone of the presentation")
    parser.add_argument("--industry", type=str, default="", dest="presentation_industry", help="Industry (optional)")
    parser.add_argument("--output", type=str, default=None, help="Output file path (for presentation export)")
    parser.add_argument("--presentation-format", type=str, default="json", dest="presentation_format",
                        choices=["json", "reveal_js", "pptx", "markdown"],
                        help="Presentation output format when using --presentation")
    parser.add_argument("--with-animations", action="store_true", default=True, dest="with_animations", help="Include animations (default: True)")
    parser.add_argument("--no-animations", action="store_false", dest="with_animations", help="Disable animations")
    parser.add_argument("--author", type=str, default=None, help="Author name for presentation metadata")
    parser.add_argument("--company", type=str, default=None, help="Company name for presentation metadata")
    parser.add_argument("--reveal-theme", type=str, default="black", help="Reveal.js theme when --presentation-format reveal_js")

    args = parser.parse_args()

    # 演示文稿生成优先于 design-system
    if args.presentation:
        if not args.query and not args.presentation_title:
            parser.error("--presentation 需要提供 query 或 --title")
        run_presentation(args)
        sys.exit(0)

    # Design system takes priority over domain search
    if args.design_system:
        result = generate_design_system(
            args.query, 
            args.project_name, 
            args.format,
            persist=args.persist,
            page=args.page,
            output_dir=args.output_dir
        )
        print(result)
        
        # Print persistence confirmation
        if args.persist:
            project_slug = args.project_name.lower().replace(' ', '-') if args.project_name else "default"
            print("\n" + "=" * 60)
            print(f"✅ Design system persisted to design-system/{project_slug}/")
            print(f"   📄 design-system/{project_slug}/MASTER.md (Global Source of Truth)")
            if args.page:
                page_filename = args.page.lower().replace(' ', '-')
                print(f"   📄 design-system/{project_slug}/pages/{page_filename}.md (Page Overrides)")
            print("")
            print(f"📖 Usage: When building a page, check design-system/{project_slug}/pages/[page].md first.")
            print(f"   If exists, its rules override MASTER.md. Otherwise, use MASTER.md.")
            print("=" * 60)
    # Stack search
    elif args.stack:
        result = search_stack(args.query, args.stack, args.max_results)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_output(result))
    # Domain search
    else:
        if not args.query:
            parser.error("请提供 query，或使用 --presentation / --design-system")
        result = search(args.query, args.domain, args.max_results)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_output(result))
