import { Money } from '../shared';

export function refund(orderId: string, amount: Money): { refundId: string } {
  return { refundId: `refund-${orderId}-${amount.amountMinor}` };
}
