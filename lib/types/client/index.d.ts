/**
 * @dsh-external/dsh-skill-vault — client 面板（conversation.view slot）。
 *
 * 交互：从 /skill-vault/api/list 拉取场景与 skill，渲染开关面板；
 * 点击 skill 行调用 /skill-vault/api/enable 或 /disable。
 */
interface SlotRegistration {
    name: string;
    id: string;
    label: () => string;
    component: () => {
        render(): HTMLElement;
    };
}
interface SlotsService {
    inject(slot: string, factory: () => unknown): unknown;
    register(reg: SlotRegistration): unknown;
}
interface EffectContext {
    effect(fn: () => unknown, label?: string): unknown;
}
type ClientContext = EffectContext & {
    slots: SlotsService;
};
export declare const inject: string[];
export declare function apply(ctx: ClientContext): void;
export {};
