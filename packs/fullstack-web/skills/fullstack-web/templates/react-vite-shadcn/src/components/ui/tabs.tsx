import { createContext, use, useId, useState } from "react";
import { cn } from "@/lib/utils";

type Ctx = { value: string; setValue: (v: string) => void; id: string };
const TabsContext = createContext<Ctx | null>(null);
function useTabs() {
  const ctx = use(TabsContext);
  if (!ctx) throw new Error("Tabs components must be used inside <Tabs>");
  return ctx;
}

export function Tabs({
  defaultValue,
  value: controlled,
  onValueChange,
  className,
  children,
}: {
  defaultValue: string;
  value?: string;
  onValueChange?: (v: string) => void;
  className?: string;
  children: React.ReactNode;
}) {
  const [inner, setInner] = useState(defaultValue);
  const value = controlled ?? inner;
  const setValue = (v: string) => {
    setInner(v);
    onValueChange?.(v);
  };
  return (
    <TabsContext value={{ value, setValue, id: useId() }}>
      <div className={className}>{children}</div>
    </TabsContext>
  );
}

export function TabsList({ className, ...props }: React.ComponentProps<"div">) {
  return <div role="tablist" className={cn("inline-flex gap-1 rounded-lg bg-muted p-1", className)} {...props} />;
}

export function TabsTrigger({ value, className, ...props }: React.ComponentProps<"button"> & { value: string }) {
  const t = useTabs();
  const selected = t.value === value;
  return (
    <button
      role="tab"
      id={`${t.id}-tab-${value}`}
      aria-selected={selected}
      aria-controls={`${t.id}-panel-${value}`}
      tabIndex={selected ? 0 : -1}
      onClick={() => t.setValue(value)}
      className={cn(
        "rounded-md px-3 py-1.5 text-sm font-medium text-muted-foreground transition-colors aria-selected:bg-background aria-selected:text-foreground aria-selected:shadow-sm",
        className,
      )}
      {...props}
    />
  );
}

export function TabsContent({ value, className, ...props }: React.ComponentProps<"div"> & { value: string }) {
  const t = useTabs();
  if (t.value !== value) return null;
  return (
    <div role="tabpanel" id={`${t.id}-panel-${value}`} aria-labelledby={`${t.id}-tab-${value}`} className={cn("mt-4", className)} {...props} />
  );
}
