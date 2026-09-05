/**
 * @dsh-external/dsh-skill-vault — 设置页。
 *
 * 展示正式模块（开发/蒸馏/教师/AI 学习/科研/文稿）；
 * 底座与 alpha 旧场景不在这里出现。数据目前是静态占位。
 */
import { createElement, useEffect, useRef } from 'react'

interface SlotRegistration {
  name: string
  id: string
  label: () => string
  order?: number
}

interface SlotsService {
  inject(slot: string, factory: () => unknown): unknown
  register(reg: SlotRegistration, component: (props?: any) => any): unknown
}

interface EffectContext {
  effect(fn: () => unknown, label?: string): unknown
}

type ClientContext = EffectContext & {
  slots: SlotsService
}

export const inject = ['slots']

interface FormalSkill {
  id: string
  title: string
  status: 'filled' | 'todo'
}

interface FormalModule {
  id: string
  title: string
  description: string
  skills: FormalSkill[]
  experts: string[]
}

const FORMAL_MODULES: FormalModule[] = [
    {
      id: 'dev',
      title: '开发',
      description: '前后端、美术/PPT、编码规范、安全、并发/性能、测试调试、设计美学、去 AI 味',
      skills: [
        { id: 'dev-module', title: '开发模块壳', status: 'filled' },
        { id: 'github-repo-consensus', title: 'GitHub 开源仓库共识', status: 'filled' },
        { id: 'ui-aesthetics-design', title: 'UI 美学设计', status: 'filled' },
        { id: 'dev-frontend', title: '前端开发', status: 'filled' },
        { id: 'dev-backend', title: '后端开发', status: 'filled' },
        { id: 'dev-art-ppt', title: '美术与 PPT', status: 'filled' },
        { id: 'dev-security', title: '信息安全', status: 'filled' },
        { id: 'dev-concurrency', title: '并发调优', status: 'filled' },
        { id: 'dev-performance', title: '性能优化', status: 'filled' },
        { id: 'dev-testing', title: '测试调试机制', status: 'filled' },
        { id: 'dev-design-aesthetics', title: '设计美学/风格库', status: 'filled' },
        { id: 'dev-remove-ai-flavor', title: '去 AI 味技巧', status: 'filled' },
      ],
      experts: [
        'Evan You', 'Rich Harris', 'Dan Abramov', 'Martin Fowler', 'Bruce Schneier',
        'Brendan Gregg', 'John Carmack', 'Andrej Karpathy', 'Lilian Weng', 'Chip Huyen',
        'Charity Majors', 'Kelsey Hightower', 'Cindy Sridharan', 'Hadley Wickham',
        'Andrew Gelman', 'Don Norman', 'Jakob Nielsen', 'Julie Zhuo'
      ],
    },
    {
      id: 'distill',
      title: '蒸馏',
      description: '继承核心迭代：元能力迭代 + 为各模块补充/调优内容',
      skills: [
        { id: 'core-iteration', title: '核心迭代元能力', status: 'filled' },
        { id: 'distillation-consensus', title: '内容蒸馏共识', status: 'filled' },
        { id: 'web-research-consensus', title: '网络信息搜集共识', status: 'filled' },
        { id: 'distill-module', title: '蒸馏模块编排层', status: 'filled' },
        { id: 'skill-effect-bench', title: '真实 Skill A/B 评测（已接入）', status: 'filled' },
      ],
      experts: [
        'core-iteration（元能力）', 'distillation-consensus', 'skill-verification-consensus',
        'tourist', 'Um_nik', 'Evan You', 'Martin Fowler', 'Andrej Karpathy',
        'William Zinsser', 'Ting Yang', 'Ping Wang'
      ],
    },
    {
      id: 'teacher',
      title: '教师',
      description: '多领域专家视角：答疑、纠偏、规划方向、多 agent 讨论团队',
      skills: [
        { id: 'teacher-consensus', title: '算法竞赛教师共识', status: 'filled' },
        { id: 'teacher-module', title: '人名专家团 + 回合式讨论', status: 'filled' },
        { id: 'expert-team', title: '专家团标准流程（跨模块）', status: 'filled' },
      ],
      experts: [
        'tourist', 'jiangly', 'benq', 'Um_nik', 'Errichto', 'ecnerwala',
        'Radewoosh', 'neal', 'rng_58', 'Petr', 'Terence Tao'
      ],
    },
    {
      id: 'learning',
      title: 'AI 学习',
      description: '用 AI 十倍速学习：项目驱动、反馈闭环、第二潜意识、AI 只去摩擦',
      skills: [
        { id: 'ai-10x-learning', title: 'AI 十倍速学习', status: 'filled' },
        { id: 'teacher-module', title: '人名专家团 + 回合式讨论', status: 'filled' },
        { id: 'expert-team', title: '专家团标准流程（跨模块）', status: 'filled' },
      ],
      experts: [
        'Dan Koe', 'Richard Feynman', 'Andrej Karpathy'
      ],
    },
    {
      id: 'research',
      title: '科研',
      description: '多 agent 科研团队：读论文、理脉络、写论文、组会、PPT、模拟导师审查',
      skills: [
        { id: 'vlpc-consensus', title: 'VLPC 领域共识', status: 'filled' },
        { id: 'research-module', title: '科研模块', status: 'filled' },
        { id: 'paper-reading', title: '论文阅读', status: 'filled' },
        { id: 'paper-outline', title: '文献脉络', status: 'filled' },
        { id: 'paper-writing', title: '论文写作', status: 'filled' },
        { id: 'group-meeting', title: '组会研讨', status: 'filled' },
        { id: 'research-ppt', title: '科研 PPT', status: 'filled' },
        { id: 'mentor-review', title: '导师审查', status: 'filled' },
        { id: 'career-path', title: '职业路径', status: 'filled' },
      ],
      experts: [
        'Ting Yang', 'Ping Wang', 'S. Ma', 'Y. Chen', 'O. K. H. Shanker',
        'A. K. Sah', 'Richard Feynman'
      ],
    },
    {
      id: 'writing',
      title: '文稿',
      description: '提示词、文案、各类文本生产；可被其他四模块复用',
      skills: [
        { id: 'writing-module', title: '文稿模块', status: 'filled' },
        { id: 'prompt-writing', title: '提示词模板', status: 'filled' },
        { id: 'copywriting', title: '文案写作', status: 'filled' },
        { id: 'document-report', title: '文档/报告生成', status: 'filled' },
      ],
      experts: [
        'William Zinsser', 'Don Norman', 'Jakob Nielsen', 'Julie Zhuo',
        'Ting Yang', 'Ping Wang'
      ],
    },
  ]

const PANEL_CLASS = 'dsh-skill-vault-panel'

/* 视觉统一：颜色/字体/边框走 DSH host 变量，明暗主题自动适配。 */
const UI_CSS = `
.${PANEL_CLASS} {
  box-sizing: border-box;
  max-width: 920px;
  padding: 16px;
  color: var(--dsw-alias-label-primary, #1f2328);
  font-family: var(--dsw-font-family, ui-sans-serif, system-ui, -apple-system, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif);
  font-size: 14px;
  line-height: 22px;
}

.${PANEL_CLASS} *,
.${PANEL_CLASS} *::before,
.${PANEL_CLASS} *::after {
  box-sizing: border-box;
}

.${PANEL_CLASS} .dsh-vault-head {
  margin-bottom: 14px;
}

.${PANEL_CLASS} .dsh-vault-title {
  margin: 0;
  color: var(--dsw-alias-label-primary, #1f2328);
  font-size: 16px;
  font-weight: 600;
  line-height: 24px;
}

.${PANEL_CLASS} .dsh-vault-sub {
  margin: 2px 0 0;
  color: var(--dsw-alias-label-tertiary, #62676d);
  font-size: 12px;
  line-height: 18px;
}

.${PANEL_CLASS} .dsh-vault-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
  gap: 12px;
}

.${PANEL_CLASS} .dsh-vault-card {
  min-width: 0;
  margin: 0;
  border: .5px solid var(--dsw-alias-border-l4, rgba(0, 0, 0, .12));
  border-radius: 16px;
  background: var(--dsw-alias-bg-layer-1, rgba(255, 255, 255, .02));
  transition: border-color .16s ease;
}

.${PANEL_CLASS} .dsh-vault-card:hover {
  border-color: var(--dsw-alias-border-l3, rgba(0, 0, 0, .2));
}

.${PANEL_CLASS} .dsh-vault-card-summary {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
  min-height: 48px;
  padding: 10px 12px;
  border-radius: 16px;
  color: var(--dsw-alias-label-primary, #1f2328);
  font-size: 14px;
  font-weight: 600;
  line-height: 22px;
  cursor: pointer;
  list-style: none;
}

.${PANEL_CLASS} .dsh-vault-card-summary::-webkit-details-marker,
.${PANEL_CLASS} .dsh-vault-card-summary::marker {
  display: none;
}

.${PANEL_CLASS} .dsh-vault-card-summary:hover {
  background: var(--dsw-alias-interactive-bg-hover, rgba(0, 0, 0, .04));
}

.${PANEL_CLASS} .dsh-vault-card-summary:focus-visible {
  outline: 2px solid var(--dsw-alias-brand-primary, #0f6cbd);
  outline-offset: -2px;
}

.${PANEL_CLASS} .dsh-vault-badge {
  flex: none;
  display: grid;
  place-items: center;
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: var(--dsw-alias-bg-module-platform, rgba(0, 0, 0, .05));
  color: var(--dsw-alias-label-secondary, #444951);
  font-size: 14px;
  font-weight: 600;
  line-height: 1;
}

.${PANEL_CLASS} .dsh-vault-name {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.${PANEL_CLASS} .dsh-vault-meta {
  flex: none;
  color: var(--dsw-alias-label-tertiary, #62676d);
  font-size: 11px;
  font-weight: 400;
  line-height: 16px;
}

.${PANEL_CLASS} .dsh-vault-chevron {
  flex: none;
  position: relative;
  width: 16px;
  height: 16px;
  color: var(--dsw-alias-label-tertiary, #62676d);
}

.${PANEL_CLASS} .dsh-vault-chevron::before {
  content: "";
  position: absolute;
  inset: 4px;
  border-right: 1.5px solid currentColor;
  border-bottom: 1.5px solid currentColor;
  transform: rotate(45deg);
  transition: transform .12s ease;
}

.${PANEL_CLASS} .dsh-vault-card[open] > .dsh-vault-card-summary {
  border-radius: 16px 16px 0 0;
}

.${PANEL_CLASS} .dsh-vault-card[open] > .dsh-vault-card-summary .dsh-vault-chevron::before {
  transform: rotate(225deg);
}

.${PANEL_CLASS} .dsh-vault-card-body {
  padding: 0 12px 12px;
  border-top: .5px solid var(--dsw-alias-border-l2, rgba(0, 0, 0, .08));
}

.${PANEL_CLASS} .dsh-vault-desc {
  margin: 10px 0 8px;
  color: var(--dsw-alias-label-secondary, #444951);
  font-size: 13px;
  line-height: 20px;
}

.${PANEL_CLASS} .dsh-vault-skills {
  margin: 0;
  padding: 0;
  list-style: none;
}

.${PANEL_CLASS} .dsh-vault-skill {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
  padding: 6px 0;
  border-top: .5px solid var(--dsw-alias-border-l1, rgba(0, 0, 0, .06));
}

.${PANEL_CLASS} .dsh-vault-tag {
  flex: none;
  padding: 1px 8px;
  border-radius: 999px;
  font-size: 11px;
  line-height: 16px;
  font-weight: 500;
}

.${PANEL_CLASS} .dsh-vault-tag.is-filled {
  color: var(--dsw-alias-state-success-primary, #16794b);
  background: color-mix(in srgb, var(--dsw-alias-state-success-primary, #16794b) 12%, transparent);
}

.${PANEL_CLASS} .dsh-vault-tag.is-todo {
  color: var(--dsw-alias-state-warn-primary, #8a5a00);
  background: color-mix(in srgb, var(--dsw-alias-state-warn-primary, #8a5a00) 10%, transparent);
}

.${PANEL_CLASS} .dsh-vault-skill-name {
  flex: 1;
  min-width: 0;
  overflow-wrap: anywhere;
  color: var(--dsw-alias-label-primary, #1f2328);
  font-size: 13px;
  line-height: 20px;
}

@media (max-width: 600px) {
  .${PANEL_CLASS} {
    padding: 12px;
  }

  .${PANEL_CLASS} .dsh-vault-grid {
    grid-template-columns: 1fr;
  }

  .${PANEL_CLASS} .dsh-vault-meta {
    display: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .${PANEL_CLASS} .dsh-vault-card,
  .${PANEL_CLASS} .dsh-vault-chevron::before {
    transition: none;
  }
}
`

function el<K extends keyof HTMLElementTagNameMap>(
  tag: K,
  className?: string,
  text?: string,
): HTMLElementTagNameMap[K] {
  const node = document.createElement(tag)
  if (className) node.className = className
  if (text !== undefined) node.textContent = text
  return node
}

function createFormalPanel(): { render(): HTMLElement } {
  return {
    render() {
      const root = el('div', PANEL_CLASS)

      const style = document.createElement('style')
      style.textContent = UI_CSS
      root.appendChild(style)

      const head = el('header', 'dsh-vault-head')
      head.append(
        el('h2', 'dsh-vault-title', '技能库'),
        el('p', 'dsh-vault-sub', '五个正式模块'),
      )
      root.appendChild(head)

      const grid = el('div', 'dsh-vault-grid')
      grid.setAttribute('role', 'list')

      for (const mod of FORMAL_MODULES) {
        const card = el('details', 'dsh-vault-card')
        card.setAttribute('role', 'listitem')

        const summary = el('summary', 'dsh-vault-card-summary')
        summary.append(
          el('span', 'dsh-vault-badge', mod.title.slice(0, 1)),
          el('span', 'dsh-vault-name', mod.title),
        )
        const filled = mod.skills.filter((skill) => skill.status === 'filled').length
        const meta = el('span', 'dsh-vault-meta', `${filled}/${mod.skills.length} 已填充`)
        const chevron = el('span', 'dsh-vault-chevron')
        chevron.setAttribute('aria-hidden', 'true')
        summary.append(meta, chevron)
        card.appendChild(summary)

        const body = el('div', 'dsh-vault-card-body')
        body.appendChild(el('p', 'dsh-vault-desc', mod.description))

        const skills = el('ul', 'dsh-vault-skills')
        skills.setAttribute('role', 'list')
        for (const skill of mod.skills) {
          const row = el('li', 'dsh-vault-skill')
          row.setAttribute('role', 'listitem')
          const tag = el('span', `dsh-vault-tag ${skill.status === 'filled' ? 'is-filled' : 'is-todo'}`, skill.status === 'filled' ? '已填充' : '待实现')
          row.append(tag, el('span', 'dsh-vault-skill-name', skill.title))
          skills.appendChild(row)
        }
        body.appendChild(skills)

        if (mod.experts && mod.experts.length > 0) {
          const experts = el('p', 'dsh-vault-experts', '专家团：' + mod.experts.join(' · '))
          experts.style.color = 'var(--dsw-alias-label-tertiary, #62676d)'
          experts.style.fontSize = '12px'
          experts.style.margin = '8px 0 0'
          body.appendChild(experts)
        }

        card.appendChild(body)

        grid.appendChild(card)
      }

      root.appendChild(grid)
      return root
    },
  }
}

function SkillVaultPanelComponent(): any {
  const hostRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    const container = hostRef.current
    if (!container) return
    const panel = createFormalPanel().render()
    container.replaceChildren(panel)
    return () => {
      if (container.isConnected) container.replaceChildren()
    }
  }, [])

  return createElement('div', { ref: hostRef })
}

export function apply(ctx: ClientContext): void {
  ctx.effect(() => {
    ctx.slots.inject('settings.section', () =>
      ctx.slots.register({
        name: 'settings.section',
        id: 'skill-vault',
        order: 25,
        label: () => '技能库',
      }, SkillVaultPanelComponent),
    )
  }, '@dsh-external/dsh-skill-vault: formal panels')
}
