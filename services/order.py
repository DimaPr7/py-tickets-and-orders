from django.db import transaction
from db.models import Order, Ticket, MovieSession, User


@transaction.atomic
def create_order(tickets: list[Ticket],
                 username: str, date: str = None) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()
    for ticket in tickets:
        movie_session_id = ticket["movie_session"]
        movie_session = (MovieSession.objects.get
                         (pk=movie_session_id))
        Ticket.objects.create(
            order=order,
            movie_session=movie_session,
            row=ticket["row"],
            seat=ticket["seat"])


def get_orders(username: str = None):
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()