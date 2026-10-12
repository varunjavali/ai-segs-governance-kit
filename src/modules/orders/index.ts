import { refund } from '../billing';
import { Money, isPositive } from '@modules/shared';

export function cancelPaidOrder(orderId: string, paid: Money) {
  return isPositive(paid) ? refund(orderId, paid) : null;
}
