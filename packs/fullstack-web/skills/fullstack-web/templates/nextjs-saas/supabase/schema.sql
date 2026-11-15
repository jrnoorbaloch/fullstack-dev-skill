-- Run in Supabase → SQL Editor
create table if not exists public.projects (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  name text not null check (char_length(name) between 1 and 100),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists projects_user_id_idx on public.projects(user_id);

alter table public.projects enable row level security;

create policy "Users read own projects"   on public.projects for select using (auth.uid() = user_id);
create policy "Users insert own projects" on public.projects for insert with check (auth.uid() = user_id);
create policy "Users update own projects" on public.projects for update using (auth.uid() = user_id);
create policy "Users delete own projects" on public.projects for delete using (auth.uid() = user_id);
