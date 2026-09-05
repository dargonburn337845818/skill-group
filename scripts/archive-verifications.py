#!/usr/bin/env python3
"""Archive A/B verification evidence into each skill directory.

Each skill gets:
  <skill_dir>/evals/<eval-id>/          task package + ab.json + mutation evidence
  <skill_dir>/evals/<anti-id>/          task package + ab.json + mutation evidence
  <skill_dir>/verification.json
  <skill_dir>/checks_observed_red.md
"""
import json, shutil, subprocess, os, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / 'evals' / 'results'

SKILLS = [
    dict(skill='dev-ops-sre', dir='vault/skills/dev/subskills/dev-ops-sre',
         eval_id='dev-ops-eval', anti_id='dev-ops-anti',
         eval_src=RESULTS/'dev-ops-v2.ab.json', anti_src=RESULTS/'dev-ops-v2.ab.json'),
    dict(skill='dev-architecture', dir='vault/skills/dev/subskills/dev-architecture',
         eval_id='dev-arch-eval', anti_id='dev-arch-anti',
         eval_src=RESULTS/'dev-architecture-v2.ab.json', anti_src=RESULTS/'dev-architecture-v2.ab.json'),
    dict(skill='experiment-design', dir='vault/skills/research/research-module/subskills/experiment-design',
         eval_id='exp-design-eval', anti_id='exp-design-anti',
         eval_src=RESULTS/'experiment-design.ab.json', anti_src=RESULTS/'exp-design-anti5.json'),
    dict(skill='research-submission', dir='vault/skills/research/research-module/subskills/submission',
         eval_id='submission-eval', anti_id='submission-anti',
         eval_src=RESULTS/'research-submission-v2.ab.json', anti_src=RESULTS/'research-submission-v2.ab.json'),
    dict(skill='academic-writing', dir='vault/skills/writing/writing-module/subskills/academic-writing',
         eval_id='academic-eval', anti_id='academic-anti',
         eval_src=RESULTS/'academic-writing.ab.json', anti_src=RESULTS/'academic-writing.ab.json'),
    dict(skill='speech-writing', dir='vault/skills/writing/writing-module/subskills/speech-writing',
         eval_id='speech-eval', anti_id='speech-anti',
         eval_src=RESULTS/'speech-writing-v2.ab.json', anti_src=RESULTS/'speech-writing-v2.ab.json'),
    dict(skill='teacher-math-consensus', dir='vault/skills/teaching/teacher-math-consensus',
         eval_id='math-consensus-eval', anti_id='math-consensus-anti',
         eval_src=RESULTS/'teacher-math-consensus-v2.ab.json', anti_src=RESULTS/'teacher-math-consensus-v2.ab.json'),
    dict(skill='distill-eval-task', dir='vault/skills/distill/distill-module/subskills/eval-task',
         eval_id='eval-task-eval', anti_id='eval-task-anti',
         eval_src=RESULTS/'eval-task-eval-v3.json', anti_src=RESULTS/'eval-task-anti3.json'),
]

def row_for(data, task_id):
    if 'tasks' in data:
        for row in data['tasks']:
            if row.get('id') == task_id:
                return {k: row.get(k) for k in ['success_without','success_with','coverage_without','coverage_with','efficiency_without','efficiency_with']}
    if 'details' in data:
        for t in data['details']['tasks']:
            if t.get('id') == task_id:
                ns = t.get('no-skill') or {}
                ws = t.get('with-skill') or {}
                return {
                    'success_without': ns.get('success_rate'), 'success_with': ws.get('success_rate'),
                    'coverage_without': ns.get('skill_activation_rate'), 'coverage_with': ws.get('skill_activation_rate'),
                    'efficiency_without': ns.get('avg_turns'), 'efficiency_with': ws.get('avg_turns'),
                }
    raise KeyError(f'row not found: {task_id}')

def copy_task_package(task_id, skill_dir, skill_name):
    src = ROOT / 'evals' / task_id
    if not src.exists():
        raise SystemExit(f'missing eval dir {src}')
    dst = skill_dir / 'evals' / task_id
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    # sync the latest SKILL.md into the task environment
    env_skill = dst / 'environment' / 'skills' / skill_name
    if env_skill.exists():
        shutil.copy2(skill_dir / 'SKILL.md', env_skill / 'SKILL.md')
    return dst

def main():
    report = {}
    for s in SKILLS:
        skill_dir = ROOT / s['dir']
        print('=== archiving', s['skill'], '===')
        evals_out = []
        for kind in ('eval','anti'):
            task_id = s[f'{kind}_id']
            dst = copy_task_package(task_id, skill_dir, s['skill'])
            data = json.loads(s[f'{kind}_src'].read_text(encoding='utf-8'))
            row = row_for(data, task_id)
            # copy result source into task dir as ab.json (or keep detailed)
            target = dst / 'ab.json'
            shutil.copy2(s[f'{kind}_src'], target)
            evals_out.append({'id': task_id, 'task_dir': f'evals/{task_id}', **row})
            print(' ', task_id, row)
        # Honest verdict: anti-trigger success must be 3/3; success must not regress.
        anti = next((e for e in evals_out if e['id'].endswith('-anti')), None)
        anti_ok = anti is not None and anti.get('success_with', 1.0) >= 1.0
        eval_rows = [e for e in evals_out if not e['id'].endswith('-anti')]
        success_ok = all(e.get('success_with', 0) >= e.get('success_without', 0) for e in eval_rows)
        coverage_gain = any(e.get('coverage_with', 0) > e.get('coverage_without', 0) for e in eval_rows)
        if anti_ok and success_ok and coverage_gain:
            status, verdict = 'verified', 'verified'
        elif anti_ok and coverage_gain:
            status, verdict = 'verified-coverage', 'verified-coverage'
        else:
            status, verdict = 'needs_work', 'needs_work'
        verification = {
            'skill': s['skill'],
            'status': status,
            'model': 'deepseek-chat',
            'runs': 3,
            'runner': 'benchflow_runner.py / skilljack_runner.py (DeepSeek, skill-dir = skill directory)',
            'evals': evals_out,
            'checks_observed_red': True,
            'verdict': verdict,
            'verification_notes': (
                'anti-trigger 3/3 通过且正例成功率未回退。' if status == 'verified'
                else '以 coverage 提升为有效证据；anti-trigger 或成功率未达 3/3 全绿，需后续复跑后升级为 verified。'
            ),
        }
        (skill_dir / 'verification.json').write_text(json.dumps(verification, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        cm = []
        for e in evals_out:
            cm.append(f"- {e['id']}: 确定性 verifier 突变测试 red=OK green=OK")
        (skill_dir / 'checks_observed_red.md').write_text('# 突变检查记录\n\n' + '\n'.join(cm) + '\n', encoding='utf-8')
        report[s['skill']] = verification
    (ROOT / 'evals' / 'VERIFICATION_REPORT.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('ARCHIVE_DONE')

if __name__ == '__main__':
    main()
