interface SlotRegistration {
    name: string;
    id: string;
    label: () => string;
    order?: number;
}
interface SlotsService {
    inject(slot: string, factory: () => unknown): unknown;
    register(reg: SlotRegistration, component: (props?: any) => any): unknown;
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
