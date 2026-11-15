import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: { default: "My SaaS", template: "%s · My SaaS" },
  description: "A SaaS starter built with Next.js and Supabase.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-white text-slate-800 antialiased dark:bg-slate-950 dark:text-slate-100">
        {children}
      </body>
    </html>
  );
}
