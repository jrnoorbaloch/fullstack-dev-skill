# Industry Blueprints

Ready feature lists for common businesses. Use the matching blueprint as the default scope, then adjust to the user's request. "Site" = public website; "App" = logged-in features.

## 🍽️ Restaurant / café / bakery
- **Site:** hero with signature dish photo, menu with categories and prices, opening hours, location map, WhatsApp/call button, gallery, reviews, reservation form.
- **App:** online ordering (cart, delivery/pickup, COD + online payment), order tracking, admin for menu items, stock "sold out" toggle, daily sales.
- **Data:** categories, menu_items, orders, order_items, reservations, customers.

## 🏥 Clinic / doctor / hospital
- **Site:** services, doctors with specialties and timings, appointment booking, insurance/panel info, FAQs, emergency contact.
- **App:** slot-based booking with doctor calendars, reminders (SMS/WhatsApp/email), patient records (restricted access), prescriptions PDF, admin schedule management.
- **Data:** doctors, schedules, slots, appointments, patients, visits, prescriptions. **Privacy:** role-based access, audit log.

## 🏫 School / academy / LMS
- **Site:** programs, admissions form, faculty, fee structure, events/news, gallery.
- **App:** student/teacher/parent roles, attendance, timetable, assignments, results/report cards, fee vouchers & payment status, notices; LMS: courses, video lessons, quizzes, progress, certificates.
- **Data:** classes, sections, students, guardians, teachers, subjects, attendance, exams, results, fees, courses, lessons, enrollments.

## 🏠 Real estate
- **Site:** property listings with filters (city, type, price, beds, area), detail page with gallery and map, agent contact, mortgage calculator.
- **App:** agent dashboard to add/edit listings, leads inbox, saved searches/favorites for users, featured listings.
- **Data:** properties, property_images, agents, leads, favorites.

## 🛒 E-commerce / online store
- **Site/App:** catalog with categories, search, filters, product variants (size/color), cart, checkout (COD + online), order tracking, reviews, wishlist, coupons.
- **Admin:** products, inventory, orders with status flow (pending → confirmed → shipped → delivered), customers, sales reports, low-stock alerts.
- **Data:** products, variants, categories, carts, orders, order_items, coupons, reviews, addresses.

## 💪 Gym / fitness studio
- **Site:** classes and trainers, membership plans, timetable, trial-class form, transformations gallery.
- **App:** member accounts, plan purchase/renewal, class booking with capacity, attendance check-in (QR), workout/diet plans, renewal reminders.
- **Data:** members, plans, subscriptions, classes, sessions, bookings, check_ins.

## 💇 Salon / spa / barber
- **Site:** services with prices and durations, stylists, gallery, booking.
- **App:** booking by service + stylist + slot, deposits, reminders, loyalty points, staff schedule, daily cash report.
- **Data:** services, staff, availability, bookings, customers, payments.

## 🏨 Hotel / guest house
- **Site:** rooms with photos and amenities, availability search by dates, booking, location, policies.
- **App:** room inventory and rates by date, bookings with check-in/check-out, invoices, housekeeping status.
- **Data:** room_types, rooms, rates, bookings, guests, invoices.

## 🚚 Delivery / logistics
- **Apps:** customer (order, live tracking), rider (assigned jobs, navigation, status updates, proof of delivery photo), admin (dispatch, zones, pricing, COD reconciliation).
- **Data:** orders, stops, riders, zones, tracking_events, cod_collections. Realtime location via Supabase Realtime or websockets.

## 🏪 Retail shop / POS / inventory
- **Desktop or web:** barcode sales, receipts, returns, stock in/out, suppliers, purchase orders, customer credit (khata), daily/monthly reports, multi-user roles, backups.
- Start from `templates/python-desktop-pos` for offline shops.

## 💼 Agency / freelancer / portfolio
- **Site:** hero with positioning, services, case studies with results, testimonials, process, pricing/packages, contact/booking (Calendly link).
- **App (optional):** client portal with project status, files and invoices.

## 🕌 NGO / mosque / community
- **Site:** mission, programs, events calendar, donation (one-off + recurring), volunteer signup, transparency reports, prayer times (mosque).
- **App:** donor dashboard and receipts, event registrations, admin for announcements.

## 🧾 SaaS (B2B tool)
- Landing + pricing, auth, team/workspace with roles and invitations, core feature dashboard, billing (Stripe subscriptions), settings, audit log, onboarding checklist, usage limits per plan.

---

For each blueprint always add: SEO basics, contact/WhatsApp, analytics, privacy policy & terms pages, admin role, backups, and mobile-first design.
