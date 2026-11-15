import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";
import { createProject, signOut } from "./actions";

export const metadata = { title: "Dashboard" };

export default async function DashboardPage() {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const { data: projects, error } = await supabase
    .from("projects")
    .select("id, name, created_at")
    .order("created_at", { ascending: false });

  async function addProject(formData: FormData) {
    "use server";
    await createProject(formData);
  }

  async function logout() {
    "use server";
    await signOut();
    redirect("/login");
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-10">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <form action={logout}>
          <span className="mr-3 text-sm text-slate-500">{user.email}</span>
          <button className="rounded-lg border px-3 py-1.5 text-sm dark:border-slate-700">Sign out</button>
        </form>
      </header>

      <form action={addProject} className="mt-8 flex gap-2">
        <label className="sr-only" htmlFor="name">Project name</label>
        <input id="name" name="name" placeholder="New project name" required maxLength={100}
          className="flex-1 rounded-lg border px-3 py-2 dark:border-slate-700 dark:bg-slate-900" />
        <button className="rounded-lg bg-indigo-600 px-4 py-2 font-semibold text-white hover:bg-indigo-700">Add</button>
      </form>

      {error && <p className="mt-6 text-sm text-red-600">Could not load projects: {error.message}</p>}
      {!error && projects?.length === 0 && (
        <p className="mt-10 rounded-xl border border-dashed p-8 text-center text-slate-500 dark:border-slate-700">
          No projects yet. Create your first one above.
        </p>
      )}
      <ul className="mt-6 space-y-2">
        {projects?.map((p) => (
          <li key={p.id} className="rounded-xl border p-4 dark:border-slate-800">
            <p className="font-medium">{p.name}</p>
            <p className="text-xs text-slate-500">{new Date(p.created_at).toLocaleString()}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
