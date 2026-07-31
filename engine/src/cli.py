"""
CLI 入口：bom-scene match <bom_file> [--output-dir ./output/] [--format md|json]
"""

from __future__ import annotations

import sys
from pathlib import Path

import click

from src.bom_parser import parse_bom
from src.matcher import Matcher, SceneLoader
from src.renderer import render_markdown, render_json

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@click.group()
def cli():
    """BOM-Scene Engine: BOM → 场景智能匹配工具。"""
    pass


@cli.command()
@click.argument("bom_file", type=click.Path(exists=True, dir_okay=False))
@click.option("--scene-dir", default=None, help="场景库目录（默认使用内置场景库）")
@click.option("--output-dir", default=None, help="输出目录")
@click.option("--format", "fmt", default="markdown", type=click.Choice(["markdown", "json"]),
              help="输出格式")
@click.option("--no-reasoning", is_flag=True, default=False, help="不输出评分推理过程")
def match(bom_file: str, scene_dir: str | None, output_dir: str | None,
          fmt: str, no_reasoning: bool):
    """匹配 BOM 与场景库，输出匹配报告。"""

    # 加载 BOM
    try:
        product = parse_bom(bom_file)
    except Exception as e:
        click.echo(f"❌ BOM 解析失败: {e}", err=True)
        sys.exit(1)

    click.echo(f"✅ BOM 解析成功: {product.name}")

    # 加载场景
    if scene_dir:
        loader = SceneLoader(scene_dir)
    else:
        loader = SceneLoader(DEFAULT_DATA_DIR / "scene_library")

    scenes = loader.load_all()
    click.echo(f"📂 加载场景: {len(scenes)} 个")

    # 匹配
    matcher = Matcher(loader)
    report = matcher.match(product)

    click.echo(f"🎯 最佳匹配: {report.top_scene.scene_name} "
               f"({report.top_scene.total_score:.1%})" if report.top_scene else "无匹配")

    # 输出
    output_path = None
    if output_dir:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        ext = ".md" if fmt == "markdown" else ".json"
        output_path = out_dir / f"bom_match_report{ext}"

    if fmt == "markdown":
        md = render_markdown(
            report,
            include_raw_scores=True,
            include_reasoning=not no_reasoning,
            output_path=output_path,
        )
        if not output_path:
            click.echo("\n" + md)
        else:
            click.echo(f"📄 已写入: {output_path}")
    else:
        j = render_json(report, output_path=output_path)
        if not output_path:
            click.echo(j)
        else:
            click.echo(f"📄 已写入: {output_path}")


@cli.command()
def list_scenes():
    """列出当前场景库中的所有场景。"""
    loader = SceneLoader(DEFAULT_DATA_DIR / "scene_library")
    scenes = loader.load_all()

    click.echo(f"场景库 ({len(scenes)} 个):")
    click.echo("")
    for s in scenes:
        sid = s.scene.get("id", "?")
        name = s.scene.get("name", "?")
        pri = s.scene.get("priority", "?")
        desc = s.scene.get("description", "")
        n_constraints = len(s.hard_constraints.items)
        n_dims = len(s.soft_scoring.dimensions)
        click.echo(f"  [{pri}] {name} ({sid})")
        click.echo(f"        {desc}")
        click.echo(f"        硬约束: {n_constraints} | 评分维度: {n_dims}")
        click.echo("")


if __name__ == "__main__":
    cli()
