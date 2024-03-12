from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from .models import Order
from decimal import Decimal

class OrderStats(APIView):
    def get(self, request, merchant_id, start_date, end_date):
        orders = Order.objects.filter(merchant_id=merchant_id, order_completed_date__range=[start_date, end_date])
        
        total_orders = orders.count()
        total_item_value = orders.aggregate(Sum('item_value'))['item_value__sum'] or 0

        print(total_item_value)
        
        prepaid_orders = orders.filter(order_type='prepaid')
        total_prepaid_item_value = prepaid_orders.aggregate(Sum('item_value'))['item_value__sum'] or 0
        taxable_prepaid_value = prepaid_orders.aggregate(Sum('taxable_value'))['taxable_value__sum'] or 0
        non_taxable_prepaid_value = prepaid_orders.aggregate(Sum('non_taxable_value'))['non_taxable_value__sum'] or 0
        total_prepaid_delivery_charge = prepaid_orders.aggregate(Sum('delivery_charge'))['delivery_charge__sum'] or 0
        total_prepaid_packing_charge = prepaid_orders.aggregate(Sum('packing_charge'))['packing_charge__sum'] or 0
        prepaid_loyalty_discounts = prepaid_orders.aggregate(Sum('loyalty_discount'))['loyalty_discount__sum']or 0 
        total_prepaid_order_value = total_prepaid_item_value + total_prepaid_delivery_charge + total_prepaid_packing_charge - prepaid_loyalty_discounts
        


        postpaid_orders = orders.filter(order_type='postpaid')
        total_postpaid_item_value = postpaid_orders.aggregate(Sum('item_value'))['item_value__sum'] or 0
        taxable_postpaid_value = postpaid_orders.aggregate(Sum('taxable_value'))['taxable_value__sum'] or 0
        non_taxable_postpaid_value = postpaid_orders.aggregate(Sum('non_taxable_value'))['non_taxable_value__sum'] or 0
        total_postpaid_delivery_charge = postpaid_orders.aggregate(Sum('delivery_charge'))['delivery_charge__sum'] or 0
        total_postpaid_packing_charge = postpaid_orders.aggregate(Sum('packing_charge'))['packing_charge__sum'] or 0
        postpaid_loyalty_discounts = postpaid_orders.aggregate(Sum('loyalty_discount'))['loyalty_discount__sum'] or 0
        total_postpaid_order_value = total_postpaid_item_value + total_postpaid_delivery_charge + total_postpaid_packing_charge - postpaid_loyalty_discounts
        print(total_postpaid_packing_charge)
        commission_percentage = 5  # Example commission percentage
        # total_item_value_float = float(total_item_value)

        commission_percentage_decimal = Decimal(commission_percentage)
        commission = commission_percentage_decimal / 100 * total_item_value
        # commission = commission_percentage / 100 * total_item_value
        # cgst = 0.09 * commission
        cgst_rate = Decimal('0.09')
        cgst = cgst_rate * commission
        # sgst = 0.09 * commission
        sgst_rate = Decimal('0.09')
        sgst = sgst_rate * commission
        # tcs =  0.01 * taxable_prepaid_value
        tcs_rate = Decimal('0.01')  # Convert the TCS rate to Decimal
        tcs = tcs_rate * taxable_prepaid_value
        
        final_settlement_amount = total_prepaid_order_value - commission - cgst - sgst - tcs
        print(final_settlement_amount)
        
        response_data = {
            "total_orders": total_orders,
            "total_item_value": total_item_value,
            "total_prepaid_orders": prepaid_orders.count(),
            "total_prepaid_item_value": total_prepaid_item_value,
            "taxable_prepaid_value": taxable_prepaid_value,
            "non_taxable_prepaid_value": non_taxable_prepaid_value,
            "total_prepaid_delivery_charge": total_prepaid_delivery_charge,
            "total_prepaid_packing_charge": total_prepaid_packing_charge,
            "prepaid_loyalty_discounts": prepaid_loyalty_discounts,
            "total_prepaid_order_value": total_prepaid_order_value,
            "total_postpaid_orders": postpaid_orders.count(),
            "total_postpaid_item_value": total_postpaid_item_value,
            "taxable_postpaid_value": taxable_postpaid_value,
            "non_taxable_postpaid_value": non_taxable_postpaid_value,
            "total_postpaid_delivery_charge": total_postpaid_delivery_charge,
            "total_postpaid_packing_charge": total_postpaid_packing_charge,
            "postpaid_loyalty_discounts": postpaid_loyalty_discounts,
            "total_postpaid_order_value": total_postpaid_order_value,
            "commission": commission,
            "cgst": cgst,
            "sgst": sgst,
            "tcs": tcs,
            "final_settlement_amount": final_settlement_amount,
        }
        
        return Response(response_data)
