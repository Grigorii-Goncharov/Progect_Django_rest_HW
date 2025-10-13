import os
import stripe
from django.shortcuts import get_object_or_404
from education.models import Course, Lesson
from users.models import Payment

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def create_stripe_product_and_price(name, description, amount, currency="usd"):
    """Создаёт продукт и цену в Stripe, возвращает ID цены."""
    product = stripe.Product.create(name=name, description=description[:200])
    price = stripe.Price.create(
        product=product.id,
        unit_amount=int(amount * 100),  # в центах
        currency=currency,
        recurring=None,
    )
    return price.id


def create_payment_record(user, course=None, lesson=None):
    """Создаёт черновик записи модели Payment"""
    if not course and not lesson:
        raise ValueError("Должен быть указан course или lesson")
    if course and lesson:
        raise ValueError("Нельзя указывать и course, и lesson одновременно")

    amount = course.price if course else lesson.price
    return Payment.objects.create(
        user=user,
        course=course,
        lesson=lesson,
        amount=amount,
        payment_method="transfer",
        stripe_status="pending",
    )


def process_course_payment(user, course_id):
    """Полный процесс оплаты курса: от создания платежа до сессии."""
    course = get_object_or_404(Course, id=course_id)
    payment = create_payment_record(user, course=course)

    description = f"Оплата курса: {course.title}"
    price_id = create_stripe_product_and_price(
        name=course.title, description=description, amount=course.price
    )

    session_data = create_checkout_session(
        user=user,
        price_id=price_id,
        payment_id=payment.id,
        item_type="course",
        item_id=course.id,
    )

    # Обновляем платеж
    payment.stripe_payment_intent_id = session_data["payment_intent"]
    payment.save()

    return {"payment": payment, "course": course, "checkout_url": session_data["url"]}


def process_lesson_payment(user, lesson_id):
    """Полный процесс оплаты урока: от создания платежа до сессии."""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    payment = create_payment_record(user, lesson=lesson)

    description = f"Оплата урока: {lesson.title} (курс: {lesson.course.title})"
    price_id = create_stripe_product_and_price(
        name=lesson.title, description=description, amount=lesson.price
    )

    session_data = create_checkout_session(
        user=user,
        price_id=price_id,
        payment_id=payment.id,
        item_type="lesson",
        item_id=lesson.id,
    )

    payment.stripe_payment_intent_id = session_data["payment_intent"]
    payment.save()

    return {"payment": payment, "lesson": lesson, "checkout_url": session_data["url"]}


def create_checkout_session(user, price_id, payment_id, item_type, item_id):
    """Создаёт итоговый результат сессии после оплаты"""
    metadata = {
        "payment_id": str(payment_id),
        "type": item_type,
        "course_id" if item_type == "course" else "lesson_id": str(item_id),
    }

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
        customer_email=user.email,
        success_url="http://127.0.0.1:8000/",
        cancel_url="http://127.0.0.1:8000/",
        metadata=metadata,
    )
    return {"url": session.url, "payment_intent": session.payment_intent}
