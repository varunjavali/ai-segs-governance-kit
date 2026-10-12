export type Money = { amountMinor: number; currency: string };
export const isPositive = (m: Money): boolean => m.amountMinor > 0;
