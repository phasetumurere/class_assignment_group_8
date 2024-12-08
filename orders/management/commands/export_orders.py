from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Export orders to a CSV file'

    def handle(self, *args, **options):
        from orders.models import Order  # Import here to avoid circular issues
        import csv

        output_file = 'orders_export.csv'

        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Order ID', 'User ID', 'Order Total', 'Date Created'])

            orders = Order.objects.all()

            for order in orders:
                writer.writerow([order.id, order.user_id, order.order_total, order.date_created])

        self.stdout.write(self.style.SUCCESS(f"Orders have been successfully exported to {output_file}"))
