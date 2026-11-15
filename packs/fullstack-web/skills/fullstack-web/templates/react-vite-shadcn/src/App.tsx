import { useMemo, useRef, useState } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";
import { ArrowRight, Moon, Sparkles, Sun, Zap, Layers, Shield } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

gsap.registerPlugin(useGSAP);

const FEATURES = [
  { icon: Zap, title: "Fast by default", text: "Vite dev server and a single-file production build." },
  { icon: Layers, title: "Composable UI", text: "shadcn-style primitives with cva variants and semantic tokens." },
  { icon: Shield, title: "Accessible", text: "Keyboard-friendly tabs, focus rings and reduced-motion support." },
];

const PLANS = { monthly: [0, 19, 49], yearly: [0, 190, 490] } as const;

export default function App() {
  const root = useRef<HTMLDivElement>(null);
  const [dark, setDark] = useState(false);
  const [seats, setSeats] = useState(5);
  const total = useMemo(() => seats * 19, [seats]);

  useGSAP(
    () => {
      const mm = gsap.matchMedia();
      mm.add("(prefers-reduced-motion: no-preference)", () => {
        gsap
          .timeline({ defaults: { ease: "power3.out", duration: 0.7 } })
          .from("[data-anim='badge']", { y: -12, autoAlpha: 0 })
          .from("[data-anim='title']", { y: 32, autoAlpha: 0 }, "<0.1")
          .from("[data-anim='sub']", { y: 20, autoAlpha: 0 }, "<0.15")
          .from("[data-anim='cta'] > *", { y: 12, autoAlpha: 0, stagger: 0.08 }, "<0.1")
          .from("[data-anim='card']", { y: 28, autoAlpha: 0, stagger: 0.1 }, "<0.2");
      });
    },
    { scope: root },
  );

  return (
    <div ref={root} className={dark ? "dark" : ""}>
      <div className="min-h-dvh bg-background text-foreground transition-colors">
        <header className="mx-auto flex max-w-5xl items-center justify-between px-5 py-5">
          <span className="flex items-center gap-2 font-semibold">
            <Sparkles className="size-5 text-primary" aria-hidden /> {"{{TITLE}}"}
          </span>
          <Button variant="ghost" size="icon" aria-label="Toggle dark mode" onClick={() => setDark((d) => !d)}>
            {dark ? <Sun /> : <Moon />}
          </Button>
        </header>

        <main className="mx-auto max-w-5xl px-5 pb-20">
          <section className="py-14 text-center md:py-20">
            <Badge data-anim="badge">React · Vite · Tailwind · shadcn · GSAP</Badge>
            <h1 data-anim="title" className="mx-auto mt-5 max-w-3xl text-4xl font-bold tracking-tight text-balance md:text-6xl">
              Build rich interfaces that ship as one file
            </h1>
            <p data-anim="sub" className="mx-auto mt-4 max-w-xl text-lg text-muted-foreground text-pretty">
              Replace this starter content with your product. Everything here is a working example of the stack.
            </p>
            <div data-anim="cta" className="mt-8 flex justify-center gap-3">
              <Button size="lg">
                Get started <ArrowRight />
              </Button>
              <Button size="lg" variant="outline">
                Learn more
              </Button>
            </div>
          </section>

          <section className="grid gap-4 md:grid-cols-3" aria-label="Features">
            {FEATURES.map(({ icon: Icon, title, text }) => (
              <Card key={title} data-anim="card">
                <Icon className="size-6 text-primary" aria-hidden />
                <CardTitle className="mt-4">{title}</CardTitle>
                <CardDescription>{text}</CardDescription>
              </Card>
            ))}
          </section>

          <section className="mt-16" aria-labelledby="pricing">
            <h2 id="pricing" className="text-2xl font-semibold tracking-tight">
              Pricing
            </h2>
            <Tabs defaultValue="monthly" className="mt-4">
              <TabsList>
                <TabsTrigger value="monthly">Monthly</TabsTrigger>
                <TabsTrigger value="yearly">Yearly</TabsTrigger>
              </TabsList>
              {(Object.keys(PLANS) as (keyof typeof PLANS)[]).map((period) => (
                <TabsContent key={period} value={period} className="grid gap-4 md:grid-cols-3">
                  {["Free", "Pro", "Team"].map((name, i) => (
                    <Card key={name} className={i === 1 ? "border-primary" : undefined}>
                      <CardTitle>{name}</CardTitle>
                      <p className="mt-3 text-3xl font-bold tabular-nums">
                        ${PLANS[period][i]}
                        <span className="text-sm font-normal text-muted-foreground">/{period === "monthly" ? "mo" : "yr"}</span>
                      </p>
                    </Card>
                  ))}
                </TabsContent>
              ))}
            </Tabs>
          </section>

          <section className="mt-16 max-w-sm" aria-labelledby="calc">
            <h2 id="calc" className="text-2xl font-semibold tracking-tight">
              Team cost
            </h2>
            <label className="mt-4 block text-sm font-medium" htmlFor="seats">
              Seats
            </label>
            <Input
              id="seats"
              type="number"
              min={1}
              max={500}
              value={seats}
              onChange={(e) => setSeats(Math.max(1, Math.min(500, Number(e.target.value) || 1)))}
              className="mt-1"
            />
            <p className="mt-3 text-muted-foreground" role="status">
              Total: <span className="font-semibold text-foreground tabular-nums">${total}</span> / month
            </p>
          </section>
        </main>
      </div>
    </div>
  );
}
