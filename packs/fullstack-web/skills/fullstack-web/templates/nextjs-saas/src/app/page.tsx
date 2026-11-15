import Link from "next/link";

const features = [
  { title: "Authentication", text: "Email sign-in with Supabase Auth and protected routes." },
  { title: "Database", text: "Postgres with Row Level Security, so users only see their own data." },
  { title: "Dashboard", text: "A clean starting point for your product's core screens." },
];

export default function Home() {
  return (
    <main>
      <section className="mx-auto max-w-5xl px-4 py-24 text-center">
        <h1 className="text-4xl font-extrabold tracking-tight md:text-6xl">Ship your SaaS faster</h1>
        <p className="mx-auto mt-5 max-w-2xl text-lg text-slate-600 dark:text-slate-400">
          Next.js, Supabase and Tailwind, wired together and ready for your idea.
        </p>
        <div className="mt-8 flex justify-center gap-3">
          <Link href="/login" className="rounded-lg bg-indigo-600 px-6 py-3 font-semibold text-white hover:bg-indigo-700">
            Get started
          </Link>
          <Link href="/dashboard" className="rounded-lg border px-6 py-3 font-semibold dark:border-slate-700">
            Dashboard
          </Link>
        </div>
      </section>
      <section className="mx-auto grid max-w-5xl gap-6 px-4 pb-24 md:grid-cols-3">
        {features.map((f) => (
          <article key={f.title} className="rounded-2xl border p-6 dark:border-slate-800">
            <h2 className="font-semibold">{f.title}</h2>
            <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">{f.text}</p>
          </article>
        ))}
      </section>
    </main>
  );
}
